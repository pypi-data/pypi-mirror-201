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

"""This module provides access to the HTB queueing discipline
"""

import re

from typing import List, Optional, TextIO

from ..deps import get_logger
from ..exceptions import TcParsingError, TcBandwidthError
from ..handle import Handle
from ..tcunit import rate2str, bwstr2int, unitstr2num
from ..parsers import QDiscParser, QClassParser

from .qdisc import QDisc, QClass, QStats

_logger = get_logger("linuxnet.qos.qdiscs.htb")


class HTBQClassStats(QStats):
    """HTB-specific class stats (see :class:`QStats` for inherited stats)
    """

    __LINE4_REGEX_PROG = re.compile(
                r"lended: (\d+) borrowed: (\d+) giants: (\d+)")
    # Tokens may be negative
    __LINE5_REGEX_PROG = re.compile(
                r"tokens: (-)?(\d+) ctokens: (\d+)")

    def __init__(self):
        super().__init__()
        self.__lent = 0
        self.__borrowed = 0
        self.__giants = 0
        # tokens/ctokens are measured in packet scheduler ticks;
        # a tick duration is 64nsec.
        # Sending a packet of size P when the rate is R takes T=P/R seconds
        # and consumes T/64 tokens.
        self.__tokens = 0
        # Sending a packet of size P when the ceil is C takes T=C/R seconds
        # and consumes T/64 ctokens.
        self.__ctokens = 0

    @property
    def packets_lent(self) -> int:
        """Number of packets lent.
        """
        return self.__lent

    @property
    def packets_borrowed(self) -> int:
        """Number of packets borrowed.
        """
        return self.__borrowed

    @property
    def overlimits(self) -> int:
        """Number of times a rate limit was exceeded.
        """
        return self.get_overlimits()

    @property
    def giant_packets(self) -> int:
        """Number of packets exceeding interface MTU
        """
        return self.__giants

    @property
    def tokens(self) -> int:
        """Tokens available for transmitting at the guaranteed rate
        (measured in packet scheduler ticks).

        This value is not a statistic; it reflects the class state at
        the time the stats were obtained.
        """
        return self.__tokens

    @property
    def ctokens(self) -> int:
        """Tokens available for transmitting at the maximum (ceil) rate
        (measured in packet scheduler ticks)

        This value is not a statistic; it reflects the class state at
        the time the stats were obtained.
        """
        return self.__ctokens

    def __parse_fourth_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 4th line
        of ``tc class ls`` output
        """
        # The line looks like this:
        #
        #    lended: 12189193 borrowed: 6524195 giants: 0
        #
        match = self.__LINE4_REGEX_PROG.match(line.strip())
        if match is None:
            _logger.warning("4th line not parsable: %s", line)
            return False
        self.__lent = int(match.group(1))
        self.__borrowed = int(match.group(2))
        self.__giants = int(match.group(3))
        return True

    def __parse_fifth_line(self, line: str) -> bool:
        """Initialize attributes from ``line``, which is the 5th line
        of ``tc class ls`` output
        """
        # The line looks like this:
        #
        #    tokens: 4953344 ctokens: 309594
        #
        match = self.__LINE5_REGEX_PROG.match(line.strip())
        if match is None:
            _logger.warning("5th line not parsable: %s", line)
            return False
        self.__tokens = int(match.group(2))
        if match.group(1) is not None:
            self.__tokens = -self.__tokens
        self.__ctokens = int(match.group(3))
        return True

    def init_from_output(self, line_group_iter: 'LineGroupIter') -> bool:
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
        print(f"{'Overlimits:':{width}} {self.__overlimits}", file=outfile)
        print(f"{'Lent:':{width}} {self.__lent}", file=outfile)
        print(f"{'Borrowed:':{width}} {self.__borrowed}", file=outfile)
        print(f"{'Giants:':{width}} {self.__giants}", file=outfile)
        print(f"{'Tokens:':{width}} {self.__tokens}", file=outfile)
        print(f"{'CTokens:':{width}} {self.__ctokens}", file=outfile)


class HTBQClass(QClass):    # pylint: disable=too-many-instance-attributes
    """A class of the HTB qdisc
    """
    def __init__(self,  # pylint: disable=too-many-arguments
                        class_handle: Handle, parent_handle: Handle,
                        *,
                        rate: int, ceil: Optional[int] =None,
                        prio: Optional[int] =None,
                        burst: Optional[int] =None,
                        cburst: Optional[int] =None,
                        quantum: Optional[int] = None,
                        class_name: Optional[str] =None):
        """
        :param class_handle: handle of this :class:`HTBQClass`
        :param parent_handle: handle of parent :class:`HTBQClass` or
            :class:`HTBQDisc`
        :param rate: guaranteed rate (unit: bits/sec)
        :param ceil: max rate (unit: bits/sec)
        :param prio: priority
        :param burst: amount of bytes that can be sent at ``ceil`` speed
        :param cburst: amount of bytes that can be sent at interface speed
        :param quantum: transmission quantum (aka interface packet size)
            in bytes; the kernel computes this from the HTB queuing
            discipline ``r2q`` if not explicitly specified at HTB class
            creation time
        """
        if class_name is None:
            # NB: class handle not included because it is automatically
            #     appended to class name in output (see get_description())
            class_name = "HTBQClass"
        super().__init__(class_handle, parent_handle, class_name=class_name)
        self.__rate = rate
        self.__ceil = ceil if ceil is not None else rate
        # We map None to -1
        self.__prio = prio if prio is not None else -1
        self.__burst = burst
        self.__cburst = cburst
        self.__quantum = quantum
        if self.__rate > self.__ceil:
            _logger.error("%s: %s: rate (%d) > ceil (%d)",
                                self.__init__.__qualname__,
                                self,
                                self.__rate,
                                self.__ceil)
            raise TcBandwidthError(
                        f'{self} has rate {self.__rate} > ceil {self.__ceil}')
        self.__residual_rate = rate
        self.__stats = None

    def __str__(self):
        return f"HTBQClass({self.get_handle()})"

    def get_description(self) -> str:
        """Returns a string describing the class and its attributes
        """
        class_name = self.get_class_name()
        if class_name is None:
            retval = str(self)
        else:
            retval = f'{class_name}({self.get_handle()}) HTB'
        retval += ' rate ' + rate2str(self.__rate)
        if self.__ceil is not None:
            retval += '/' + rate2str(self.__ceil)
        if self.__prio >= 0:
            retval += f' prio {self.__prio}'
        return retval

    def qclass_creation_args(self) -> List[str]:
        """Returns the tc arguments to create this HTB class
        """
        args = ['htb', 'rate', str(self.__rate)]
        if self.__ceil is not None:
            args.extend(['ceil', str(self.__ceil)])
        if self.__prio >= 0:
            args.extend(['prio', str(self.__prio)])
        # For the burst/cburst parameters, if an explicit burst/cburst is
        # not specified, tc defaults to the formula
        #       R / HZ + MTU
        # where
        #  - HZ is the system clock frequency (typical 10ms quantum implies
        #   a frequency of 100 Hz)
        #  - MTU defaults to 1600; it can be changed using the undocumented
        #    'mtu' parameter when adding a htb class via tc
        #  - R is the specified rate/ceil in bytes (i.e. it is divided by 8)
        if self.__burst is not None:
            args.extend(['burst', str(self.__burst)])
        if self.__cburst is not None:
            args.extend(['cburst', str(self.__cburst)])
        if self.__quantum is not None:
            args.extend(['quantum', str(self.__quantum)])
        return args

    def get_priority(self) -> int:
        """Returns the class priority, or -1 if the class
        has no priority specified
        """
        return self.__prio

    def get_rate(self) -> int:
        """Returns the bandwidth guaranteed to this class
        """
        return self.__rate

    def get_ceil(self) -> Optional[int]:
        """Returns the maximum bandwidth that may be consumed
        by this class.
        """
        return self.__ceil

    def get_burst(self) -> Optional[int]:
        """Returns the burst (bytes)
        """
        return self.__burst

    def get_cburst(self) -> Optional[int]:
        """Returns the cburst (bytes)
        """
        return self.__cburst

    def get_quantum(self) -> Optional[int]:
        """Returns the quantum (bytes)
        """
        return self.__quantum

    def get_residual_rate(self) -> int:
        """Returns the residual rate, which is the guaranteed
        bandwidth left at this class after all its children
        have been allocated their guaranteed bandwidth.
        """
        return self.__residual_rate

    def get_stats(self) -> Optional[HTBQClassStats]:
        """Returns class stats (an :class:`HTBQClassStats` instance) or
        ``None`` if no stats are available.
        """
        return self.__stats

    def __residual_rate_check(self, qclass):
        """Check that there is enough rate for a new class
        """
        child_rate = qclass.get_rate()
        if child_rate > self.__residual_rate:
            _logger.error("%s: %s: rate (%d) of %s exceeds residual rate (%d)",
                        self.__residual_rate_check.__qualname__,
                        self,
                        child_rate,
                        qclass,
                        self.__residual_rate)
            raise TcBandwidthError(
                    f'rate {child_rate} of {qclass} exceeds residual '
                    f'rate {self.__residual_rate} of {self}')

    def _add_child_class(self, qclass: 'HTBQClass'):
        """Add ``qclass`` as a child of this :class:`HTBQClass`.

        The residual rate is updated accordingly.
        """
        super()._add_child_class(qclass)
        self.__residual_rate -= qclass.get_rate()
        if self.__residual_rate < 0:
            _logger.warning(
                "%s: %s: negative residual rate after addition of %s",
                        self._add_child_class.__qualname__,
                        self,
                        qclass)

    def _remove_child_class(self, qclass: 'HTBQClass'):
        """Remove ``qclass`` from the children of this :class:`HTBQClass`.

        The residual rate is updated accordingly.
        """
        super()._remove_child_class(qclass)
        self.__residual_rate += qclass.get_rate()

    def child_admission_check(self, new_child_class: 'HTBQClass') -> None:
        """Perform sanity tests before adding a child class:

            - child is an :class:`HTBQClass`
            - child ceil <= parent ceil
            - aggr children rate <= parent rate

        Raises a :exc:`TcBandwidthError` if the check fails
        """
        if not isinstance(new_child_class, HTBQClass):
            _logger.error("%s: %s: class-mismatch: expected=HTBQClass found=%s",
                                self.child_admission_check.__qualname__,
                                self,
                                type(new_child_class))
            raise TcBandwidthError(f"not a HTBQClass: {new_child_class}")
        self.__residual_rate_check(new_child_class)
        child_ceil = new_child_class.get_ceil()
        if child_ceil > self.__ceil:
            _logger.error("%s: %s: ceil (%d) of '%s' exceeds our ceil (%d)",
                            self.child_admission_check.__qualname__,
                            self,
                            child_ceil,
                            new_child_class,
                            self.__ceil)
            raise TcBandwidthError(
                        f"{new_child_class} ceil {child_ceil} > "
                        f"parent {self} ceil {self.__ceil}")

    def _parse_stats(self, line_group_iter) -> None:
        """Parse queuing stats
        """
        stats = HTBQClassStats()
        if stats.init_from_output(line_group_iter):
            self.__stats = stats

    @classmethod
    def parse(cls, qclass_output) -> 'HTBQClass':
        """Create a :class:`HTBQClass` object from the output of **tc(8)**.

        Raises :class:`TcParsingError` if unable to parse

        :meta private:
        """
        field_iter = qclass_output.get_field_iter()
#
# The iterator returns the fields of a line like this:
#
# class htb 1:11 parent 1:1 prio 0 rate 500bit ceil 500bit burst 1600b cburst 1600b
#
# or
#
# class htb 1:1 root rate 100000Kbit ceil 100000Kbit burst 1600b cburst 1600b
#
# The fields 'class', 'htb', 'root', 'parent', 'leaf' (and their values)
# have been consumed by the caller.
#
        try:
            prio = None
            rate = None
            ceil = None
            burst = None
            cburst = None
            for field in field_iter:
                if field == 'prio':
                    prio = int(next(field_iter))
                elif field == 'rate':
                    rate = bwstr2int(next(field_iter))
                elif field == 'ceil':
                    ceil = bwstr2int(next(field_iter))
                elif field == 'burst':
                    burst = unitstr2num(next(field_iter), 'b')
                elif field == 'cburst':
                    cburst = unitstr2num(next(field_iter), 'b')
                else:
                    raise TcParsingError(f"unknown field '{field}'")
            htb_class = HTBQClass(qclass_output.get_handle(),
                                    qclass_output.get_parent_handle(),
                                    rate=rate,
                                    ceil=ceil, prio=prio,
                                    burst=burst, cburst=cburst)
            return htb_class
        except ValueError as valerr:
            raise TcParsingError(f"bad value for {field}") from valerr


class HTBQDisc(QDisc):
    """This class provides access to the Hierarchy Token Bucket
    queueing discipline of Linux (see **tc-htb(8)**).
    """
    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                *,
                default_class_minor: Optional[int] =None,
                r2q: Optional[int] =None):
        """
        :param qdisc_handle: handle of this queuing discipline
        :param parent_handle: handle of parent, ``None`` if this is a
            root queuing discipline
        :param default_class_minor: minor number of default class
        :param r2q: when a queuing class of this queuing discipline has
            not an explicitly specified quantaum, its quantum is
            computed as ``rate/r2q``
        """
        super().__init__(qdisc_handle, parent_handle)
        if default_class_minor is not None:
            self.__default_class_handle = Handle(qdisc_handle.major,
                                                        default_class_minor)
        else:
            self.__default_class_handle = None
        self.__r2q = r2q

    def __str__(self):
        return f"HTBQDisc({self.get_handle()})"

    def get_default_class_handle(self) -> Optional[Handle]:
        """Get the handle of the default class
        """
        return self.__default_class_handle

    def get_r2q(self) -> Optional[int]:
        """Returns the rate-to-quantum divisor
        """
        return self.__r2q

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by tc to create
        a HTB qdisc
        """
        args = ['htb']
        if self.__default_class_handle is not None:
            args.extend(['default', f'{self.__default_class_handle.minor:x}'])
        if self.__r2q is not None:
            args.extend(['r2q', f'{self.__r2q:d}'])
        return args

    def get_description(self) -> str:
        """Returns a string describing the queuing discipline and
        its attributes
        """
        retval = super().get_description()
        if self.__default_class_handle:
            retval += f' default {self.__default_class_handle}'
        if self.__r2q:
            retval += f' r2q {self.__r2q}'
        return retval

    @classmethod
    def parse(cls, qdisc_output) -> 'HTBQDisc':
        """Create a HTBQDisc object from the output of the **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc htb 1: root refcnt 2 r2q 10 default 10 direct_packets_stat 0
        #
        # The next field to be returned from field_iter is 'r2q'
        #
        default_class_minor = None
        r2q = None
        for field in field_iter:
            if field == 'r2q':
                r2q = int(next(field_iter))
            elif field in ('direct_packets_stat', 'direct_qlen'):
                _ = next(field_iter)
            elif field == 'default':
                try:
                    default_class_minor = int(next(field_iter), 16)
                except ValueError as valerr:
                    raise TcParsingError(
                        "bad default class minor number") from valerr
            else:
                raise TcParsingError(f"unknown htb argument '{field}'")
        htb = HTBQDisc(qdisc_output.get_handle(),
                        qdisc_output.get_parent_handle(),
                        default_class_minor=default_class_minor, r2q=r2q)
        return htb


QDiscParser.register_qdisc('htb', HTBQDisc)
QClassParser.register_qclass('htb', HTBQClass)
