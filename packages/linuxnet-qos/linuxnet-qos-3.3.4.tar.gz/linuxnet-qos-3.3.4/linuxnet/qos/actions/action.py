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

"""This module provides traffic action classes
"""

from enum import Enum
from typing import List, Optional

class ActionDecision(Enum):
    """List of decisions for **tc(8)** actions (see :manpage:`tc-actions(8)`);
    there are also referred-to as *control* actions.
    """
    #: Reclassify packet
    RECLASSIFY = 'reclassify'
    #: Pass packet to next action
    PIPE = 'pipe'
    #: Drop packet
    DROP = 'drop'
    #: Pass packet to next filter
    CONTINUE = 'continue'
    #: End packet classification (packet returned to queuing discipline/class)
    PASS = 'pass'

    @classmethod
    def create_from_string(cls, decision_str: str) -> 'ActionDecision':
        """Convert from a string to an :class:`ActionDecision` member.

        :param decision_str: the string representation of
            :class:`ActionDecision` member.
        :rtype: a :class:`ActionDecision` member

        Raises a :exc:`ValueError` if no match is found.
        """
        for decision in ActionDecision.__members__.values():
            if decision.value == decision_str:
                return decision
        raise ValueError(f'bad ActionDecision value: {decision_str}')


class TrafficAction:
    """Generic action class. It cannot be instantiated.
    It is subclassed based on action type (aka kind).
    """

    def __init__(self, kind: str, action_index: Optional[int]):
        """
        :param kind: the action type (e.g. ``police``)
        :param action_index: an integer that effectively names the action;
            the kernel will pick one if it is not explicitly given
        """
        self.__kind = kind
        self.__actid = action_index

    def __str__(self):
        return f'TrafficAction({self.__kind})'

    def get_kind(self) -> str:
        """Returns the action type
        """
        return self.__kind

    def get_action_index(self) -> Optional[int]:
        """Returns the action index
        """
        return self.__actid

    def action_creation_args(self) -> List[str]:
        """Returns a list of **tc(8)** arguments to instantiate this action
        """
        raise NotImplementedError
