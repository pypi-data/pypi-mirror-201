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
This module provides access to functions and classes that can be used
to extend the functionality of this package by adding support
for new queueing disciplines, classes, and traffic filters.
"""

# pylint: disable=unused-import

from .exceptions import TcError, TcParsingError

from .qdiscs.qdisc import (
                        QDisc,
                        QClass,
                        QStats,
                        QNode,
                        )

from .filters.filter import TrafficFilter

from .parsers import (
                QDiscParser,
                QClassParser,
                TrafficFilterParser,
                QDiscOutput,
                QClassOutput,
                FilterOutput,
                FilterOutputLine,
                LineGroupIterator,
                )

from .tcunit import (
                bwstr2int,
                datastr2int,
                timestr2float,
                rate2str,
                )
