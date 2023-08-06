# Copyright (c) 2022, 2023, Panagiotis Tsirigotis

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

"""This module provides access to the PRIO queueing discipline
"""

from typing import List, Optional, Sequence, Tuple

from ..deps import get_logger
from ..exceptions import TcParsingError, TcError
from ..handle import Handle
from ..parsers import QClassParser, QDiscParser

from .qdisc import QDisc, QClass


_logger = get_logger("linuxnet.qos.qdiscs.prio")

class PrioQClass(QClass):
    """A class of the :class:`PrioQDisc` (``prio``) queuing discipline.
    """

    def __str__(self):
        return f"PrioQClass({self.get_handle()})"

    def qclass_creation_args(self) -> List[str]:
        """The traffic classes of the ``prio`` qdisc are automatically
        instantiated when the qdisc is instantiated, and the same is true
        of the corresponding :class:`PrioQClass` objects.
        An attempt to invoke this method to instantiate such a class
        will result in a :class:`TcError` exception.

        :meta private:
        """
        raise TcError(
                'classes of the prio qdisc cannot be manually instantiated')

    def get_description(self) -> str:
        """Returns a string describing the class and its attributes
        """
        class_name = self.get_class_name()
        if class_name is None:
            retval = str(self)
        else:
            retval = f'{class_name}({self.get_handle()}) prio'
        return retval

    @classmethod
    def parse(cls, qclass_output) -> 'PrioQClass':
        """Create a :class:`PrioQClass` from the output of **tc(8)**

        :meta private:
        """
        #
        # The tc output looks like this:
        #
        #     class prio 1:1 parent 1:
        #
        # Everyhing has been consumed by the caller.
        #
        return PrioQClass(qclass_output.get_handle(),
                            qclass_output.get_parent_handle())


class PrioQDisc(QDisc):
    """This class provides access to the Priority queueing discipline
    of Linux (see **tc-prio(8)**).
    """

    DEFAULT_BANDS = 3
    DEFAULT_PRIOMAP = (1, 2, 2, 2, 1, 2, 0, 0 , 1, 1, 1, 1, 1, 1, 1, 1)

    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                    bands: Optional[int] =None,
                    priomap: Optional[Sequence[int]] =None):
        """
        :param qdisc_handle: handle of this :class:`PrioQDisc`
        :param parent_handle: handle of parent, ``None`` if this is a
            root queuing discipline
        :param bands: as documented in **tc-prio(8)**
        :param priomap: as documented in **tc-prio(8)**

        The ``bands`` and ``priomap`` parameters must be consistent:
            * ``priomap`` must have 16 entries (number of Linux priorities)
            * value of each entry in ``priomap`` must be less than ``bands``
        """
        super().__init__(qdisc_handle, parent_handle)
        if bands is None:
            self.__bands = self.DEFAULT_BANDS
        else:
            if bands <= 0:
                raise TcError(f'invalid number of bands: {bands}')
            self.__bands = bands
        if priomap is not None:
            n_prio = len(self.DEFAULT_PRIOMAP)
            if len(priomap) != n_prio:
                raise TcError(f'priomap must have {n_prio} entries')
            for band in priomap:
                # pylint: disable=superfluous-parens
                if not (0 <= band < self.__bands):
                    raise TcError(f'invalid band number {band} in priomap')
            self.__priomap = tuple(priomap)
        else:
            # The default priomap requires at least 3 bands.
            if self.__bands < self.DEFAULT_BANDS:
                raise TcError(
                            f'need at least {self.DEFAULT_BANDS} bands '
                            'when using default priomap')
            self.__priomap = self.DEFAULT_PRIOMAP

    def __str__(self):
        return f"PrioQDisc({self.get_handle()})"

    def get_description(self) -> str:
        """Returns a string describing the queuing discipline and
        its attributes
        """
        priomap_str = ' '.join([str(i) for i in self.__priomap])
        return (super().get_description() +
                    f' bands {self.__bands} priomap {priomap_str}')

    def get_bands(self) -> int:
        """Returns the number of bands
        """
        return self.__bands

    def get_priomap(self) -> Tuple[int]:
        """Returns the priomap
        """
        return self.__priomap

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by the **tc(8)** command to create
        a prio qdisc
        """
        args = ['prio', 'bands', str(self.__bands), 'priomap']
        for val in self.__priomap:
            args.append(str(val))
        return args

    def _instantiate_qdisc(self, config) -> None:
        """Instantiate this qdisc inside the kernel.
        """
        super()._instantiate_qdisc(config)
        #
        # Create the child PrioQClass objects since the corresponding
        # kernel traffic classes are created automatically.
        #
        qdisc_handle = self.get_handle()
        major = qdisc_handle.major
        qclass_map = config.get_qclass_map()
        for band in self.__bands:
            class_handle = Handle(major, band+1)
            prioclass = PrioQClass(class_handle, qdisc_handle)
            prioclass._set_config(config)
            self._add_child_class(prioclass)
            qclass_map[class_handle] = prioclass
            _logger.info("%s: registered automatically created class %s",
                self._instantiate_qdisc.__qualname__, prioclass)

    @classmethod
    def parse(cls, qdisc_output) -> 'PrioQDisc':
        """Create a :class:`PrioQDisc` object from the output of
        the **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc prio 2: root refcnt 2 bands 3 priomap  1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1
        #
        # The next field to be returned from field_iter is 'bands'
        #
        bands = None
        priomap = None
        for field in field_iter:
            if field == 'bands':
                try:
                    bands = int(next(field_iter))
                except ValueError as valerr:
                    raise TcParsingError('bad number of bands') from valerr
            elif field == 'priomap':
                priomap = [int(v) for v in field_iter]
            else:
                raise TcParsingError(f"unknown argument '{field}'")
        return PrioQDisc(qdisc_output.get_handle(),
                            qdisc_output.get_parent_handle(), bands, priomap)

QDiscParser.register_qdisc('prio', PrioQDisc)
QClassParser.register_qclass('prio', PrioQClass)
