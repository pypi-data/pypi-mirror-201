# Copyright (c) 2023, Panagiotis Tsirigotis

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
This module provides access to the ``police`` action.
"""

from typing import Iterator, List, Optional

from ..deps import get_logger
from ..exceptions import TcParsingError
from ..parsers import TrafficFilterParser
from ..tcunit import bwstr2int, datastr2int

from .action import TrafficAction, ActionDecision

_logger = get_logger("linuxnet.qos.actions.police")


class PoliceAction(TrafficAction):
    """This class supports the **tc(8)** ``police`` action as
    documented in :manpage:`tc-police(8)`.
    """

    KIND = 'police'

    def __init__(self, action_index: Optional[int] =None,
                        *,
                        rate: Optional[int] =None,
                        burst: Optional[int] =None,
                        mtu: Optional[int] =None,
                        decision: ActionDecision,
                        overhead: Optional[int] =None):
        """
        :param action_index: an integer that effectively names the action
        :param rate: rate
        :param burst: burst
        :param mtu: MTU
        :param decision: control action to take
        :param overhead: overhead
        """
        super().__init__(self.KIND, action_index)
        self.__rate = rate
        self.__burst = burst
        self.__mtu = mtu
        self.__decision = decision
        self.__overhead = overhead

    def get_rate(self) -> Optional[int]:
        """Returns the rate
        """
        return self.__rate

    def get_burst(self) -> Optional[int]:
        """Returns the burst
        """
        return self.__burst

    def get_mtu(self) -> Optional[int]:
        """Returns the mtu
        """
        return self.__mtu

    def get_overhead(self) -> Optional[int]:
        """Returns the overhead
        """
        return self.__overhead

    def get_decision(self) -> ActionDecision:
        """Returns the decision (e.g. :attr:`ActionDecision.DROP`)
        for this action
        """
        return self.__decision

    def action_creation_args(self) -> List[str]:
        """Returns a list of **tc(8)** arguments to create this filter
        """
        args = []
        if self.__rate:
            args.extend(['rate', str(self.__rate)])
        if self.__burst:
            args.extend(['burst', str(self.__burst)])
        if self.__mtu:
            args.extend(['mtu', str(self.__mtu)])
        if self.__decision:
            args.append(self.__decision.value)
        if self.__overhead:
            args.extend(['overhead', str(self.__overhead)])
        return args

    @classmethod
    def parse(cls, fields: List[str],
                        line_iter: Iterator) -> TrafficAction:
        """The ``fields`` list holds the line fields after ``police``.
        The ``line_iter`` is an iterator for the following lines.
        If the fields are successfully parsed, a :class:`PoliceAction`
        instance is returned.

        :meta private:
        """
        #
        # The expected format of the fields is:
        #
        #    0x1 rate 256Kbit burst 10Kb mtu 2Kb action drop overhead 0b
        #
        # 0x1 is the action index.
        #
        fiter = iter(fields)
        action_index = int(next(fiter), 16)
        rate = None
        burst = None
        mtu = None
        decision = None
        overhead = None
        for field in fiter:
            if field == 'rate':
                rate = bwstr2int(next(fiter))
            elif field == 'burst':
                burst = datastr2int(next(fiter))
            elif field == 'mtu':
                mtu = datastr2int(next(fiter))
            elif field == 'action':
                decision = ActionDecision.create_from_string(next(fiter))
            elif field == 'overhead':
                overhead = datastr2int(next(fiter))
            else:
                _logger.warning("unexpected police attribute: %s", field)
        if decision is None:
            raise TcParsingError("police control action missing")
        for line in line_iter:
            line = line.strip()
            if not line:
                break
        return PoliceAction(
                        action_index,
                        rate=rate, burst=burst, mtu=mtu,
                        decision=decision, overhead=overhead)


TrafficFilterParser.register_action(action_name=PoliceAction.KIND,
                                        klass=PoliceAction)
