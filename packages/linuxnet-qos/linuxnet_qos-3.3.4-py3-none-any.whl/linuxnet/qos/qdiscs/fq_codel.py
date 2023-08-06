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

"""This module provides access to the Fair Queuing (FQ) with
Controlled Delay (fq_codel) queueing discipline
"""

import re

from typing import List, Optional, TextIO

from ..deps import get_logger
from ..exceptions import TcParsingError
from ..handle import Handle
from ..tcunit import datastr2int, timestr2float, unitstr2num
from ..parsers import QDiscParser

from .qdisc import QDisc, QStats

_logger = get_logger("linuxnet.qos.qdiscs.fq_codel")


class FQCoDelQDiscStats(QStats):
    """FQCoDelQDisc stats
    """

    __LINE4_REGEX_PROG = re.compile(
                r"maxpacket (\d+) drop_overlimit (\d+) "
                r"new_flow_count (\d+) ecn_mark (\d+)")
    __LINE5_REGEX_PROG = re.compile(
            r"new_flows_len (-)?(\d+) old_flows_len (\d+)")

    def __init__(self):
        super().__init__()
        self.__maxpacket = 0
        self.__drop_overlimit = 0
        self.__new_flow_count = 0
        self.__ecn_mark = 0
        self.__new_flows_len = 0
        self.__old_flows_len = 0

    @property
    def maxpacket(self) -> int:
        """Size of largest packet seen
        """
        return self.__maxpacket

    @property
    def drop_overlimit(self) -> int:
        """Number of packets dropped because the queue was full.
        """
        return self.__drop_overlimit

    @property
    def new_flow_count(self) -> int:
        """Returns number of times a new flow was identified.
        """
        return self.__new_flow_count

    @property
    def ecn_packets(self) -> int:
        """Number of packets that were ECN marked (instead of dropped)
        """
        return self.__ecn_mark

    @property
    def new_flows_len(self) -> int:
        """Number of new flows.

        This value is not a statistic; it reflects the qdisc state at
        the time the stats were obtained.
        """
        return self.__new_flows_len

    @property
    def old_flows_len(self) -> int:
        """Number of old flows.

        This value is not a statistic; it reflects the qdisc state at
        the time the stats were obtained.
        """
        return self.__old_flows_len

    def __parse_fourth_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 4th line
        of ``tc qdisc ls`` output
        """
        # The line looks like this:
        #
        #    maxpacket 98 drop_overlimit 0 new_flow_count 5 ecn_mark 0
        #
        match = self.__LINE4_REGEX_PROG.match(line.strip())
        if match is None:
            _logger.warning("4th line not parsable: %s", line)
            return False
        self.__maxpacket = int(match.group(1))
        self.__drop_overlimit = int(match.group(2))
        self.__new_flow_count = int(match.group(3))
        self.__ecn_mark = int(match.group(4))
        return True

    def __parse_fifth_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 5th line
        of ``tc qdisc ls`` output
        """
        # The line looks like this:
        #
        #    new_flows_len 0 old_flows_len 0
        #
        match = self.__LINE5_REGEX_PROG.match(line.strip())
        if match is None:
            _logger.warning("5th line not parsable: %s", line)
            return False
        self.__new_flows_len = int(match.group(2))
        if match.group(1):
            self.__new_flows_len = -self.__new_flows_len
        self.__old_flows_len = int(match.group(3))
        return True

    def init_from_output(self, line_group_iter: 'LineGroupIterator') -> bool:
        """This method is used when parsing the output of ``tc -s qdisc ls``
        to extract statistics information.
        The iterator returns the lines of the output of ``tc -s qdisc ls``
        for a single queuing class.

        :meta private:
        """
        #
        # The first line of the output has already been consumed,
        # and the 2nd line is the next to be returned.
        # Parent class will consume the 2nd and 3rd line
        #
        if not super().init_from_output(line_group_iter):
            return False
        try:
            line = next(line_group_iter)
            if not self.__parse_fourth_line(line):
                return False
            line = next(line_group_iter)
            if not self.__parse_fifth_line(line):
                return False
        except StopIteration:
            return False
        except ValueError as valerr:
            _logger.warning("bad value in stats line: %s (line=%s)",
                                valerr, line)
            return False
        return True

    def dump(self, outfile: TextIO, width: Optional[int] =None) -> None:
        """Dump stats to ``outfile``.
        There is one stat per line output. Each line has the format::

            header: value

        The ``header:`` part occupies at least ``width`` characters.
        """
        super().dump(outfile, width)
        width = width or self.HEADER_WIDTH
        print(f"{'Maxpacket:':{width}} {self.__maxpacket}", file=outfile)
        print(f"{'Drop-overlimits':{width}} {self.__drop_overlimit}",
                        file=outfile)
        print(f"{'New-flows:':{width}} {self.__new_flow_count}", file=outfile)
        print(f"{'ECN-mark:':{width}} {self.__ecn_mark}", file=outfile)
        print(f"{'New-flows-len:':{width}} {self.__new_flows_len}",
                file=outfile)
        print(f"{'Old-flows-len:':{width}} {self.__old_flows_len}",
                file=outfile)


class FQCoDelQDisc(QDisc):      # pylint: disable=too-many-instance-attributes
    """This class provides access to the Fair Queuing (FQ) with
    Controlled Delay (fq_codel) queueing discipline (see **tc-fq_codel(8)**)
    """

    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                        *,
                        limit: Optional[int], flows: Optional[int],
                        quantum: Optional[int], target: Optional[float],
                        interval: Optional[float],
                        memory_limit: Optional[int], ecn: Optional[bool]):
        """
        :param qdisc_handle: handle of this :class:`FQCoDelQDisc`
        :param parent_handle: handle of parent, ``None`` if this is a
            root queuing discipline
        :param limit: as documented in **tc-fq_codel(8)**
        :param flows: as documented in **tc-fq_codel(8)**
        :param quantum: as documented in **tc-fq_codel(8)**
        :param target: as documented in **tc-fq_codel(8)**
        :param interval: as documented in **tc-fq_codel(8)**
        :param memory_limit: as documented in **tc-fq_codel(8)**
        :param ecn: as documented in **tc-fq_codel(8)**
        """
        super().__init__(qdisc_handle, parent_handle)
        self.__limit = limit
        self.__flows = flows
        self.__quantum = quantum
        self.__target = target                  # in ms
        self.__interval = interval              # in ms
        self.__memory_limit = memory_limit      # in bytes
        self.__ecn: bool = ecn
        self.__drop_batch = None
        self.__stats = None

    def __str__(self):
        return f"FQCoDelQDisc({self.get_handle()})"

    def get_packet_limit(self) -> Optional[int]:
        """Returns packet limit
        """
        return self.__limit

    def get_flows(self) -> Optional[int]:
        """Returns number of flows
        """
        return self.__flows

    def get_quantum(self) -> Optional[int]:
        """Returns quantum
        """
        return self.__quantum

    def get_memory_limit(self) -> Optional[int]:
        """Returns memory limit in bytes
        """
        return self.__memory_limit

    def get_queue_delay_target(self) -> Optional[int]:
        """Returns target for the minimum queue delay (in ms)
        """
        return self.__target

    def get_queue_delay_interval(self) -> Optional[int]:
        """Returns time interval in which to measure queue delay (in ms)
        """
        return self.__interval

    def get_ecn(self) -> Optional[bool]:
        """Returns the ``ecn`` value
        """
        return self.__ecn

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by the **tc(8)** command to create
        a ``fq_codel`` qdisc
        """
        args = ['fq_codel']
        if self.__limit is not None:
            args.extend(['limit', f'{self.__limit}p'])
        if self.__flows is not None:
            args.extend(['flows', f'{self.__limit:d}'])
        if self.__quantum is not None:
            args.extend(['quantum', f'{self.__quantum:d}'])
        if self.__target is not None:
            args.extend(['target', f'{self.__target:.1f}ms'])
        if self.__interval is not None:
            args.extend(['interval', f'{self.__interval:.1f}ms'])
        if self.__memory_limit is not None:
            args.extend(['memory_limit', f'{self.__memory_limit:d}b'])
        if self.__ecn is not None:
            if self.__ecn:
                args.append('ecn')
            else:
                args.append('noecn')
        return args

    def get_description(self) -> str:
        """Returns a string describing the qdisc and its attributes
        """
        retval = super().get_description()
        if self.__limit is not None:
            retval += f' {self.__limit}p'
        if self.__flows is not None:
            retval += f' {self.__flows}'
        if self.__quantum is not None:
            retval += f' {self.__quantum}'
        if self.__target is not None:
            retval += f' {self.__target:.1f}ms'
        if self.__interval is not None:
            retval += f' {self.__interval:.1f}ms'
        if self.__memory_limit is not None:
            retval += f' {self.__memory_limit}b'
        if self.__ecn is not None:
            if self.__ecn:
                retval += ' ecn'
            else:
                retval += ' noecn'
        if self.__drop_batch is not None:
            retval += f' {self.__drop_batch}'
        return retval

    def get_stats(self) -> Optional[FQCoDelQDiscStats]:
        """Returns qdisc stats (an :class:`FQCoDelQDiscStats` instance) or
        ``None`` if no stats are available.
        """
        return self.__stats

    def _parse_stats(self, line_group_iter) -> None:
        """Parse queuing stats.
        """
        stats = FQCoDelQDiscStats()
        if stats.init_from_output(line_group_iter):
            self.__stats = stats

    def _set_drop_batch(self, drop_batch: int) -> None:
        """Set the drop_batch attribute.
        This is a private method used only by the parsing code because
        this fq_codel parameter is not documented in tc-fq_codel(8)
        """
        self.__drop_batch = drop_batch

    # pylint: disable=too-many-branches
    @classmethod
    def parse(cls, qdisc_output) -> 'FQCoDelQDisc':
        """Create a :class:`FQCoDelQDisc` object from the output of the
        **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        # pylint: disable=line-too-long
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc fq_codel 0: parent :2 limit 10240p flows 1024 quantum 1514 target 5.0ms interval 100.0ms memory_limit 32Mb ecn drop_batch 64
        #
        limit = None
        flows = None
        quantum = None
        target = None
        interval = None
        memory_limit = None
        ecn = None
        drop_batch = None
        try:
            for field in field_iter:
                if field == 'limit':
                    limit = unitstr2num(next(field_iter), 'p')
                elif field == 'flows':
                    flows = int(next(field_iter))
                elif field == 'quantum':
                    quantum = int(next(field_iter))
                elif field == 'target':
                    target = timestr2float(next(field_iter))
                elif field == 'interval':
                    interval = timestr2float(next(field_iter))
                elif field == 'memory_limit':
                    memory_limit = datastr2int(next(field_iter))
                elif field == 'ecn':
                    ecn = True
                elif field == 'noecn':
                    ecn = False
                elif field == 'drop_batch':
                    drop_batch = int(next(field_iter))
                else:
                    raise TcParsingError(f"unknown field '{field}'")
        except ValueError as valerr:
            raise TcParsingError(f"bad value for field {field}") from valerr
        qdisc = FQCoDelQDisc(
                        qdisc_output.get_handle(),
                        qdisc_output.get_parent_handle(),
                        limit=limit, flows=flows, target=target,
                        quantum=quantum, interval=interval,
                        memory_limit=memory_limit, ecn=ecn)
        if drop_batch is not None:
            qdisc._set_drop_batch(drop_batch)
        return qdisc
    # pylint: enable=too-many-branches


QDiscParser.register_qdisc('fq_codel', FQCoDelQDisc)
