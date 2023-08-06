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

"""This module provides access to the SFQ queueing discipline
"""

from typing import List, Optional, TextIO

from ..exceptions import TcParsingError
from ..handle import Handle
from ..tcunit import unitstr2num, datastr2int
from ..parsers import QDiscParser

from .qdisc import QDisc, QStats


class SFQQDiscStats(QStats):
    """SFQDisc stats
    """

    @property
    def byte_backlog(self) -> int:
        """Backlog in bytes.

        This value is not a statistic; it reflects the qdisc state at
        the time the stats were obtained.
        """
        return self.get_byte_backlog()

    @property
    def packet_backlog(self) -> int:
        """Backlog in packets.

        This value is not a statistic; it reflects the qdisc state at
        the time the stats were obtained.
        """
        return self.get_byte_backlog()

    def dump(self, outfile: TextIO, width: Optional[int] =None) -> None:
        """Dump stats to ``outfile``.
        There is one stat per line output. Each line has the format::

            header: value

        The ``header:`` part occupies at least ``width`` characters.
        """
        super().dump(outfile, width)
        width = width or self.HEADER_WIDTH
        print(f"{'Backlog:':{width}} "
            f'{self.__byte_backlog} bytes / {self.__packet_backlog} packets',
                file=outfile)


class SFQQDisc(QDisc):
    """This class provides access to the Stochastic Fairness Queueing
    queueing discipline of Linux (see **tc-sfq(8)**).
    """
    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                perturb: Optional[int] =None, quantum: Optional[int] =None):
        """
        :param qdisc_handle: handle of this :class:`SFQQDisc`
        :param parent_handle: handle of parent, ``None`` if this is a
            root queuing discipline
        :param perturb: as documented in **tc-sfq(8)**
        :param quantum: as documented in **tc-sfq(8)**
        """
        super().__init__(qdisc_handle, parent_handle)
        self.__perturb = perturb        # seconds
        self.__quantum = quantum        # bytes
        self.__stats = None

    def __str__(self):
        return f"SFQQDisc({self.get_handle()})"

    def get_description(self) -> str:
        """Returns a string describing the queuing discipline and
        its attributes
        """
        retval = super().get_description()
        if self.__perturb is not None:
            retval += f' perturb {self.__perturb:d}s'
        if self.__quantum is not None:
            retval += f' quantum {self.__quantum:d}B'
        return retval

    def get_perturb(self) -> Optional[int]:
        """Returns the perturb value (in seconds), or ``None``.
        """
        return self.__perturb

    def get_quantum(self) -> Optional[int]:
        """Returns the quantum value (in bytes), or ``None``.
        """
        return self.__quantum

    def get_stats(self) -> Optional[SFQQDiscStats]:
        """Returns the qdisc stats (an :class:`SFQQDiscStats` instance) or
        ``None`` if no stats are available.
        """
        return self.__stats

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by the **tc(8)** command to create
        a SFQ qdisc
        """
        args = ['sfq']
        if self.__perturb is not None:
            args += ['perturb', str(self.__perturb)]
        if self.__quantum is not None:
            args += ['quantum', str(self.__quantum)]
        return args

    def _parse_stats(self, line_group_iter) -> None:
        """Parse queuing stats.
        """
        stats = SFQQDiscStats()
        if stats.init_from_output(line_group_iter):
            self.__stats = stats

    @classmethod
    def parse(cls, qdisc_output) -> 'SFQQDisc':
        """Create a :class:`SFQQDisc` object from the output of
        the **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc sfq 101: parent 1:101 limit 127p quantum 1514b perturb 10sec
        #
        # The next field to be returned from field_iter is 'limit'
        #
        perturb = None
        quantum = None
        for field in field_iter:
            if field == 'limit':
                #
                # 'limit' is not documented in tc-sfq(8), so we ignore it.
                #
                _ = next(field_iter)
            elif field == 'perturb':
                perturb = unitstr2num(next(field_iter), 'sec')
            elif field == 'quantum':
                quantum = datastr2int(next(field_iter))
            elif field == 'depth':
                _ = next(field_iter)
            elif field == 'divisor':
                _ = next(field_iter)
            else:
                raise TcParsingError(f"unknown argument '{field}'")
        return SFQQDisc(qdisc_output.get_handle(),
                        qdisc_output.get_parent_handle(), perturb, quantum)

QDiscParser.register_qdisc('sfq', SFQQDisc)
