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
This module provides access to the ``fw`` filter.
"""

from typing import List, Optional

from ..deps import get_logger
from ..exceptions import TcError, TcParsingError
from ..handle import Handle
from ..parsers import TrafficFilterParser, FilterOutput

from .filter import TrafficFilter

_logger = get_logger("linuxnet.qos.filters.fwfilter")


class FwmarkIPFilter(TrafficFilter):
    """This class is used for filters that compare against the firewall
    mark when the ethernet frames carry IP datagrams (see **tc-fw(8)**)
    """

    def __init__(self, *,
                        prio=None,
                        dest_class_handle: Optional[Handle] =None,
                        filter_name=None,
                        fwmark: Optional[int] =None):
        """
        :param prio: filter priority (integer)
        :param dest_class_handle: :class:`Handle` of queuing class where
            filter-matching traffic will be directed
        :param filter_name: user-friendly filter name (string)
        :param fwmark: firewall mark (integer)
        """
        super().__init__(protocol='ip', prio=prio, filter_type='fw',
                                dest_class_handle=dest_class_handle,
                                filter_name=filter_name)
        self.__fwmark = fwmark

    def __str__(self):
        filter_name = self.get_filter_name() or ""
        prio = self.get_prio()
        return f'FwmarkIPFilter({filter_name}:0x{prio:x})'

    def get_description(self) -> str:
        """Returns a string with detailed info about the filter
        """
        filter_name = self.get_filter_name() or "FW-IP-Filter"
        filter_type = self.get_filter_type()
        prio = self.get_prio()
        return (f'{filter_name}({filter_type}:0x{prio:x}): '
                f'FWMARK == {self.__fwmark}')

    def get_match_name(self) -> Optional[str]:
        """Returns a string with the name that describes the traffic matched
        by the filter.
        """
        if self.__fwmark is None:
            return None
        return f'fwmark:0x{self.__fwmark:x}'

    def filter_creation_args(self) -> List[str]:
        """Returns a list of **tc(8)** arguments to create this filter
        """
        if self.__fwmark is None:
            raise TcError('missing fwmark')
        return ['handle', str(self.__fwmark), 'fw',
                        'classid', str(self.get_dest_handle())]

    def get_fwmark(self) -> Optional[int]:
        """Returns the fwmark that this filter compares against
        """
        return self.__fwmark

    def set_fwmark(self, fwmark: int):
        """Set the fwmark that this filter compares against.

        Raises a :class:`TcError` if the filter is already instantiated.
        """
        if self.is_instantiated():
            raise TcError('cannot change fwmark of instantiated filter')
        self.__fwmark = fwmark

    @classmethod
    def parse(cls, filt_output: FilterOutput) -> TrafficFilter:
        """Parse the filter output in ``filt_output`` into a
        :class:`TrafficFilter` instance.

        :meta private:
        """
        #
        # The expected format of the filter output lines (after the
        # 'fw' filter type) is:
        #
        #    handle 0x100 classid 1:200
        #
        # The classid is optional.
        #
        owner = filt_output.get_filter_owner()
        fwmark = None
        class_handle = None
        action = None
        for filter_line in filt_output.filter_lines_iter():
            field_iter = iter(filter_line)
            for field in field_iter:
                if field == 'handle':
                    fwmark = int(next(field_iter), 16)
                elif field == 'classid':
                    class_handle = Handle.parse(next(field_iter),
                                                    owner.get_handle().major)
                elif field == 'chain':
                    _ = next(field_iter)
                elif field == 'police':
                    fields = [field] + list(field_iter)
                    action = TrafficFilterParser.parse_action(fields,
                                    filt_output.nonfilter_lines_iter())
                else:
                    reason = f"unexpected argument: {field}"
                    line = str(filter_line)
                    _logger.error("%s: %s line='%s' (owner=%s)",
                        cls.parse.__qualname__, reason, line, owner)
                    raise TcParsingError(reason, line=line)
            if fwmark is not None and class_handle is not None:
                break
        if fwmark is None:
            reason = 'fw filter with no handle'
            _logger.error("%s: %s (owner=%s)",
                        cls.parse.__qualname__, reason, owner)
            raise TcParsingError(reason)
        traffic_filter = FwmarkIPFilter(
                        prio=filt_output.get_prio(),
                        dest_class_handle=class_handle,
                        fwmark=fwmark)
        if action is not None:
            traffic_filter.add_action(action)
        return traffic_filter


TrafficFilterParser.register_filter(filter_type='fw', protocol='ip',
                                                klass=FwmarkIPFilter)
