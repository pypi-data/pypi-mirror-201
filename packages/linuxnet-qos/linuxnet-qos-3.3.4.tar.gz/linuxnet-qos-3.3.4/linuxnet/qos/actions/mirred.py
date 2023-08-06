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
This module provides access to the ``mirred`` action.
"""

from typing import Iterator, List, Optional

from ..deps import get_logger
from ..exceptions import TcParsingError
from ..parsers import TrafficFilterParser

from .action import TrafficAction

_logger = get_logger("linuxnet.qos.actions.mirred")


class MirredAction(TrafficAction):
    """This class supports the **tc(8)** ``mirred`` action as
    documented in :manpage:`tc-mirred(8)`.
    """

    KIND = 'mirred'

    # mirred_action
    #: `mirred` mirroring action
    MIRROR = 'mirror'
    #: `mirred` redirect action
    REDIRECT = 'redirect'

    # Packet direction when placed at destination interface
    #: Direction for packets to be sent out
    EGRESS = 'egress'
    #: Direction for packets to be received
    INGRESS = 'ingress'

    def __init__(self, action_index: Optional[int] =None,
                        *,
                        mirred_action: str,
                        direction: str,
                        to_dev: str):
        """
        :param action_index: an integer that effectively names the action
        :param mirred_action: either ``mirror`` or ``redirect``
        :param direction: either ``ingress`` or ``egress``
        :param to_dev: destination interface
        """
        super().__init__(self.KIND, action_index)
        self.__mirred_action = mirred_action
        self.__direction = direction
        self.__to_dev = to_dev

    def get_destination_interface(self) -> str:
        """Returns the name of the destination interface
        """
        return self.__to_dev

    def get_mirred_action(self) -> str:
        """Returns the mirred action, either :attr:`MirredAction.MIRROR`
        or :attr:`MirredAction.REDIRECT`
        """
        return self.__mirred_action

    def get_direction(self) -> Optional[int]:
        """Returns the direction of the packet when it arrives at
        the destination interface, either :attr:`MirredAction.INGRESS`
        or :attr:`MirredAction.EGRESS`
        """
        return self.__direction

    def action_creation_args(self) -> List[str]:
        """Returns a list of **tc(8)** arguments to create this filter
        """
        return [self.__direction, self.__mirred_action, 'dev', self.__to_dev]

    @classmethod
    def parse(cls, fields: List[str],
                        line_iter: Iterator) -> TrafficAction:
        """The ``fields`` list holds the line fields after ``mirred``.
        The ``line_iter`` is an iterator for the following lines.
        If the fields are successfully parsed, a :class:`MirredAction`
        instance is returned.

        :meta private:
        """
        #
        # The expected format of the fields is:
        #
        #    (Egress Redirect to device lo) stolen
        #
        # The following line looks like this:
        #
        #       index 20 ref 2 bind 2
        #
        try:
            direction_field = fields[0]
            if direction_field[0] != '(':
                raise TcParsingError("Expected open-paren")
            direction = direction_field[1:].lower()
            if direction not in (cls.INGRESS, cls.EGRESS):
                raise TcParsingError(f"bad direction: {direction}")
            mirred_action = fields[1].lower()
            if mirred_action not in (cls.REDIRECT, cls.MIRROR):
                raise TcParsingError(f"bad mirred action: {mirred_action}")
            if fields[2] != 'to' and fields[3] != 'device':
                raise TcParsingError("missing dest interface")
            interface_field = fields[4]
            if interface_field[-1] != ')':
                raise TcParsingError("Expected close-paren")
            to_dev = interface_field[:-1]
        except IndexError as idxerr:
            raise TcParsingError("missing fields") from idxerr
        action_index = None
        for line in line_iter:
            if not line:
                break
            fields = line.split()
            try:
                if fields[0] == 'index':
                    action_index = int(fields[1])
            except IndexError:
                pass
        return MirredAction(
                        action_index,
                        mirred_action=mirred_action,
                        direction=direction,
                        to_dev=to_dev)


TrafficFilterParser.register_action(action_name=MirredAction.KIND,
                                        klass=MirredAction)
