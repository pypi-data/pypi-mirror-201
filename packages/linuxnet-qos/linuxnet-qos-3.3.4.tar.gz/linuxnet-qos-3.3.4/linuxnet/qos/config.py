# Copyright (c) 2021, 2022, Panagiotis Tsirigotis

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

"""This module provides the ability to read an existing
qdisc configuration
"""

import errno
import subprocess
import sys

from typing import List, Mapping, Optional, Set

from .deps import get_logger
from .exceptions import TcConfigError, TcExecutionError, TcError

from .handle import Handle
from .qdiscs.qdisc import QDisc, QClass, QNode
from .qdiscs.ingress import IngressQDisc
from .util import run_command, run_subprocess

from .parsers import TrafficFilterParser, QClassParser, QDiscParser

_logger = get_logger("linuxnet.qos.config")


class QDiscConfig:      # pylint: disable=too-many-public-methods
    """Objects of this class track and manage the queuing discipline
    configuration of a particular interface. The object internal state can
    reflect the configuration inside the kernel by reading the kernel
    configuration using the **tc(8)** command. This can optionally be
    performed upon object initialization.

    :class:`QDiscConfig` also provides the methods for adding/removing
    queueing disciplines, queuing classes, and traffic filters from
    the kernel.

    :class:`QDiscConfig` provides methods to delete the entire queuing
    discipline configuration from the kernel. After successful invocation
    of such a method, the internal state will not reflect the kernel
    configuration because the kernel automatically installs a default
    queuing discipline, and the new kernel configuration will need
    to be read again.
    """

    # The QDiscConfig is responsible for maintaining the parent/child
    # relationships between qdiscs and qclasses as qdiscs/qclasses
    # are added/removed. This is handled by the
    # {create,delete}_{qdisc,qclass} methods.
    #
    # The kernel behavior wrt qdisc/qclass creation/deletion is as follows:
    #
    # 1. Add a qdisc to a qclass with child qclasses:
    #           not-allowed
    # 2. Add a qclass to qclass with a child qdisc:
    #           allowed, qdisc deleted
    # 3. Delete qclass with child qclasses:
    #           not-allowed
    # 4. Delete qclass with child qdisc:
    #           allowed, deletes qdisc and everything below it
    # 5. Delete root qdisc by handle:
    #           not-allowed
    # 6. Add root qdisc when existing root qdisc is not the default one
    #           not-allowed
    # 7. Delete the child qdisc of a qclass
    #           not-allowed
    #
    # The above was determined via experimentation using the tc command
    # of iproute2-ss091226 on CentOS-6.10. The HTB qdisc was used (it is
    # possible that other qdisc's may have different semantics).

    # User-assigned major handle numbers should be in the
    # range 1-0x7fff. We use major numbers in the range
    # 0x7d00-0x7fff to replace tc-reported numbers that
    # collide with other existing numbers. This usually
    # happens with handle 0.
    __QDISC_REMAP_MAJOR = 0x7d00
    _qdisc_remap_major = __QDISC_REMAP_MAJOR

    def __init__(self, interface: str, runner=None,
                                read_interface_config=True,
                                allow_parsing_errors=False):
        """
        :param interface: network interface name
        :param runner: optional callable used to invoke **tc(8)**
        :param read_interface_config: if ``True``, read and parse
            the existing queuing discipline configuration of the interface
        :param allow_parsing_errors: if ``True``, count the parsing
            errors instead of raising an exception when processing
            the existing configuration

        Raises a :class:`TcParsingError` if unable to parse the
        existing configuration.

        Raises a :class:`TcConfigError` if a logical error is encountered
        when processing the existing configuration.
        """
        self.__interface = interface
        self.__runner = runner or run_subprocess
        # The __qdisc_map/__qclass_map dictionaries maintain all queueing
        # disciplines/classes of an interface. The goal is to keep
        # them in-sync with the in-kernel state.
        # Key: qdisc/qclass handle
        # Value: qdisc/qclass
        self.__qdisc_map = {}
        self.__qclass_map = {}
        self.__root_qdisc = None
        self.__ingress_qdisc = None
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        if read_interface_config:
            self.read_interface_config(allow_parsing_errors)

    def get_root_qdisc(self) -> Optional[QDisc]:
        """Returns the root queuing discipline, or ``None`` if the root
        queuing discipline has not been discovered yet.
        """
        return self.__root_qdisc

    def get_ingress_qdisc(self) -> Optional[QDisc]:
        """Returns the ingress queuing discipline, or ``None`` if there
        is no ingress queuing discipline (or if the interface configuration
        has not been read).
        """
        return self.__ingress_qdisc

    def get_interface(self) -> str:
        """Returns the interface associated with this configuration
        """
        return self.__interface

    def _get_existing_node(self, handle: Handle) -> QNode:
        """Returns the node with the specified handle. Thia may be
        either a :class:`QClass` or a :class:`QDisc`.

        Raises :class:`TcError` if the node does not exist
        """
        node = self.__qclass_map.get(handle)
        if node is None:
            node = self.__qdisc_map.get(handle)
            if node is None:
                raise TcError( f'no qdisc/qclass with handle {handle}')
        return node

    def get_qdisc(self, handle: Handle) -> Optional[QDisc]:
        """Returns the :class:`QDisc` with the specified ``handle``,
        or ``None`` if there is no such qdisc.
        """
        return self.__qdisc_map.get(handle)

    def get_qclass(self, handle: Handle) -> Optional[QClass]:
        """Returns the :class:`QClass` with the specified ``handle``,
        or ``None`` if there is no such qclass.
        """
        return self.__qclass_map.get(handle)

    def get_qdisc_map(self) -> Mapping[Handle, QDisc]:
        """Returns the qdisc map

        :meta private:
        """
        return self.__qdisc_map

    def get_qclass_map(self) -> Mapping[Handle, QClass]:
        """Returns the qclass map

        :meta private:
        """
        return self.__qclass_map

    def tc_run(self, cmd: List[str], operation: str):
        """Execute the (tc) command in ``cmd``

        :param cmd: tc command to execute
        :param operation: description of what the command is supposed to do

        :meta private:
        """
        run_command(self.__runner, cmd, operation)

    def read_interface_config(self,
                allow_parsing_errors: Optional[bool] =None) -> bool:
        """Read the queuing discipling configuration of the interface
        and initialize our internal state. This can only be performed once.

        :param allow_parsing_errors: if ``False``, a :exc:`TcParsingError`
            will be raised upon a parsing error; if ``True``,  no
            :exc:`TcParsingError` will be raised; if ``None``, the behavior
            depends on the value of the ``allow_parsing_errors``
            parameter when this :class:`QDiscConfig` instance was created

        :rtype: ``True`` if no parsing error is encountered; ``False``
            if ``allow_parsing_errors`` is ``True`` and there are
            parsing errors.

        Raises a :class:`TcConfigError` if the interface configuration has
        already been discovered.
        """
        if self.__root_qdisc is not None:
            raise TcConfigError(
                f'already read configuration of {self.__interface}')
        if allow_parsing_errors is not None:
            self.__allow_parsing_errors = allow_parsing_errors
        self.__qdisc_map = self.__read_qdisc_config()
        self.__qclass_map = self.__read_qclass_config()
        self.__root_qdisc = self.__find_root_qdisc()
        self.__create_qdisc_tree()
        return self.get_error_count() == 0

    def get_error_count(self) -> int:
        """Returns number of parsing errors
        """
        return self.__parsing_errors

    def __prune_children(self, node) -> None:
        """Prune all qclass children of this node
        """
        for qclass in node.get_child_iter():
            self.__prune_qclass(qclass)

    def __prune_qclass(self, qclass: QClass):
        """Prune the qdisc and all classes below
        """
        qdisc = qclass.get_qdisc()
        if qdisc is not None:
            self.__prune_qdisc(qdisc)
        else:
            self.__prune_children(qclass)
        if self.__qclass_map.pop(qclass.get_handle(), None) is None:
            _logger.warning("pruned unknown qclass %s", qclass)

    def __prune_qdisc(self, qdisc: QDisc):
        """Prune the qdisc and all classes below
        """
        self.__prune_children(qdisc)
        if self.__qdisc_map.pop(qdisc.get_handle(), None) is None:
            _logger.warning("pruned unknown qdisc %s", qdisc)

    def create_qdisc(self, qdisc: QDisc) -> None:
        """Create the queuing discipline ``qdisc`` inside the kernel.
        """
        parent = None
        if not qdisc.is_root():
            parent = self._get_existing_node(qdisc.get_parent_handle())
        qdisc._instantiate_qdisc(config=self)
        self.__qdisc_map[qdisc.get_handle()] = qdisc
        if qdisc.is_root():
            old_root_qdisc = self.__root_qdisc
            if old_root_qdisc is not None:
                self.__prune_qdisc(old_root_qdisc)
            self.__root_qdisc = qdisc
        else:
            parent.set_qdisc(qdisc)

    def delete_qdisc(self, qdisc: QDisc) -> None:
        """Delete the queuing discipline ``qdisc`` from the kernel.

        If ``qdisc`` is the root queuing discipline, the entire configuration
        will be deleted. In that case, a call to :meth:`read_interface_config`
        will be needed to rediscover the new root queuing discipline.
        """
        if qdisc.is_root():
            self.delete_config()
            return
        qdisc._uninstantiate_qdisc(config=self)
        # Experimentation shows that the above call will fail.
        # It appears that it is not be possible to delete an existing
        # qdisc. What is possible is to delete the parent class of the
        # qdisc which will result in the deletion of the qdisc
        self.__prune_qdisc(qdisc)

    def create_ingress_qdisc(self) -> QDisc:
        """Create the ingress queuing discipline.

        :rtype: the ingress queuing discipline
        """
        if self.__ingress_qdisc is not None:
            raise TcError('ingress qdisc exists')
        qdisc = IngressQDisc()
        qdisc._instantiate_qdisc(config=self)
        self.__qdisc_map[qdisc.get_handle()] = qdisc
        self.__ingress_qdisc = qdisc
        return qdisc

    def delete_ingress_qdisc(self) -> None:
        """Delete the ingress queuing discipline.
        """
        if self.__ingress_qdisc is None:
            return
        self.__ingress_qdisc._uninstantiate_qdisc(config=self)
        self.__ingress_qdisc = None

    def create_qclass(self, qclass: QClass) -> None:
        """Create the queuing class ``qclass`` inside the kernel.
        """
        parent = self._get_existing_node(qclass.get_parent_handle())
        if isinstance(parent, QClass):
            # Experimentation has shown that adding a qclass as a child
            # of a qclass that has a qdisc results in the deletion of
            # the qdisc; we choose not to support this.
            child_qdisc = parent.get_qdisc()
            if child_qdisc is not None:
                _logger.error(
                    "%s: creating qclass %s as a child of qclass %s "
                    "not allowed; latter has qdisc %s",
                        self.create_qclass.__qualname__,
                        qclass, parent, child_qdisc)
                raise TcError('parent class has qdisc')
        qclass._instantiate_qclass(config=self)
        self.__qclass_map[qclass.get_handle()] = qclass
        parent._add_child_class(qclass)   # pylint: disable=protected-access

    def delete_qclass(self, qclass: QClass) -> None:
        """Delete the queuing class ``qclass`` from the kernel.

        ``qclass`` should have no :class:`QClass` children, or the
        kernel will fail the operation.

        If the queuing class has a queuing discipline, that queuing
        discipline will also be recursively deleted (this is the kernel
        behavior).
        """
        parent = self._get_existing_node(qclass.get_parent_handle())
        qclass._uninstantiate_qclass(config=self)
        self.__qclass_map.pop(qclass.get_handle(), None)
        parent._remove_child_class(qclass)  # pylint: disable=protected-access
        qdisc = qclass.get_qdisc()
        if qdisc is not None:
            self.__prune_qdisc(qdisc)

    def create_filter(self, traffic_filter, parent_handle: Handle) -> None:
        """Create the specified traffic filter inside the kernel.

        :param traffic_filter: :class:`TrafficFilter` object describing
            the filter to create
        :param parent_handle: handle of the owner
            :class:`QDisc`/:class:`QClass` of the filter
        """
        node = self._get_existing_node(parent_handle)
        node.create_filter(traffic_filter)

    def delete_filter(self, traffic_filter, parent_handle):
        """Delete the specified traffic filter from the kernel.

        :param traffic_filter: :class:`TrafficFilter` object describing
            the filter to delete; it must have a priority assigned to it
        :param parent_handle: handle of the owner
            :class:`QDisc`/:class:`QClass` of the filter

        Raises a :class:`TcError` if ``traffic_filter`` has no priority.
        """
        node = self._get_existing_node(parent_handle)
        node.delete_filter(traffic_filter)

    def retrieve_filters(self, qnode: QNode) -> List['TrafficFilter']:
        """Returns a list of :class:`TrafficFilter` objects.

        :param qnode: a :class:`QDisc` or :class:`QClass` object

        This method can be used to retrieve the filters of any
        queuing discipline or class using an actual :class:`QDisc` or
        :class:`QClass` object (not one of a subclass).
        """
        # NB: pretty output should be avoided as tc may not show
        #     all selectors (observed with the tc command in iproute2-ss091226)
        # Also, we avoid using pretty output to make filter parsing easier
        cmd = ['tc', 'filter', 'ls', 'dev', self.__interface,
                        'parent', str(qnode.get_handle())]
        proc = self.__runner(cmd, check=True, universal_newlines=True,
                                stdout=subprocess.PIPE, execute_always=True)
        parser = TrafficFilterParser(self.__allow_parsing_errors)
        if proc.stdout:
            output_lines = proc.stdout.split('\n')
        else:
            output_lines = []
        parser.parse_output(output_lines, qnode)
        self.__parsing_errors += parser.get_error_count()
        return parser.get_filter_list()

    def __reset_config(self):
        """Set attributes to their initial values
        """
        self.__root_qdisc = None
        self.__qdisc_map.clear()
        self.__qclass_map.clear()
        if self.__parsing_errors is not None:
            self.__parsing_errors = 0

    def delete_config(self):
        """Delete the existing configuration.

        This method is a no-op before reading the interface qdisc
        configuration.

        Since the kernel installs a default root queuing discipline when
        the queuing configuration is deleted, a call to
        :meth:`read_interface_config` will be needed to rediscover
        the new root queuing discipline.
        """
        root_qdisc = self.__root_qdisc
        if root_qdisc is None:
            return
        if not root_qdisc.is_default():
            # Deleting the root qdisc will remove the entire configuration
            # from the kernel
            root_qdisc._uninstantiate_qdisc(config=self)
        self.__reset_config()

    def delete_root_qdisc(self):
        """Delete the interface root qdisc.

        This method can be used even without reading the interface
        qdisc configuration.
        """
        cmd = ['tc', 'qdisc', 'del', 'dev', self.__interface, 'root']
        try:
            # To avoid polluting the log, we skip logging tc failures
            # in run_command, since in the majority of cases they are
            # caused by the lack of the absence of a QoS configuration.
            run_command(self.__runner, cmd, 'root qdisc deletion',
                                log_process_error=False)
        except TcExecutionError as tc_err:
            if tc_err.get_rtnetlink_errno() == errno.ENOENT:
                pass    # no qdisc present
            elif 'qdisc with handle of zero' in tc_err.get_error_message():
                # Happens when trying to delete the default root qdisc
                pass
            else:
                _logger.exception("%s: command failed: %s",
                        self.delete_root_qdisc.__qualname__,
                        ' '.join(cmd))
                raise
        self.__reset_config()

    def dump(self, outfile=sys.stdout):
        """Dump the queueing tree to ``outfile``
        """
        if not self.__root_qdisc:
            return
        self.__root_qdisc.dump(outfile, 0, qclass_map=self.__qclass_map)

    def __remap_handle(self, handle) -> Handle:
        """Remap the major number of the handle
        """
        new_major = self._qdisc_remap_major
        self._qdisc_remap_major += 1
        new_handle = Handle(new_major, handle.minor)
        _logger.info("Qdisc handle %s already present; remapping it to %s",
                                handle, new_handle)
        return new_handle

    def __read_qdisc_config(self) -> Mapping[Handle, QDisc]:
        """Get the qdisc info via **tc(8)** and return it as a dictionary
        """
        cmd = ['tc', '-s', 'qdisc', 'ls', 'dev', self.__interface]
        proc = self.__runner(cmd, check=True, universal_newlines=True,
                            stdout=subprocess.PIPE, execute_always=True)
        qdisc_map = {}
        parser = QDiscParser(self.__allow_parsing_errors)
        parser.parse_output(proc.stdout.split('\n'))
        self.__parsing_errors += parser.get_error_count()
        for qdisc in parser.get_qdisc_list():
            qdisc._set_config(config=self)
            handle = qdisc.get_handle()
            remap_needed = False
            while handle in qdisc_map:
                handle = self.__remap_handle(handle)
                remap_needed = True
            if remap_needed:
                qdisc._replace_handle(handle)
            qdisc_map[qdisc.get_handle()] = qdisc
            if qdisc.is_ingress():
                if self.__ingress_qdisc is None:
                    self.__ingress_qdisc = qdisc
                else:
                    _logger.warning(
                        "found another ingress qdisc; original=%s, new=%s",
                                self.__ingress_qdisc, qdisc)
        return qdisc_map

    def __read_qclass_config(self) -> Mapping[Handle, QClass]:
        """Get the class info via tc(8) and populate __qclass_map
        """
        cmd = ['tc', '-s', 'class', 'ls', 'dev', self.__interface]
        proc = self.__runner(cmd, check=True, universal_newlines=True,
                            stdout=subprocess.PIPE, execute_always=True)
        qclass_map = {}
        parser = QClassParser(self.__allow_parsing_errors)
        parser.parse_output(proc.stdout.split('\n'))
        self.__parsing_errors += parser.get_error_count()
        for qclass in parser.get_qclass_list():
            qclass._set_config(config=self)
            qclass_map[qclass.get_handle()] = qclass
        return qclass_map

    def __find_root_qdisc(self) -> QDisc:
        """Find and return the root qdisc.
        There must be exactly one.
        """
        root_qdisc = None
        for qdisc in self.__qdisc_map.values():
            if qdisc.is_root():
                if root_qdisc is not None:
                    raise TcConfigError(f'duplicate root qdisc {qdisc}')
                root_qdisc = qdisc
        if root_qdisc is None:
            _logger.error("%s: unable to find root qdisc: n_qdiscs=%d",
                                self.__find_root_qdisc.__qualname__,
                                len(self.__qdisc_map))
            raise TcConfigError('unable to find root qdisc')
        return root_qdisc

    def __create_qdisc_tree(self) -> None:
        """Create the parent-child relationships bewteen qdisc's and classes.
        """
        # Find the parents of all queuing classes
        for qclass in self.__qclass_map.values():
            parent_handle = qclass.get_parent_handle()
            if parent_handle.minor == 0:    # parent is a qdisc
                parent_qdisc = self.__qdisc_map.get(parent_handle)
                if parent_qdisc is None:
                    _logger.error(
                        "%s: missing qdisc parent of class '%s': "
                        "qdisc-parent-handle='%s'",
                            self.__create_qdisc_tree.__qualname__,
                            qclass,
                            parent_handle)
                    raise TcError(f'Unable to find qdisc {parent_handle}')
                # pylint: disable=protected-access
                parent_qdisc._add_child_class(qclass)
                # pylint: enable=protected-access
            else:
                parent_class = self.__qclass_map.get(parent_handle)
                if parent_class is None:
                    _logger.error(
                        "%s: missing class parent of class '%s': "
                        "class-parent-handle='%s'",
                            self.__create_qdisc_tree.__qualname__,
                            qclass,
                            parent_handle)
                    raise TcError(f'Unable to find class {parent_handle}')
                # pylint: disable=protected-access
                parent_class._add_child_class(qclass)
                # pylint: enable=protected-access
        # Find the parents of all qdisc's
        for qdisc in self.__qdisc_map.values():
            parent_handle = qdisc.get_parent_handle()
            if qdisc.is_root() or qdisc.is_ingress():
                continue
            parent_class = self.__qclass_map.get(parent_handle)
            if parent_class is None:
                _logger.error(
                    "%s: missing class parent of qdisc '%s': "
                    "class-parent-handle='%s'",
                        self.__create_qdisc_tree.__qualname__,
                        qdisc,
                        parent_handle)
                raise TcConfigError(
                            f'Unable to find class {parent_handle} '
                            f'when looking for parent of {qdisc}')
            if not parent_class.is_leaf():
                _logger.error(
                    "%s: parent class '%s' of qdisc '%s' is not a leaf class",
                    self.__create_qdisc_tree.__qualname__,
                    parent_class,
                    qdisc)
                raise TcConfigError(
                    f'non-leaf class {parent_class} is a parent '
                    f'of qdisc {qdisc}')
            parent_class.set_qdisc(qdisc)


class QDiscConfigImporter:
    """Helper class for importing an existing qdisc configuration.
    """
    def __init__(self, qdisc_config: QDiscConfig):
        """
        """
        self.__config = qdisc_config
        self.__qdisc_map = qdisc_config.get_qdisc_map()
        self.__qclass_map = qdisc_config.get_qclass_map()
        # Contains Handle's of imported QDisc's
        self.__imported_qdiscs = set()
        # Contains Handle's of imported QClass'es
        self.__imported_qclasses = set()

    def __str__(self):
        return f'QDiscConfigImporter({self.__config.get_interface()})'

    def __verify_empty(self, descr: str, handle_set: Set[Handle]) -> None:
        """Raise a TcError if handle_set is not empty
        """
        if handle_set:
            handles_msg = ', '.join([str(h) for h in handle_set])
            _logger.error("%s: unreferenced %s: %s", self, descr, handles_msg)
            raise TcError(f'unreferenced {descr}: {handles_msg}')

    def verify_import(self) -> None:
        """Verify that all qdiscs/qclasses were imported
        """
        remain = set(self.__qdisc_map.keys()) - self.__imported_qdiscs
        self.__verify_empty('qdiscs', remain)
        remain = set(self.__qclass_map.keys()) - self.__imported_qclasses
        self.__verify_empty('qclasses', remain)

    def import_qdisc(self, qdisc: QDisc) -> None:
        """Mark the specified qdisc as imported
        """
        handle = qdisc.get_handle()
        if handle in self.__imported_qdiscs:
            raise TcError(f'internal error: already imported {qdisc}')
        self.__imported_qdiscs.add(handle)
        _logger.info("Imported qdisc %s", handle)

    def import_qclass(self, qclass: QClass) -> None:
        """Mark the specified qclass as imported.
        """
        handle = qclass.get_handle()
        if handle in self.__imported_qclasses:
            raise TcError(f'internal error: already imported {qclass}')
        self.__imported_qclasses.add(handle)
        _logger.info("Imported qclass %s", handle)
