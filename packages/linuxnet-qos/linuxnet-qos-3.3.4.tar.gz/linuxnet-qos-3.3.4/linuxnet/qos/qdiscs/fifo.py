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

"""This module provides access to the pfifo_fast queueing discipline
"""

from typing import List, Optional, Sequence

from ..deps import get_logger
from ..exceptions import TcError, TcParsingError
from ..handle import Handle
from ..parsers import QDiscParser

from .qdisc import QDisc

_logger = get_logger('linuxnet.qos.qdiscs.fifo')


class PFifoFastQDisc(QDisc):
    """This class provides access to the pfifo_fast
    queueing discipline of Linux (see **tc-pfifo_fast(8)**).
    """

    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                    *,
                    txqueuelen: Optional[int] =None,
                    bands: Optional[int] =None,
                    priomap: Optional[Sequence[int]] =None):
        """
        :param qdisc_handle: handle of this :class:`PFifoFastQDisc`
        :param parent_handle: handle of parent, or ``None`` if this is a
            root queuing discipline
        :param txqueuelen: as documented in **tc-pfifo_fast(8)**
        :param bands: as documented in **tc-pfifo_fast(8)**
        :param priomap: as documented in **tc-pfifo_fast(8)**

        Only ``txqueuelen`` is used when creating a new ``pfifo_fast``
        queuing discipline. If ``bands`` or ``priomap`` are specified,
        this will raise a :class:`TcError` exception.
        """
        super().__init__(qdisc_handle, parent_handle)
        self.__txqueuelen = txqueuelen
        self.__bands = bands
        self.__priomap = priomap

    def __str__(self):
        return f"PFifoFastQDisc({self.get_handle()})"

    def get_description(self) -> str:
        """Returns a string describing the queuing discipline and
        its attributes
        """
        description = super().get_description()
        if self.__txqueuelen:
            description += f' txqueuelen {self.__txqueuelen}'
        if self.__bands:
            description += f' bands {self.__bands}'
        if self.__priomap:
            priomap_str = ' '.join([str(i) for i in self.__priomap])
            description += f' priomap {priomap_str}'
        return description

    def get_txqueuelen(self) -> Optional[int]:
        """Returns the queue length for each band, if specified.
        """
        return self.__txqueuelen

    def set_txqueuelen(self, txqueuelen: Optional[int]) -> None:
        """Set the queue length for each band (if ``None``, use
        the interface's txqueuelen).
        """
        if self.get_config() is not None:
            raise TcError('cannot change txqueuelen of instantiated pfifo_fast')
        self.__txqueuelen = txqueuelen

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by the **tc(8)** command  to create
        a ``pfifo_fast`` qdisc
        """
        if self.__bands is not None:
            raise TcError('cannot specify bands of pfifo_fast')
        if self.__priomap is not None:
            raise TcError('cannot specify priomap of pfifo_fast')
        args = ['pfifo_fast']
        if self.__txqueuelen is not None:
            args += ['txqueuelen', str(self.__txqueuelen)]
        return args

    def _uninstantiate_qdisc(self, config) -> None:
        """Invoke the **tc(8)** command to delete the queuing discipline
        described by this object.

        :param config: a :class:`QDiscConfig` object
        """
        super()._uninstantiate_qdisc(config)
        # We clear these attributes so that the object can be used
        # for instantiation again.
        self.__bands = None
        self.__priomap = None

    @classmethod
    def parse(cls, qdisc_output) -> 'PFifoFastQDisc':
        """Create a :class:`PFifoFastQDisc` object from the output of the
        **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc pfifo_fast 0: root refcnt 2 bands 3 priomap  1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1
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
                _logger.warning("unknown pfifo_fast parameter: %s", field)
        return PFifoFastQDisc(qdisc_output.get_handle(),
                                qdisc_output.get_parent_handle(),
                                bands=bands, priomap=priomap)

QDiscParser.register_qdisc('pfifo_fast', PFifoFastQDisc)
