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

"""This module provides functions that can process the output of tc
"""

import enum
import re

from .exceptions import TcParsingError

_int_unit_expr = re.compile(r'(\d+)(.*)')
_float_unit_expr = re.compile(r'(\d+([.]\d+)?)(.*)')

def bwstr2int(bwstr: str) -> int:
    """Convert a string of the form

        * 500000bit
        * 500000Kbit
        * 500000Mbit

    to the corresponding number.
    """
    match = _int_unit_expr.match(bwstr)
    if match is None:
        raise TcParsingError(f'not a valid bandwidth string: {bwstr}')
    numstr = match.group(1)
    unit = match.group(2)
    if unit == 'bit':
        multiplier = 1
    elif unit == 'Kbit':
        multiplier = 1000
    elif unit == 'Mbit':
        multiplier = 1000 * 1000
    else:
        raise TcParsingError(f'unknown bandwidth unit: {unit}')
    return int(numstr) * multiplier


def datastr2int(datastr: str) -> int:
    """Convert a string of the form

        * 500000b
        * 500000Kb
        * 500000Mb

    to the corresponding number.  'b' stands for 'byte'.
    """
    match = _int_unit_expr.match(datastr)
    if match is None:
        raise TcParsingError(f'not a valid data string: {datastr}')
    numstr = match.group(1)
    unit = match.group(2)
    if unit == 'b':
        multiplier = 1
    elif unit == 'Kb':
        multiplier = 1000
    elif unit == 'Mb':
        multiplier = 1000 * 1000
    else:
        raise TcParsingError(f'unknown data unit: {unit}')
    return int(numstr) * multiplier


def timestr2float(timestr: str) -> float:
    """Convert a string of the form

        * 10s
        * 11.3ms
        * 201.3us

    to the corresponding number.
    The unit of the return value is always milliseconds.
    """
    match = _float_unit_expr.match(timestr)
    if match is None:
        raise TcParsingError(f'not a valid time string: {timestr}')
    numstr = match.group(1)
    unit = match.group(3)
    if unit == 's':
        multiplier = 1000.0
    elif unit == 'ms':
        multiplier = 1.0
    elif unit == 'us':
        multiplier = 0.001
    else:
        raise TcParsingError(f'unknown time unit: {unit}')
    return float(numstr) * multiplier


def unitstr2num(bytestr: str, suffix: str) -> int:
    """Convert a string of the form '1600b' to the corresponding number
    """
    if not bytestr.endswith(suffix):
        raise ValueError(f"missing suffix '{suffix}': " + bytestr)
    return int(bytestr[:-len(suffix)])


class _TcBandwidthUnit(enum.IntEnum):
    """This class uses units as reported by the tc(8) command.
        kbit means kilobit per second
        mbit means megabit per second
        bps means bytes per second
    """
    # pylint: disable=invalid-name
    mbit = 1000 * 1000
    kbit = 1000
    bps = 8
    # pylint: enable=invalid-name


def rate2str(rate: int) -> str:
    """Convert the specified rate to a string suitable as an argument to
    the **tc(8)** command, using the maximum unit size possible.
    For example::

        >>> print(rate2str(128), rate2str(1024), rate2str(10000))
        16bps 128bps 10kbit
        >>> print(rate2str(1000000),rate2str(1500000))
        1mbit 1500kbit

    bps stands for bytes-per-second.
    """
    for unit in list(_TcBandwidthUnit):
        n_units = rate // unit
        if n_units == 0:
            continue
        if rate % unit == 0:
            return f'{n_units}{unit.name}'
    # pylint: disable=consider-using-f-string
    return "%.3fbps" % (rate / 8)
