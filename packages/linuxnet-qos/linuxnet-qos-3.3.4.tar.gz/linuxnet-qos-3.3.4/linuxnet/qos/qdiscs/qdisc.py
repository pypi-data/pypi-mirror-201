# Copyright (c) 2021, 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-qos.
#
# linuxnet-qos is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-qos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-qos. If not, see
# <https://www.gnu.org/licenses/>.

"""
This module provides the basic traffic queueing classes.

It is important to note that traffic shaping based on the
source IP address will not have the desirable result when doing
NAT before the interface where traffic shaping takes place
(this would be the case when NATing traffic before an ISP-connected
interface).
"""

import re

from typing import Iterator, List, Mapping, Optional, TextIO

from ..deps import get_logger
from ..exceptions import TcError
from ..handle import Handle
from ..tcunit import bwstr2int

_logger = get_logger("linuxnet.qos.qdiscs.qdisc")


class QStats:           # pylint: disable=too-many-instance-attributes
    """QStats holds statistics for either queuing class or queuing
    disciplines.

    Statistics that are common across all queuing disciplines are accessible
    as properties. The rest are accessible via getter methods, which
    the subclasses may use to convert to properties.
    """

    HEADER_WIDTH = 15

    __LINE2_REGEX_PROG = re.compile(
            r"Sent (\d+) bytes (\d+) pkt "
            r"[(]dropped (\d+), overlimits (\d+) requeues (\d+)[)]")
    __LINE3_REGEX_PROG_V1 = re.compile(
            r"rate (\d+\w+) (\d+)pps backlog (\d+)b (\d+)p requeues (\d+)")
    __LINE3_REGEX_PROG_V2 = re.compile(
            r"backlog (\d+)b (\d+)p requeues (\d+)")

    def __init__(self):
        self.__bytes_sent = 0
        self.__packets_sent = 0
        self.__dropped = 0
        self.__overlimits = 0
        self.__requeues = 0
        self.__bitrate = 0
        self.__pktrate = 0
        self.__byte_backlog = 0
        self.__packet_backlog = 0

    @property
    def bitrate(self) -> int:
        """Consumed bandwidth measured in bits/sec
        """
        return self.__bitrate

    @property
    def packetrate(self) -> int:
        """Consumed bandwidth measured in packets/sec
        """
        return self.__pktrate

    @property
    def bytes_sent(self) -> int:
        """Number of bytes sent.
        """
        return self.__bytes_sent

    @property
    def packets_sent(self) -> int:
        """Number of packets sent.
        """
        return self.__packets_sent

    @property
    def dropped_packets(self) -> int:
        """Number of packets dropped.
        """
        return self.__dropped

    @property
    def requeued_packets(self) -> int:
        """Number of packets that were requeued for some reason.
        """
        return self.__requeues

    def get_overlimits(self) -> int:
        """Number of times a packet was delayed due to rate limits.
        """
        return self.__overlimits

    def get_byte_backlog(self) -> int:
        """Queue backlog in bytes
        """
        return self.__byte_backlog

    def get_packet_backlog(self) -> int:
        """Queue backlog in packets
        """
        return self.__packet_backlog

    def __parse_second_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 2nd line
        of ``tc qdisc ls`` (or ``tc class ls``) output.
        """
        # The line looks like this:
        #
        #   Sent 566719 bytes 1669 pkt (dropped 0, overlimits 0 requeues 0)
        #
        match = self.__LINE2_REGEX_PROG.match(line.strip())
        if match is None:
            _logger.warning("2nd line not parsable: %s", line)
            return False
        self.__bytes_sent = int(match.group(1))
        self.__packets_sent = int(match.group(2))
        self.__dropped = int(match.group(3))
        self.__overlimits = int(match.group(4))
        self.__requeues = int(match.group(5))
        return True

    def __parse_third_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 3rd line
        of ``tc qdisc ls`` (or ``tc class ls``) output
        """
        # The line looks like this:
        #
        #   rate 9280bit 1pps backlog 0b 0p requeues 0
        #
        match = self.__LINE3_REGEX_PROG_V1.match(line.strip())
        if match is not None:
            self.__bitrate = bwstr2int(match.group(1))
            self.__pktrate = int(match.group(2))
            self.__byte_backlog = int(match.group(3))
            self.__packet_backlog = int(match.group(4))
            requeues = int(match.group(5))
        else:
            match = self.__LINE3_REGEX_PROG_V2.match(line.strip())
            if match is None:
                _logger.warning("3rd line not parsable: %s", line)
                return False
            self.__byte_backlog = int(match.group(1))
            self.__packet_backlog = int(match.group(2))
            requeues = int(match.group(3))
        if requeues != self.__requeues:
            _logger.warning(
                "requeue mismatch between 2nd and 3rd line: l2=%d l3=%d",
                    self.__requeues, requeues)
        return True

    def init_from_output(self, line_group_iter: 'LineGroupIter') -> bool:
        """Initialize attributes from the lines in ``line_group_iter``.
        The iterator returns the lines of the output of ``tc -s qdisc ls``
        for a single qdisc; the first line of the output has already been
        consumed, and the 2nd line is the next to be returned.
        """
        # Parse the 2nd and 3rd lines which look like this:
        #
        #  Sent 22557655 bytes 241990 pkt (dropped 0, overlimits 0 requeues 0)
        #  rate 104bit 0pps backlog 0b 0p requeues 0
        #
        try:
            line = next(line_group_iter)
            if not self.__parse_second_line(line):
                return False
            line = next(line_group_iter)
            if not self.__parse_third_line(line):
                return False
        except StopIteration:
            return False
        except ValueError as valerr:
            _logger.warning("bad value in stats line: %s (line=%s)",
                                valerr, line)
            return False
        return True

    def dump(self, outfile: TextIO, width: Optional[int] =None) -> None:
        """Dump the common stats to ``outfile``.
        There is one stat per line output. Each line has the format::

            header: value

        The ``header:`` part occupies at least ``width`` characters.
        """
        width = width or self.HEADER_WIDTH
        print(f"{'Sent:':{width}} "
            f'{self.__bytes_sent} bytes / {self.__packets_sent} packats',
                file=outfile)
        print(f"{'Rate:':{width}} "
            f'{self.__bitrate} bps / {self.__pktrate} pps',
                file=outfile)
        print(f"{'Dropped:':{width}} {self.__dropped}", file=outfile)
        print(f"{'Requeues:':{width}} {self.__requeues}", file=outfile)


class QNode:
    """Used as a base class for the Python classes :class:`QDisc` and
    :class:`QClass` which are the actual nodes of the traffic
    classification tree.

    A path from the root of the tree down to a leaf looks like this::

        QDisc -> QClass+ -> QDisc

    where the ``QClass+ -> QDisc`` can repeat 0 or more times, and
    the final ``QDisc`` may not be present (``pfifo`` is implied)
    """

    def __init__(self, handle: Handle, parent_handle: Optional[Handle]):
        """
        :param handle: :class:`Handle` of this :class:`QClass`/:class:`QDisc`
        :param parent_handle: :class:`Handle` of the parent of this
            :class:`QClass`/:class:`QDisc`
        """
        self.__handle = handle
        self.__parent_handle = parent_handle
        # Key: Handle
        # Value: QClass
        self.__child_map = {}
        # List of TrafficFilter's; initialized to None for lazy evaluation
        self.__filters = None
        self.__can_retrieve_filters = True
        # If the config is not None, this qdisc/qclass is instantiated.
        self.__config = None
        self.__stats = None

    def __init_filters(self, refresh=False, must_retrieve=True) -> bool:
        """Initialize self.__filters

        Returns True if the filters have been retrieved, either by this
        invocation or a previous one.
        """
        if self.__filters is not None and not refresh:
            return True
        if not self.__can_retrieve_filters:
            if must_retrieve:
                raise TcError('cannot retrieve filters')
            return False
        self.__filters = self.__config.retrieve_filters(self)
        return True

    def _instantiate(self, node: str, cmd: List[str], config):
        """This method creates a qdisc/qclass.
        """
        if self.__config is not None:
            raise TcError(
                f'{node} already instantiated on '
                f'interface {self.__config.get_interface()}')
        config.tc_run(cmd, f"{node} {self.__handle!s} creation")
        self.__config = config
        self.__filters = []

    def _uninstantiate(self, node: str, cmd: List[str], config):
        """This method deletes a qdisc/qclass.
        """
        if self.__config is None:
            raise TcError(f'{node} not instantiated')
        my_interface = self.__config.get_interface()
        config_interface = config.get_interface()
        if my_interface != config_interface:
            raise TcError(
                f'{node} instantiated on interface {my_interface} '
                f'instead of {config_interface}')
        config.tc_run(cmd, f"{node} {self.__handle!s} deletion")
        self.__config = None
        self.__filters = None

    def get_handle(self) -> Handle:
        """Returns the :class:`QDisc`/:class:`QClass` handle
        """
        return self.__handle

    def get_parent_handle(self) -> Optional[Handle]:
        """Returns the handle of the parent of this
        :class:`QDisc`/:class:`QClass`
        """
        return self.__parent_handle

    def get_config(self) -> 'QDiscConfig':
        """Returns the :class:`QDiscConfig` where this
        :class:`QDisc`/:class:`QClass` has been instantiated, or ``None``
        if not instantiated.
        """
        return self.__config

    def get_interface(self) -> Optional[str]:
        """Returns the interface where this :class:`QDisc`/:class:`QClass`
        has been instantiated, or ``None`` if the :class:`QDisc`/:class:`QClass`
        is not instantiated.
        """
        if self.__config is None:
            return None
        return self.__config.get_interface()

    def get_child_count(self) -> int:
        """Return number of children of this :class:`QDisc`/:class:`QClass`
        """
        return len(self.__child_map)

    def get_child(self, handle: Handle) -> Optional['QClass']:
        """Returns the :class:`QClass` with the specified handle
        """
        return self.__child_map.get(handle)

    def get_child_iter(self) -> Iterator['QClass']:
        """Returns an iterator for the :class:`QClass` children of this
        :class:`QDisc`/:class:`QClass`.
        """
        return iter(self.__child_map.values())

    def get_children(self) -> List['QClass']:
        """Returns the children of this :class:`QDisc`/:class:`QClass`.
        """
        return list(self.__child_map.values())

    def get_filters(self, refresh=False) -> List['TrafficFilter']:
        """Returns (a copy of) the list of filters at this
        :class:`QDisc`/:class:`QClass`

        :param refresh: if ``True``, a fresh copy of the filter list is
            obtained using the **tc(8)** command.
        """
        if self.__init_filters(refresh=refresh, must_retrieve=False):
            return self.__filters[:]
        return []

    def get_stats(self) -> Optional[QStats]:
        """Returns queuing stats.
        """
        return self.__stats

    def _add_child_class(self, qclass: 'QClass') -> None:
        """Add ``qclass`` as a child of this :class:`QDisc`/:class:`QClass`
        """
        handle = qclass.get_handle()
        if handle in self.__child_map:
            _logger.error("%s: %s: attempt to add child '%s' twice",
                self._add_child_class.__qualname__, self, qclass)
            raise TcError(f'{qclass} already a child of {self}')
        self.__child_map[handle] = qclass

    def _remove_child_class(self, qclass: 'QClass') -> None:
        """Remove ``qclass`` from the children of this
        :class:`QDisc`/:class:`QClass`.

        When this method is invoked, the class **has already been removed**
        from the kernel.

        If the ``qclass`` is not a child of this :class:`QDisc`/:class:`QClass`,
        this method does nothing.
        """
        child = self.__child_map.pop(qclass.get_handle(), None)
        if child is None:
            _logger.warning("%s: %s: not a child: %s",
                self._remove_child_class.__qualname__, self, qclass)

    def _set_config(self, config) -> None:
        """This method is used when parsing an existing configuration.
        """
        if self.__config is not None:
            raise TcError(
                f'{self} already associated with '
                f'interface {self.__config.get_interface()}')
        self.__config = config

    def _replace_handle(self, new_handle: Handle) -> None:
        """Replace the handle of this node.
        """
        _logger.info("%s: replacing handle %s with %s",
                                self, self.__handle, new_handle)
        self.__handle = new_handle
        self.__can_retrieve_filters = False
        self.__filters = None

    def _parse_stats(self, line_group_iter: 'LineGroupIterator') -> None:
        """Parse queuing stats.
        """
        stats = QStats()
        if stats.init_from_output(line_group_iter):
            self.__stats = stats

    def create_filter(self, traffic_filter: 'TrafficFilter') -> None:
        """Create the filter ``traffic_filter``.
        """
        if self.__config is None:
            _logger.error(
                "%s: cannot create filter %s because %s is not instantiated",
                    self.create_filter.__qualname__,
                    traffic_filter, self)
            raise TcError(
                f'cannot create filter because {self} is not instantiated')
        self.__init_filters()
        traffic_filter._instantiate(owner=self)
        self.__filters.append(traffic_filter)

    def delete_filter(self, traffic_filter: 'TrafficFilter') -> None:
        """Delete the filter  ``traffic_filter``.
        """
        if self.__config is None:
            _logger.error(
                "%s: cannot delete filter %s because %s is not instantiated",
                    self.delete_filter.__qualname__,
                    traffic_filter, self)
            raise TcError(
                f'cannot delete filter because {self} is not instantiated')
        self.__init_filters()
        traffic_filter._uninstantiate(owner=self)
        self.__filters.remove(traffic_filter)

    def get_description(self) -> str:
        """Return a string that *fully* describes this node
        (name + attributes)
        """
        raise NotImplementedError

    def dump(self, outfile: TextIO, level: int,
                qclass_map: Mapping[Handle, 'QClass']) -> None:
        """Recursively dump this node and all its child classes to ``outfile``
        """
        prefix = '    ' * level
        print(prefix + self.get_description(), file=outfile)
        self.__init_filters(must_retrieve=False)
        if self.__filters:
            print(prefix + '  Filters:', file=outfile)
            filter_list = sorted(self.__filters, key=lambda f: f.get_prio())
            for traffic_filter in filter_list:
                printval = prefix + '    ' + traffic_filter.get_description()
                dest = traffic_filter.get_dest_handle()
                if dest is not None:
                    qclass = qclass_map.get(dest)
                    if qclass is not None:
                        printval += f' ---> {qclass.get_class_name()} ({dest})'
                    else:
                        printval += f' ---> {dest}'
                else:
                    printval += ' (NO-DESTINATION)'
                print(printval, file=outfile)
        if self.__child_map:
            print(prefix + '  Classes:', file=outfile)
            qclass_list = list(self.__child_map.values())
            qclass_list.sort(key=lambda c: c.get_handle().minor)
            for qclass in qclass_list:
                qclass.dump(outfile, level+1, qclass_map)


class QClass(QNode):
    """Used as a base class for all queuing discipline specific classes

    A :class:`QClass` object can either have a queuing discipline as a child,
    or it can have a set of :class:`QClass` objects.
    """

    def __init__(self, handle: Handle, parent_handle: Handle,
                        class_name: Optional[str] =None):
        """
        :param handle: :class:`Handle` of this :class:`QClass`
        :param parent_handle: :class:`Handle` of the parent of this
            :class:`QClass`
        :param class_name: optional class name; defaults to the class handle
        """
        super().__init__(handle, parent_handle)
        # descriptive class name
        self.__class_name = class_name or f'class-{handle}'
        # A leaf class should have a qdisc; may be None if using a
        # default qdisc (pfifo)
        self.__qdisc = None

    def __str__(self):
        return f'QClass({self.get_handle()})'

    def get_description(self) -> str:
        """Return a string that *fully* describes this :class:`QCclass`
        """
        return f'{self} parent {self.get_parent_handle()}'

    def get_class_name(self) -> str:
        """Returns the class name
        """
        return self.__class_name

    def set_class_name(self, class_name: str) -> None:
        """Sets the class name
        """
        self.__class_name = class_name

    def _instantiate_qclass(self, config) -> None:
        """Invoke the **tc(8)** command to create the queuing class
        described by this object.

        :param config: a :class:`QDiscConfig` object
        """
        class_handle_str = str(self.get_handle())
        cmd = ['tc', 'class', 'add', 'dev', config.get_interface(),
                    'parent', str(self.get_parent_handle()),
                    'classid', class_handle_str]
        # Derived Python class provides the qclass-specific arguments
        cmd.extend(self.qclass_creation_args())
        self._instantiate('class', cmd, config)

    def _uninstantiate_qclass(self, config) -> None:
        """Invoke the **tc(8)** command to delete the queuing class
        described by this object.

        :param config: a :class:`QDiscConfig` object
        """
        class_handle_str = str(self.get_handle())
        cmd = ['tc', 'class', 'del', 'dev', config.get_interface(),
                    'classid', class_handle_str]
        self._uninstantiate('class', cmd, config)

    def qclass_creation_args(self) -> List[str]:
        """Returns the class-specific arguments passed to tc
        to create the particular class

        It must be implemented by the derived Python class.
        """
        raise NotImplementedError

    def is_leaf(self) -> bool:
        """Returns ``True`` if this is a leaf queuing class
        """
        return self.get_child_count() == 0

    def get_qdisc(self) -> Optional['QDisc']:
        """Returns the :class:`QDisc` under with this :class:`QClass`,
        or ``None`` if this is not a leaf queuing class.
        """
        return self.__qdisc

    def set_qdisc(self, qdisc: 'QDisc') -> None:
        """Set the :class:`QDisc` under with this queuing class
        """
        n_children = self.get_child_count()
        if n_children != 0:
            # Setting the qdisc in the presence of children is not supposed
            # to work (in the kernel).
            _logger.warning(
                "%s: %s: set qdisc to '%s' with %d child class(es) present",
                    self.set_qdisc.__qualname__, self, qdisc, n_children)
        self.__qdisc = qdisc

    def _add_child_class(self, qclass: 'QClass') -> None:
        """Add ``qclass`` as a child of this :class:`QClass`

        When this method is invoked, the class **has already been created**
        inside the kernel.
        """
        if self.__qdisc is not None:
            _logger.warning(
                "%s: %s: attempt to add child class with qdisc '%s' present",
                    self._add_child_class.__qualname__, self, self.__qdisc)
        super()._add_child_class(qclass)

    def dump(self, outfile: TextIO, level: int,
                qclass_map: Optional[Mapping[Handle, 'QClass']] =None):
        """Recursively dump this :class:`QClass` to ``outfile``.

        The ``qclass_map``, if present, is used to determine the
        destination :class:`QClass` objects of traffic filters.
        """
        if qclass_map is None:
            qclass_map = {}
        super().dump(outfile, level, qclass_map)
        if self.__qdisc:
            self.__qdisc.dump(outfile, level+1, qclass_map)

    def __eq__(self, other):
        return (isinstance(other, QClass) and
                self.get_handle() == other.get_handle())

    def __ne__(self, other):
        return not self.__eq__(other)


class QDisc(QNode):
    """Base class for all queueing discipline classes
    """
    # pylint: disable=useless-super-delegation
    #
    # The reason for defining __init__ is to avoid the use of the
    # parent's doc string in the Sphinx documentation.
    def __init__(self, handle: Handle, parent_handle: Optional[Handle]):
        """
        :param handle: :class:`Handle` of this :class:`QDisc`
        :param parent_handle: :class:`Handle` of the parent of this
            :class:`QDisc` (if ``None``, this is a root :class:`QDisc`)
        """
        super().__init__(handle, parent_handle)

    def __str__(self):
        return f'QDisc({self.get_handle()})'

    def _instantiate_qdisc(self, config) -> None:
        """Invoke the **tc(8)** command to create the queuing discipline
        described by this object.

        :param config: a :class:`QDiscConfig` object
        """
        cmd = ['tc', 'qdisc', 'add', 'dev', config.get_interface()]
        if self.is_ingress():
            cmd.append('ingress')
        else:
            if self.is_root():
                cmd.append('root')
            else:
                cmd.extend(['parent', str(self.get_parent_handle())])
            cmd.extend(['handle', str(self.get_handle())])
            # Derived Python class provides the qdisc-specific arguments
            cmd.extend(self.qdisc_creation_args())
        self._instantiate('qdisc', cmd, config)

    def _uninstantiate_qdisc(self, config) -> None:
        """Invoke the **tc(8)** command to delete the queuing discipline
        described by this object.

        :param config: a :class:`QDiscConfig` object
        """
        cmd = ['tc', 'qdisc', 'del', 'dev', config.get_interface()]
        if self.is_ingress():
            cmd.append('ingress')
        else:
            if self.is_root():
                cmd.append('root')
            else:
                cmd.extend(['handle', str(self.get_handle())])
        self._uninstantiate('qdisc', cmd, config)

    def qdisc_creation_args(self) -> List[str]:
        """Returns the qdisc-specific arguments passed to **tc(8)**
        to create the particular qdisc

        It must be implemented by the derived Python class.
        """
        raise NotImplementedError

    def is_root(self) -> bool:
        """Returns ``True`` if this is a root :class:`QDisc`
        """
        return self.get_parent_handle() is None

    def is_default(self) -> bool:
        """Returns ``True`` if this :class:`QDisc` is the default qdisc used
        by the kernel.
        """
        return self.get_handle().major == 0

    @staticmethod
    def is_ingress() -> bool:
        """Returns ``True`` if this :class:`QDisc` is the ingress qdisc
        """
        return False

    def get_description(self) -> str:
        """Return a string that *fully* describes this :class:`QDisc`
        """
        retval = str(self)
        if self.is_root():
            retval += ' root'
        elif self.is_ingress():
            retval += ' ingress'
        else:
            retval += f' parent {self.get_parent_handle()}'
        return retval

    def dump(self, outfile: TextIO, level=0,
                qclass_map: Optional[Mapping[Handle, 'QClass']] =None):
        """Recursively dump this :class:`Qdisc` to ``outfile``.

        The ``qclass_map``, if present, is used to determine the
        destination :class:`QClass` objects of traffic filters.
        """
        if qclass_map is None:
            qclass_map = {}
        super().dump(outfile, level, qclass_map)
