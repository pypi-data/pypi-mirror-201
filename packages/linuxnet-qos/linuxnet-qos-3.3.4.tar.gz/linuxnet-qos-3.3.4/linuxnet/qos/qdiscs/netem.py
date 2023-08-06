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

"""This module provides access to the netem queueing discipline
"""

from typing import List, Optional, Tuple, Union

from ..exceptions import TcParsingError
from ..handle import Handle
from ..tcunit import timestr2float
from ..parsers import QDiscParser
from ..deps import get_logger

from .qdisc import QDisc

_logger = get_logger("linuxnet.qos.qdiscs.netem")

class Param:
    """Parses a netem parameter
    """

    INT = 1
    TIME = 2
    PERCENT = 3

    def __init__(self, *argtypes, **kwargs):
        self.__argtypes = argtypes
        self.__kwargs = kwargs
        self.__param = None
        self.__values = []

    def parse(self, param: str, field_iter) -> Optional[str]:
        """Parse the parameter values based on the stored argtypes.

        Returns the next field.
        """
        self.__param = param
        self.__values = []
        try:
            for i, argtype in enumerate(self.__argtypes):
                field = next(field_iter)
                if argtype == self.INT:
                    self.__values.append(int(field))
                elif argtype == self.TIME:
                    self.__values.append(timestr2float(field))
                elif argtype == self.PERCENT:
                    if not field.endswith('%'):
                        raise TcParsingError(
                            f"bad value for field '{param}'")
                    self.__values.append(int(field[:-1]))
                else:
                    _logger.warning(
                        "unknown argument type %d for parameter '%s'",
                                argtype, self.__param)
                field = None
        except StopIteration as stopit:
            if i == 0:
                raise TcParsingError(
                        f"missing value for field '{param}'") from stopit
        except TcParsingError:
            if i == 0:
                raise
        return field

    def update_kwargs(self, kwargs):
        """Update the kwargs which will be provided to NetemQDisc.__init__
        """
        if self.__param:
            param_name = self.__kwargs.get('name', self.__param)
        if len(self.__argtypes) > 1:
            argval = tuple(self.__values)
        else:
            argval = self.__values[0]
        kwargs[param_name] = argval



class NetemQDisc(QDisc):
    """This class provides access to the ``netem``
    queueing discipline (see **tc-netem(8)**).
    """

    def __init__(self, qdisc_handle: Handle, parent_handle: Optional[Handle],
                    *,
                    delay: Union[float, int, Tuple, None] =None,
                    limit: Optional[int] =None,
                    drop: Union[int, Tuple, None] =None,
                    duplicate: Union[int, Tuple, None] =None,
                    corrupt: Union[int, Tuple, None] =None,
                    reorder: Union[int, Tuple, None] =None,
                    gap: Optional[int] =None,
                    ):
        """
        :param qdisc_handle: :class:`Handle` of this :class:`NetemQDisc`
        :param parent_handle: :class:`Handle` of the parent :class:`QDisc`,
            or ``None`` if this is a root queuing discipline
        :param delay: delay (in ms) added to each outgoing packet;
            ``delay`` can be specified as a :class:`float`, as an :class:`int`,
            or as a tuple of the form ``(delay, [jitter, [correlation]])``
        :param limit: packet limit
        :param drop: drop percentage;
            ``drop`` can be specified as an :class:`int`,
            or as a tuple of the form ``(percent, [correlation])``
        :param duplicate: duplicate percentage;
            ``duplicate`` can be specified as an :class:`int`,
            or as a tuple of the form ``(percent, [correlation])``
        :param corrupt: corrupt percentage;
            ``corrupt`` can be specified as an :class:`int`,
            or as a tuple of the form ``(percent, [correlation])``
        :param reorder: reorder percentage;
            ``reorder`` can be specified as an :class:`int`,
            or as a tuple of the form ``(percent, [correlation])``
        :param gap: packet distance when reordering
        """
        super().__init__(qdisc_handle, parent_handle)
        if isinstance(delay, float):
            self.__delay = (delay,)             # in ms
        elif isinstance(delay, int):
            self.__delay = (float(delay),)      # in ms
        else:   # should be either a Tuple or None
            self.__delay = delay
        self.__limit = limit
        if isinstance(drop, int):
            self.__loss = (drop,)
        else:
            self.__loss = drop
        if isinstance(duplicate, int):
            self.__duplicate = (duplicate,)
        else:
            self.__duplicate = duplicate
        if isinstance(corrupt, int):
            self.__corrupt = (corrupt,)
        else:
            self.__corrupt = corrupt
        if isinstance(reorder, int):
            self.__reorder = (reorder,)
        else:
            self.__reorder = reorder
        self.__gap = gap

    def __str__(self):
        return f"NetemQDisc({self.get_handle()})"

    def get_description(self) -> str:
        """Returns a string describing this :class:`NetemQDisc` instance and
        its attributes
        """
        retval = super().get_description()
        if self.__delay is not None:
            retval += f' delay {self.__delay[0]:.1f}ms'
            if len(self.__delay) >= 2:
                retval += f' {self.__delay[1]:.1f}ms'
            if len(self.__delay) >= 3:
                retval += f' {self.__delay[2]:d}%'
        return retval

    def get_delay(self) -> Optional[float]:
        """Returns the delay added to outgoing packets (in ms)
        """
        return self.__delay[0] if self.__delay is not None  else None

    def get_delay_all(self) -> Optional[Tuple]:
        """Returns the delay parameters as the tuple
        ``(delay, [jitter, [correlation]])``
        """
        return self.__delay if self.__delay is not None  else None

    def get_limit(self) -> Optional[int]:
        """Returns the packet limit
        """
        return self.__limit

    def get_loss(self) -> Optional[int]:
        """Returns the packet loss rate (percentage)
        """
        return self.__loss[0] if self.__loss is not None  else None

    def get_loss_all(self) -> Optional[Tuple]:
        """Returns the packet loss parameters as the tuple
        ``(percent, [correlation])``
        """
        return self.__loss

    def get_duplicate(self) -> Optional[int]:
        """Returns the duplicate packet percentage
        """
        return self.__duplicate[0] if self.__duplicate is not None else None

    def get_duplicate_all(self) -> Optional[Tuple]:
        """Returns the packet duplication parameters as the tuple
        ``(percent, [correlation])``
        """
        return self.__duplicate

    def get_corrupt(self) -> Optional[int]:
        """Returns the corrupted packet percentage
        """
        return self.__corrupt[0] if self.__corrupt is not None else None

    def get_corrupt_all(self) -> Optional[int]:
        """Returns the packet corruption parameters as the tuple
        ``(percent, [correlation])``
        """
        return self.__corrupt

    def get_reorder(self) -> Optional[int]:
        """Returns the reordered packet percentage
        """
        return self.__reorder[0] if self.__reorder is not None else None

    def get_reorder_all(self) -> Optional[int]:
        """Returns the packet reordering parameters as the tuple
        ``(percent, [correlation])``
        """
        return self.__reorder

    def get_gap(self) -> Optional[int]:
        """Returns the gap (in packets) when reordering
        """
        return self.__gap

    def qdisc_creation_args(self) -> List[str]:
        """Returns the arguments expected by **tc(8)** to create
        a netem qdisc
        """
        args = ['netem']
        if self.__delay is not None:
            args += ['delay', f'{self.__delay[0]:.1f}ms']
            if len(self.__delay) >= 2:
                args.append(f'{self.__delay[1]:.1f}ms')
            if len(self.__delay) >= 3:
                args.append(f'{self.__delay[2]:d}')
        if self.__limit is not None:
            args += ['limit', f'{self.__limit:d}']
        if self.__loss is not None:
            args += ['drop'] + [str(n) for n in self.__loss]
        if self.__duplicate is not None:
            args += ['duplicate'] + [str(n) for n in self.__duplicate]
        if self.__corrupt is not None:
            args += ['corrupt'] + [str(n) for n in self.__corrupt]
        if self.__reorder is not None:
            args += ['reorder'] + [str(n) for n in self.__reorder]
        if self.__gap is not None:
            args += ['gap', str(self.__gap)]
        return args

    _param_map = {
                        'limit' : Param(Param.INT),
                        'delay' : Param(Param.TIME, Param.TIME, Param.PERCENT),
                        'loss' : Param(Param.PERCENT, Param.PERCENT,
                                                        name='drop'),
                        'duplicate' : Param(Param.PERCENT, Param.PERCENT),
                        'reorder' : Param(Param.PERCENT, Param.PERCENT),
                        'corrupt' : Param(Param.PERCENT, Param.PERCENT),
                        'gap' : Param(Param.INT),
                }

    @classmethod
    def parse(cls, qdisc_output) -> 'NetemQDisc':
        """Create a :class:`NetemQDisc` object from the output of the
        **tc(8)** command.

        :meta private:
        """
        field_iter = qdisc_output.get_field_iter()
        #
        # The fields are generated from a split of a line like this:
        #
        # qdisc netem 114: parent 1:104 limit 1000 delay 100.0ms 20.0ms
        #
        # The next field to be returned from field_iter is 'limit'
        #
        # Some fields, like delay accept 1, 2 or 3 values. In the above,
        # 100ms is the delay and 20.0 variance.
        #
        kwargs = {}
        field = None
        while True:
            if field is None:
                field = next(field_iter, None)
                if field is None:
                    break
            param = cls._param_map.get(field)
            if param is None:
                raise TcParsingError(f"unknown argument '{field}'")
            field = param.parse(field, field_iter)
            param.update_kwargs(kwargs)
        return NetemQDisc(qdisc_output.get_handle(),
                                qdisc_output.get_parent_handle(), **kwargs)


QDiscParser.register_qdisc('netem', NetemQDisc)
