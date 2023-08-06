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

"""This module provides traffic filter classes
"""

from typing import List, Optional

from ..deps import get_logger
from ..exceptions import TcError
from ..handle import Handle

_logger = get_logger("linuxnet.qos.filters.filter")


class TrafficFilter:    # pylint: disable=too-many-instance-attributes
    """Generic filter class. It cannot be instantiated.
    It is subclassed based on filter type.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                        protocol: str, prio: Optional[int], filter_type: str,
                        *,
                        dest_class_handle: Optional[Handle] =None,
                        filter_name: Optional[str] =None):
        """
        :param protocol: protocol
        :param prio: optional filter priority (a number); defaults to -1
        :param filter_type: a string indicating one of the currently supported
            filter types: ``u32``, ``fw``
        :param dest_class_handle: :class:`Handle` of class where this
            filter will direct traffic
        :param filter_name: user-friendly filter name
        """
        self.__protocol = protocol
        self.__prio = prio if prio is not None else -1
        self.__filter_type = filter_type
        self.__instantiated = False
        self.__dest_class_handle = dest_class_handle
        self.__filter_name = filter_name
        self.__action_list = []

    def __str__(self):
        prio = 'NOPRIO' if self.__prio < 0 else f'0x{self.__prio:x}'
        return f'Filter({self.__protocol}/{prio}/{self.__filter_type})'

    def filter_creation_args(self) -> List[str]:
        """Returns a list of **tc(8)** arguments to create this filter
        """
        raise NotImplementedError

    def is_instantiated(self) -> bool:
        """Returns ``True`` if the filter is in the kernel
        """
        return self.__instantiated

    def _mark_as_instantiated(self) -> None:
        """This method is intended to be used by the code that parses
        an existing qdisc configuration.
        """
        self.__instantiated = True

    def get_description(self) -> str:
        """Returns a string with detail info about the filter
        """
        return str(self)

    def get_match_name(self) -> Optional[str]:
        """Returns a string with the name that describes the traffic matched
        by the filter, or ``None``.

        This method should be defined in derived classes.
        """
        _ = self

    def get_filter_type(self) -> str:
        """Returns the filter type
        """
        return self.__filter_type

    def get_prio(self) -> int:
        """Returns the filter priority
        """
        return self.__prio

    def set_prio(self, prio: int):
        """Set the filter priority.

        Raises :class:`TcError` if the filter is instantiated.
        """
        if self.__instantiated:
            _logger.error(
                "%s: %s: attempt to change priority of instantiated filter",
                        self.set_prio.__qualname__,
                        self)
            raise TcError(f"attempt to change filter {self} priority")
        self.__prio = prio

    def get_filter_name(self) -> Optional[str]:
        """Returns the filter name
        """
        return self.__filter_name

    def set_filter_name(self, filter_name: str):
        """Set the filter name
        """
        self.__filter_name = filter_name

    def get_dest_handle(self) -> Optional[Handle]:
        """Returns the :class:`Handle` of the :class:`QClass` where this
        filter will send traffic
        """
        return self.__dest_class_handle

    def set_dest_handle(self, handle: Handle):
        """Sets the handle of the class where this filter will send traffic.

        Raises :class:`TcError` if the filter is instantiated.
        """
        if self.__instantiated:
            _logger.error(
                "%s: %s: attempt to change destination of instantiated filter",
                        self.set_dest_handle.__qualname__,
                        self)
            raise TcError(f"attempt to change filter {self} destination")
        self.__dest_class_handle = handle

    def get_actions(self) -> List['TrafficAction']:
        """Returns the action list for this filter
        """
        return self.__action_list

    def add_action(self, action: 'TrafficAction') -> None:
        """Add a filter action
        """
        if self.__instantiated:
            _logger.error(
                "%s: %s: attempt to add action to an instantiated filter",
                        self.add_action.__qualname__,
                        self)
            raise TcError(f"attempt to add action to filter {self}")
        self.__action_list.append(action)

    def _instantiate(self, owner) -> None:
        """Instantiate a filter by invoking the **tc(8)** command.

        :param owner: :class:`QClass`/:class:`QDisc` that is the parent of
            this filter
        """
        if self.__instantiated:
            raise TcError('filter is already instantiated')
        if self.__dest_class_handle is None:
            raise TcError('filter has no destination class handle')
        config = owner.get_config()
        if config is None:
            raise TcError(f'filter owner {owner} not instantiated')
        cmd = ['tc', 'filter', 'add', 'dev', config.get_interface(),
                'parent', str(owner.get_handle()),
                'protocol', self.__protocol]
        if self.__prio >= 0:
            cmd += ['prio', f'{self.__prio:d}']
        else:
            _logger.warning(
                "instantiating filter %s with no priority -- "
                "it will not be possible to delete",
                    self)
        cmd += self.filter_creation_args()
        for action in self.__action_list:
            cmd += ['action', action.get_kind()]
            action_index = action.get_action_index()
            if action_index is not None:
                cmd += ['index', str(action_index)]
            cmd += action.action_creation_args()
        config.tc_run(cmd, 'filter creation')
        self.__instantiated = True

    def _uninstantiate(self, owner) -> None:
        """Uninstantiate a filter by invoking the **tc(8)** command.

        :param owner: :class:`QClass`/:class:`QDisc` that is the parent of
            this filter
        """
        if not self.__instantiated:
            raise TcError('filter has not been instantiated')
        config = owner.get_config()
        if config is None:
            # If the owner is no longer instantiated, the filter is gone too.
            _logger.info("%s: %s: owner not instantiated: %s",
                    self._uninstantiate.__qualname__, self, owner)
            return
        if self.__prio < 0:
            _logger.error("%s: unable to delete filter '%s': missing priority",
                            self._uninstantiate.__qualname__, self)
            raise TcError(
                        f'unable to delete filter {self} '
                        'because of missing priority')
        cmd = ['tc', 'filter', 'del', 'dev', config.get_interface(),
                'parent', str(owner.get_handle()),
                'prio', f'{self.__prio:d}']
        config.tc_run(cmd, 'filter deletion')
