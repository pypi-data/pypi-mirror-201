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

"""This module provides access to the multiqueue (``mq``) queueing discipline
See
    https://lwn.net/Articles/351021/
for info about this queuing discipline
"""

from typing import List

from ..exceptions import TcError
from ..parsers import QDiscParser, QClassParser

from .qdisc import QDisc, QClass

class MultiQueueQClass(QClass):
    """A class of the :class:`MultiQueueQDisc` (``mq``) queuing discipline.
    """

    def __str__(self):
        return f"MultiQueueQClass({self.get_handle()})"

    def qclass_creation_args(self) -> List[str]:
        """The classes of the ``mq`` qdisc are automatically instantiated.
        An attempt to invoke this method to instantiate such a class
        will result in a :class:`TcError` exception.

        :meta private:
        """
        raise TcError("classes of the 'mq' qdisc "
                        "cannot be manually instantiated")

    def get_description(self) -> str:
        """Returns a string describing the class and its attributes
        """
        class_name = self.get_class_name()
        if class_name is None:
            retval = str(self)
        else:
            retval = f'{class_name}({self.get_handle()}) MQ'
        return retval

    @classmethod
    def parse(cls, qclass_output) -> 'MultiQueueQClass':
        """Create a :class:`MultiQueueQClass` from the output of **tc(8)**

        :meta private:
        """
        return MultiQueueQClass(qclass_output.get_handle(),
                                qclass_output.get_parent_handle())


class MultiQueueQDisc(QDisc):
    """This class provides access to the multiqueue (``mq``)
    queueing discipline of Linux
    """

    def __str__(self):
        return f"MultiQueueQDisc({self.get_handle()})"

    def qdisc_creation_args(self) -> List[str]:
        """The ``mq`` qdisc is automatically instantiated as the default
        root queuing discipline for interfaces with multiple hardware queues.
        An attempt to add a ``mq`` qdisc as the qdisc of a queuing class of a
        classful qdisc failed (the error was 'operation not supported').
        Therefore this class does not support manual instantiation.

        An attempt to invoke this method will result in a :class:`TcError`
        exception.
        """
        raise TcError('the mq qdisc cannot be manually instantiated')

    @classmethod
    def parse(cls, qdisc_output) -> 'MultiQueueQDisc':
        """Create a :class:`MultiQueueQDisc` object from the output of
        **tc(8)**.

        :meta private:
        """
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc mq 0: root
        #
        return MultiQueueQDisc(qdisc_output.get_handle(),
                                qdisc_output.get_parent_handle())

QDiscParser.register_qdisc('mq', MultiQueueQDisc)
QClassParser.register_qclass('mq', MultiQueueQClass)
