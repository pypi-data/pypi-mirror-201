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

"""This module provides access to the ingress queueing discipline
"""

from typing import List

from ..deps import get_logger
from ..handle import Handle
from ..parsers import QDiscParser

from .qdisc import QDisc

_logger = get_logger('linuxnet.qos.qdiscs.ingress')


class IngressQDisc(QDisc):
    """This class provides access to the ``ingress``
    queueing discipline.
    """

    __HANDLE = Handle(0xffff, 0)
    __PARENT_HANDLE = Handle(0xffff, 0xfff1)

    def __init__(self, handle=None, parent_handle=None):
        """
        :meta private:
        """
        super().__init__(handle or self.__HANDLE,
                                parent_handle or self.__PARENT_HANDLE)

    def __str__(self):
        return f"Ingress({self.get_handle()})"

    @staticmethod
    def is_ingress():
        """Always returns ``True``
        """
        return True

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by the **tc(8)** command  to create
        an ``ingress`` qdisc
        """
        return []

    @classmethod
    def parse(cls, qdisc_output) -> 'IngressQDisc':
        """Create a :class:`IngressQDisc` object from the output of the
        **tc(8)** command.

        :meta private:
        """
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc ingress ffff: parent ffff:fff1 ----------------
        #
        # The next field to be returned from field_iter is '-----------'
        #
        return IngressQDisc(qdisc_output.get_handle(),
                                qdisc_output.get_parent_handle())

QDiscParser.register_qdisc('ingress', IngressQDisc)
