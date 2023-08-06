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

"""This module provides the Handle class.
"""

from typing import Optional

from .deps import get_logger
from .exceptions import TcParsingError

_logger = get_logger("linuxnet.qos.handle")


class Handle:
    """Objects of this class represent handles of queue disciplines or
    queue discipline classes.
    """
    def __init__(self, major: int, minor: int):
        """
        :param major: handle major number
        :param minor: handle minor number
        """
        self.__major = major
        self.__minor = minor

    @property
    def major(self):
        """Major number
        """
        return self.__major

    @property
    def minor(self):
        """Minor number
        """
        return self.__minor

    @staticmethod
    def __parsenum(numstr: str, descr: str) -> int:
        """Parse numstr as a hex number
        """
        try:
            return int(numstr, 16)
        except ValueError:
            pass
        raise ValueError(f'bad {descr}: {numstr}')

    def qclass_handle(self, minor: int) -> 'Handle':
        """Create a :class:`Handle` for a class of the same queuing discipline.
        """
        return Handle(self.major, minor)

    @staticmethod
    def qdisc_handle(major: int) -> 'Handle':
        """Create a qdisc handle (the minor number is always 0)

        :param major: handle major number of handle
        """
        return Handle(major, 0)

    @classmethod
    def create_from_string(cls, handle_str: str,
                            default_major: Optional[int] =None) -> 'Handle':
        """Create a :class:`Handle` object from a string

        :param handle_str: string containing handle with the expected
            syntax [[<num>]:]<num>; the number strings are interpreted as
            hexadecimal numbers
        :default_major: if `handle_str` does not contain a ':', it is
            assumed to be the minor number, and this parameter provides
            the major number

        Raises a :exc:`ValueError` if ``handle_str`` is malformed
        """
        if ':' in handle_str:
            major_str, minor_str = handle_str.split(':', 1)
            if major_str:
                major = cls.__parsenum(major_str, 'major number')
            elif default_major is not None:
                major = default_major
            else:
                raise ValueError("major number missing")
            if minor_str:
                minor = cls.__parsenum(minor_str, 'minor number')
            else:
                minor = 0
        elif default_major:
            major = default_major
            minor = cls.__parsenum(handle_str, 'minor number')
        else:
            raise ValueError("major number missing")
        return Handle(major, minor)

    @classmethod
    def parse(cls, handle_str: str,
                        default_major: Optional[int] =None) -> 'Handle':
        """Parse ``handle_str`` into a :class:`Handle` instance.

        :param handle_str: string containing handle with the expected
            syntax [[<num>]:]<num>; the number strings are interpreted as
            hexadecimal numbers
        :default_major: if `handle_str` does not contain a ':', it is
            assumed to be the minor number, and this parameter provides
            the major number

        Raises a :exc:`TcParsingError` if ``handle_str`` cannot be parsed.

        :meta private:
        """
        try:
            return cls.create_from_string(handle_str, default_major)
        except ValueError as valerr:
            raise TcParsingError(
                f"Unable to parse handle: {handle_str}") from valerr

    def __hash__(self):
        return (self.__major << 16) + self.__minor

    # pylint: disable=protected-access
    def __eq__(self, other):
        return (isinstance(other, Handle) and
                self.__major == other.__major and
                self.__minor == other.__minor)

    def __lt__(self, other):
        if not isinstance(other, Handle):
            raise TypeError(f"not a Handle: {other}")
        return (self.__major, self.__minor) < (other.__major, other.__minor)

    def __le__(self, other):
        if not isinstance(other, Handle):
            raise TypeError(f"not a Handle: {other}")
        return (self.__major, self.__minor) <= (other.__major, other.__minor)
    # pylint: enable=protected-access

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __str__(self):
        # pylint: disable=consider-using-f-string
        return "%x:%x" % (self.__major, self.__minor)
