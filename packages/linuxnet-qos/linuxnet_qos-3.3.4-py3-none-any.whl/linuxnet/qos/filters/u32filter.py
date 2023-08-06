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
This module provides access to the ``u32`` filter.
"""

from ipaddress import IPv4Network, IPv4Address
from typing import List, Optional

from ..deps import get_logger
from ..exceptions import TcError, TcParsingError
from ..handle import Handle
from ..parsers import TrafficFilterParser, FilterOutput

from .filter import TrafficFilter

_logger = get_logger("linuxnet.qos.filters.u32filter")


class U32Selector:         # pylint: disable=too-few-public-methods
    """Abstract base class for selector objects
    """
    def tc_creation_args(self) -> List[str]:
        """Returns a list of strings suitable to be used as arguments
        to the **tc(8)** command.
        """
        raise NotImplementedError

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        _ = self

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        raise NotImplementedError


class IPSubnetSelector(U32Selector):
    """A ``U32`` selector that identifies a subnet
    """
    def __init__(self, direction: str, ipv4_network: IPv4Network):
        """
        :param direction: should be either ``src`` or ``dst``
        :param ipv4_network: match against this subnet
        """
        direction = direction.lower()
        if direction not in ('src', 'dst'):
            raise ValueError("direction must be 'src' or 'dst'")
        self.__direction = direction
        self.__ipv4_network = ipv4_network

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        if self.get_address() == '0.0.0.0' and self.get_prefix() == 0:
            return f'{self.__direction}(any)'.upper()
        return None

    def get_direction(self) -> str:
        """Returns the direction
        """
        return self.__direction

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        return f'{self.__direction} == {self.__ipv4_network}'

    def get_address(self) -> str:
        """Returns the subnet address as a string
        """
        return str(self.__ipv4_network.network_address)

    def get_prefix(self) -> int:
        """Returns the subnet prefix (an int)
        """
        return self.__ipv4_network.prefixlen

    @staticmethod
    def any_source_ip() -> 'IPSubnetSelector':
        """Returns an :class:`IPSubnetSelector` that matches any
        source IP address
        """
        return IPSubnetSelector('src', IPv4Network('0.0.0.0/0'))

    @staticmethod
    def any_dest_ip() -> 'IPSubnetSelector':
        """Returns an :class:`IPSubnetSelector` that matches any
        destination IP address
        """
        return IPSubnetSelector('dst', IPv4Network('0.0.0.0/0'))

    def tc_creation_args(self) -> List[str]:
        """Returns a list of strings suitable to be used as tc args
        """
        return ['ip', self.__direction, f'{self.__ipv4_network}']

    def __eq__(self, other):
        # pylint: disable=protected-access
        return (isinstance(other, IPSubnetSelector) and
                    self.__direction == other.__direction and
                    self.__ipv4_network == other.__ipv4_network)
        # pylint: enable=protected-access



class IPPortSelector(U32Selector):
    """A ``U32`` selector that identifies a TCP/UDP port

    Precondition:
        The protocol should be TCP or UDP.
    """

    __PORT_MAP = {
                    22 : 'SSH',
                    53  : 'DNS',
                    443 : 'HTTPS',
                    587 : 'SMTP',
                    993 : 'IMAPS',
                    8801 : 'ZOOM',
                    25565 : 'MINECRAFT',
                }

    def __init__(self, direction: str, port: int):
        """
        :param direction: should be either ``src`` or ``dst``
        :param port: match against this port number
        """
        if direction not in ('src', 'dst'):
            raise ValueError("direction must be 'src' or 'dst'")
        self.__direction = direction
        self.__port = port

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        proto_name = self.__PORT_MAP.get(self.__port)
        if proto_name is None:
            return None
        return f"{proto_name}/{self.__direction}".upper()

    def get_direction(self) -> str:
        """Returns the direction
        """
        return self.__direction

    def get_port(self) -> int:
        """Returns the port
        """
        return self.__port

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        return f'{self.__direction} port {self.__port}'

    def tc_creation_args(self) -> List[str]:
        """Returns a list of strings suitable to be used as arguments
        to the **tc(8)** command.
        """
        return ['ip', 'sport' if self.__direction == 'src' else 'dport',
                        f'{self.__port:d}', '0xffff']

    def __eq__(self, other):
        # pylint: disable=protected-access
        return (isinstance(other, IPPortSelector) and
                    self.__direction == other.__direction and
                    self.__port == other.__port)
        # pylint: enable=protected-access


class IPProtocolSelector(U32Selector):
    """A ``U32`` selector that identifies a protocol by number
    """

    ICMP = 1
    TCP = 6
    UDP = 17

    __PROTO_MAP = {
                    ICMP : 'ICMP',
                    TCP  : 'TCP',
                    UDP : 'UDP',
                }

    def __init__(self, protonum: int):
        """
        :param protonum: protocol number
        """
        self.__protonum = protonum

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        return self.__PROTO_MAP.get(self.__protonum)

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        return f'IP-proto == {self.__protonum}'

    def tc_creation_args(self) -> List[str]:
        """Returns a list of strings suitable to be used as arguments
        to the **tc(8)** command.
        """
        return ['ip', 'protocol', f'{self.__protonum}', '0xff']

    def __eq__(self, other):
        # pylint: disable=protected-access
        return (isinstance(other, IPProtocolSelector) and
                    self.__protonum == other.__protonum)
        # pylint: enable=protected-access


class NumberSelector(U32Selector):
    """A ``U32`` selector that matches a number at a specific offset in
    the packet.
    """
    def __init__(self, width: str, number: int, mask: int, offset: int):
        """
        :param width: one of ``u8``, ``u16``, ``u32``
        :param number: compare packet contents against this number
        :param mask: apply this mask to the number and the packet contents
            before comparing
        :param offset: offset inside the packet, always in bytes, regardless
            of width
        """
        if width not in ('u8', 'u16', 'u32'):
            raise ValueError(f"invalid width: {width}")
        self.__width = width
        self.__number = number
        self.__mask = mask
        self.__offset = offset

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        retval = f'{self.__width} packet@{self.__offset} & '
        if self.__width == 'u8':
            retval += f'0x{self.__mask:02x} == 0x{self.__number:02x}'
        elif self.__width == 'u16':
            retval += f'0x{self.__mask:04x} == 0x{self.__number:04x}'
        else:
            retval += f'0x{self.__mask:08x} == 0x{self.__number:08x}'
        return retval

    def tc_creation_args(self) -> List[str]:
        """Returns a list of strings suitable to be used as arguments
        to the **tc(8)** command.
        """
        args = [self.__width, f'{self.__number}', f'{self.__mask:#x}']
        if self.__offset != 0:
            args += ['at', f'{self.__offset}']
        return args

    def get_number(self) -> int:
        """Return the comparison value
        """
        return self.__number

    def get_mask(self) -> int:
        """Return the mask
        """
        return self.__mask

    def get_offset(self) -> int:
        """Return the offset
        """
        return self.__offset

    def __eq__(self, other):
        # pylint: disable=protected-access
        return (isinstance(other, NumberSelector) and
                    self.__width == other.__width and
                    self.__number == other.__number and
                    self.__mask == other.__mask and
                    self.__offset == other.__offset)
        # pylint: enable=protected-access


class IPHeaderLength(NumberSelector):   # pylint: disable=too-few-public-methods
    """This is a convenience ``U32`` selector that matches against a specific
    IP header length
    """
    def __init__(self, header_length: int):
        """
        :param header_length: compare packet header length against this number;
            ``header_length`` must be a multiple of 4
        """
        if header_length & 0x3:
            raise ValueError(
                    f'IP header length {header_length} not a multiple of 4')
        n_words = header_length // 4
        if n_words > 0xf:
            raise ValueError(f'IP header length {header_length} too big')
        super().__init__(width='u8', number=n_words, mask=0xf, offset=0)

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        header_len = self.get_number()*4
        return f"IPHDRLEN({header_len})"

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        return f"IP-header-len == {self.get_number()*4}"



class IPDatagramLimit(NumberSelector): # pylint: disable=too-few-public-methods
    """This is a convenience ``U32`` selector that matches if the IP datagram
    size is less that a specific limit; the limit must be a power of 2.
    """
    def __init__(self, limit: int):
        """
        :param limit: compare against this limit
        """
        if limit == 0 or (limit & (limit-1)) != 0:
            raise ValueError(f'invalid datagram size limit: {limit}')
        mask = 0xffff ^ (limit-1)
        super().__init__(width='u16', number=0, mask=mask, offset=2)

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        limit = (self.get_mask() ^ 0xffff) + 1
        return f"IPDGLIM({limit})"

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        limit = (self.get_mask() ^ 0xffff) + 1
        return f'IP-datagram-size < {limit}'



class TcpAck(NumberSelector):   # pylint: disable=too-few-public-methods
    """This is a convenience ``U32`` selector that matches the ``TCP ACK`` bit.
    Preconditions:

        - no IP options
        - no IP fragmentation
    """
    def __init__(self):
        """
        :meth:`__init__` expects no parameters.
        """
        super().__init__(width='u8', number=0x10, mask=0xff, offset=33)

    def get_name(self) -> Optional[str]:
        """Returns an (optional) selector name.
        """
        return "TCPACK"

    def get_description(self) -> str:
        """Returns a string describing the selector
        """
        return "TCP-ACK"


class U32FilterHandle:
    """U32 filter handle.
    """
    def __init__(self, htid: int, *, bucket: Optional[int] =0,
                        nodeid: Optional[int] = 0):
        """
        :param htid: hash table id (12-bit integer)
        :param bucket: bucket value (8-bit integer)
        :param nodeid: 12-bit integer
        """
        if htid & ~0xfff:
            raise ValueError("htid value out of range")
        self.__htid = htid
        if bucket & ~0xff:
            raise ValueError("hash value out of range")
        self.__bucket = bucket
        if nodeid & ~0xfff:
            raise ValueError("nodeid value out of range")
        self.__nodeid = nodeid & 0xfff
        self.__ident = f'{self.__htid:x}:'
        if self.__bucket != 0:
            self.__ident += f'{self.__bucket:x}'
        if self.__nodeid != 0:
            self.__ident += ':'
            self.__ident += f'{self.__nodeid:x}'

    @property
    def htid(self) -> int:
        """Hash table id
        """
        return self.__htid

    @property
    def bucket(self) -> int:
        """Bucket value (aka hash value)
        """
        return self.__bucket

    @property
    def nodeid(self) -> int:
        """Nodeid value
        """
        return self.__nodeid

    def __str__(self):
        return self.__ident

    @classmethod
    def create_from_string(cls, handle_str: str) -> 'U32FilterHandle':
        """Create a :class:`U32FilterHandle` object from a string

        :param handle_str: string containing handle with the expected
            syntax ``<num>:[<num>][:<num>]``;
            the number strings are interpreted as hexadecimal numbers

        Raises a :exc:`ValueError` if ``handle_str`` is malformed
        """
        fields = handle_str.split(':')
        n_fields = len(fields)
        if n_fields == 0 or n_fields > 3:
            raise ValueError('bad U32 filter handle')
        if not fields[0]:
            raise ValueError('bad U32 filter handle')
        htid = int(fields[0], 16)
        if n_fields == 1:
            return U32FilterHandle(htid)
        if n_fields == 2:
            bucket = int(fields[1], 16) if fields[1] else 0
            return U32FilterHandle(htid, bucket=bucket)
        bucket = int(fields[1], 16) if fields[1] else 0
        nodeid = int(fields[2], 16) if fields[2] else 0
        return U32FilterHandle(htid, bucket=bucket, nodeid=nodeid)

    @classmethod
    def parse(cls, handle_str: str) -> 'U32FilterHandle':
        """Parse a string into a :class:`U32FilterHandle` instance.

        :param handle_str: string containing handle with the expected
            syntax ``<num>:[<num>][:<num>]``;
            the number strings are interpreted as hexadecimal numbers

        :meta private:
        """
        try:
            return cls.create_from_string(handle_str)
        except ValueError as valerr:
            raise TcParsingError(
                    f"unable to parse handle: {handle_str}") from valerr


class U32IPFilter(TrafficFilter):
    """This class is used for ``U32`` filters when the ethernet frames carry
    IP datagrams. It uses an arbitrary number of selectors for matching
    against the packet fields.
    """

    def __init__(self, *,
                        prio: Optional[int] =None,
                        dest_class_handle: Optional[Handle] =None,
                        filter_handle: Optional[U32FilterHandle] =None,
                        filter_name: Optional[str] =None,
                        selectors: Optional[List[U32Selector]] =None):
        """
        :param prio: filter priority
        :param dest_class_handle: if there is a match, traffic will be
            directed to the :class:`QClass` with this :class:`Handle`
        :param filter_handle: handle of this filter
        :param filter_name: name for this filter
        :param selectors: list of :class:`U32Selector` objects specifying
            the matching criteria
        """
        super().__init__(protocol='ip', prio=prio, filter_type='u32',
                                dest_class_handle=dest_class_handle,
                                filter_name=filter_name)
        self.__filter_handle = filter_handle
        self.__selectors = selectors.copy() if selectors else []

    def get_match_name(self) -> Optional[str]:
        """Returns a string with the name that describes the traffic matched
        by the filter.
        """
        name_list = []
        for selector in self.__selectors:
            name = selector.get_name()
            if name is None:
                return None
            name_list.append(name)
        if not name_list:
            return None
        return '-'.join(name_list)

    def __str__(self):
        filter_name = (self.get_filter_name() or self.get_match_name() or "")
        prio = self.get_prio()
        return f'U32IPFilter({filter_name}:0x{prio:x})'

    def get_description(self) -> str:
        """Returns a string with detail info about the filter
        """
        filter_name = self.get_filter_name()
        if not filter_name:
            match_name = self.get_match_name()
            # The match name is derived from the selector names.
            # In the case where there are multiple selectors resulting
            # in a match name that is too long, we do not use it; the
            # description should suffice.
            if (match_name is None or
                    (len(match_name) > 20 and len(self.__selectors) > 2)):
                filter_name = "U32-IP-Filter"
            else:
                filter_name = match_name + "-Filter"
        filter_type = self.get_filter_type()
        prio = self.get_prio()
        return (f'{filter_name}({filter_type}:0x{prio:x}): ' +
                ' AND '.join([s.get_description() for s in self.__selectors]))

    def filter_creation_args(self):
        """Returns a list of **tc(8)** arguments to create this filter
        """
        args = ['u32']
        for selector in self.__selectors:
            args.append('match')
            args += selector.tc_creation_args()
        args += ['flowid', str(self.get_dest_handle())]
        return args

    def get_filter_handle(self) -> U32FilterHandle:
        """Returns the filter handle
        """
        return self.__filter_handle

    def set_filter_handle(self, filter_handle: U32FilterHandle):
        """Set the filter handle.

        Raises :class:`TcError` if the filter is instantiated.
        """
        if self.__instantiated:
            _logger.error(
                "%s: %s: attempt to set handle of instantiated filter",
                        self.set_filter_handle.__qualname__,
                        self)
            raise TcError(f"attempt to set handle of filter {self}")
        self.__filter_handle = filter_handle

    def get_selectors(self) -> List[U32Selector]:
        """Returns the selector list
        """
        return self.__selectors

    def has_selector(self, selector: U32Selector) -> bool:
        """Returns ``True`` if a selector matching ``selector``
        is included in this filter (:class:`U32Selector` objects
        support equality comparisons)
        """
        for sel in self.__selectors:
            if sel == selector:
                return True
        return False

    def add_selector(self, selector: U32Selector):
        """Add the specified selector to this filter.
        """
        if self.is_instantiated():
            raise TcError('cannot change selectors of instantiated filter')
        self.__selectors.append(selector)

    @staticmethod
    def __is_size_limit(mask_value):
        """Returns ``True`` if the specified 16-bit prefix_value has its MSB
        equal to 1 and no 0 bit between 1 bits, i.e. it looks like:
               MSB          LSB
                11111....00000
        """
        inv_value = (mask_value ^ 0xffff) & 0xffff
        return (inv_value & (inv_value + 1)) == 0

    @staticmethod
    def __make_ipv4_network(value, mask) -> IPv4Network:
        """Create an IPv4Network object from the value and mask, which
        are both strings holding hex numbers.
        """
        addr_str = str(IPv4Address(value))
        if mask != 0:
            mask_str = str(IPv4Address(mask))
        else:
            mask_str = '0'
        netstr = addr_str + '/' + mask_str
        return IPv4Network(netstr)

    # pylint: disable=too-many-branches
    @classmethod
    def _parse_u32_selector(cls, *, value: int, mask: int,
                                offset: int) -> List[U32Selector]:
        """Parse the specified parameters into one or more selectors
        """
        selector_list = []
        while True:
            # Identify the relevant packet field via the offset.
            # Extract a selector, then clear the relevant mask bits.
            # Once the mask is 0, we are done (we may extract more than
            # one selector)
            if offset == 0 and (mask & 0x0f000000) == 0x0f000000:
                selector = IPHeaderLength(((value >> 24) & 0x0f) * 4)
                mask &= 0xf0ffffff
                value &= 0xf0ffffff
            elif offset == 0 and cls.__is_size_limit(mask):
                limit = ((mask ^ 0xffff) & 0xffff) + 1
                selector = IPDatagramLimit(limit)
                mask &= 0xffff0000
                value &= 0xffff0000
            elif offset == 8 and (mask & 0x00ff0000) == 0x00ff0000:
                selector = IPProtocolSelector((value >> 16) & 0xff)
                mask &= 0xff00ffff
                value &= 0xff00ffff
            elif offset == 12:          # source IP address
                selector = IPSubnetSelector('src',
                                cls.__make_ipv4_network(value, mask))
                mask = 0
            elif offset == 16:          # source IP address
                selector = IPSubnetSelector('dst',
                                cls.__make_ipv4_network(value, mask))
                mask = 0
            elif offset == 20:    # src/dest port
                if (mask & 0xffff) == 0xffff:
                    selector = IPPortSelector('dst', value & 0xffff)
                    mask &= 0xffff0000
                    value &= 0xffff0000
                elif (mask & 0xffff0000) == 0xffff0000:
                    selector = IPPortSelector('src', (value >> 16) & 0xffff)
                    mask &= 0xffff
                    value &= 0xffff
                else:
                    selector = NumberSelector('u32', number=value,
                                        mask=mask, offset=offset)
                    mask = 0
            elif (offset == 32 and mask == 0x00ff0000 and value == 0x00100000):
                selector = TcpAck()
                mask = 0
            else:
                selector = NumberSelector('u32', number=value,
                                        mask=mask, offset=offset)
                mask = 0
            selector_list.append(selector)
            if mask == 0:
                break
        return selector_list
    # pylint: enable=too-many-branches

    @classmethod
    def _parse_selector_line(cls, field_iter) -> List[U32Selector]:
        """A selector line looks like this:
              match 00060000/00ff0000 at 8
           or
              match 00000035/0000ffff at nexthdr+0
        """
        match_spec = next(field_iter)
        value_str, mask_str = match_spec.split('/', 1)
        value = int(value_str, 16)
        mask = int(mask_str, 16)
        field = next(field_iter)
        if field != 'at':
            raise TcParsingError(f"expected 'at', found {field}")
        offset = int(next(field_iter))
        return cls._parse_u32_selector(value=value, mask=mask, offset=offset)

    # pylint: disable=too-many-branches, too-many-locals, too-many-statements
    @classmethod
    def parse(cls, filt_output: FilterOutput) -> TrafficFilter:
        """Parse the filter output in ``filt_output`` into a
        :class:`TrafficFilter` instance.

        :meta private:
        """
        #
        # When this library is used to create a U32 filter, the output
        # will have 3 lines as follows (below are the fields *after*
        # the 'u32' filter type):
        #       <empty>
        #       fh 802: ht divisor 1
        #       fh 802::800 order 2048 key ht 802 bkt 0 flowid 1:102
        #
        # Other forms are possible, e.g.
        #
        #   fh 801::800 order 2048 key ht 801 bkt 0 link 1:
        #
        # These will be ignored with a log warning.
        #
        class_handle = None
        filter_handle = None
        is_terminal = False
        for filter_line in filt_output.filter_lines_iter():
            filter_handle = None
            field_iter = iter(filter_line)
            for field in field_iter:
                try:
                    if field == 'fh':
                        filter_handle = U32FilterHandle.create_from_string(
                                                            next(field_iter))
                    elif field == 'ht':
                        # Parse the form 'ht divisor <num>'
                        field = next(field_iter)
                        if field == 'divisor':
                            _ = int(next(field_iter))
                        else:
                            raise TcParsingError(
                                    f"expecting 'divisor', found '{field}'",
                                    line=str(filter_line))
                    elif field == 'order':
                        _ = int(next(field_iter))
                    elif field == 'link':
                        _ = next(field_iter)
                    elif field == 'key':
                        # Parse the form 'key ht <num> bkt <num>'
                        field = next(field_iter)
                        if field != 'ht':
                            raise TcParsingError(
                                        f"expecting 'ht', found '{field}'",
                                        line=str(filter_line))
                        _ = int(next(field_iter), 16)
                        field = next(field_iter)
                        if field != 'bkt':
                            raise TcParsingError(
                                        f"expecting 'bkt', found '{field}'",
                                        line=str(filter_line))
                        _ = int(next(field_iter))
                    elif field == 'flowid':
                        if not is_terminal:
                            class_handle = Handle.create_from_string(
                                                        next(field_iter),
                                                        default_major=0)
                    elif field == 'terminal':
                        is_terminal = True
                    elif field == 'not_in_hw':
                        pass
                    elif field == 'chain':
                        _ = int(next(field_iter))
                    else:
                        raise TcParsingError(f"unexpected argument: {field}",
                                                line=str(filter_line))
                except ValueError as valerr:
                    line = str(filter_line)
                    reason = f"bad value for field: {field}"
                    _logger.error("%s: %s line='%s' (owner=%s)",
                            cls.parse.__qualname__, reason, line,
                            filt_output.get_filter_owner())
                    raise TcParsingError(reason, line=line) from valerr
                except StopIteration as stopiter:
                    line = str(filter_line)
                    reason = f"missing value for field: {field}"
                    _logger.error("%s: %s line='%s' (owner=%s)",
                            cls.parse.__qualname__, reason, line,
                            filt_output.get_filter_owner())
                    raise TcParsingError(reason, line=line) from stopiter
            if class_handle is not None and filter_handle is not None:
                break
        if filter_handle is None:
            reason = 'u32 filter with no handle'
            _logger.error("%s: %s (owner=%s)",
                            cls.parse.__qualname__, reason,
                            filt_output.get_filter_owner())
            raise TcParsingError('u32 filter with no handle')
        #
        # If we get here, we have a filter handle and maybe a
        # (destination) class handle.
        #
        # We now parse the non-filter lines; these lines look like this:
        #
        #       match 00000000/00000000 at 16
        #         hash mask 0000ff00 at 12
        #
        # We only handle 'match' lines here.
        #
        filter_selectors = []
        nfl_iter = filt_output.nonfilter_lines_iter()
        action_present = False
        for nonfilter_line in nfl_iter:
            # lws: leading white-space
            lws = len(nonfilter_line) - len(nonfilter_line.lstrip())
            fields = nonfilter_line.split()
            if len(fields) == 0:
                break
            if fields[0] == 'match':
                selectors = cls._parse_selector_line(iter(fields[1:]))
                filter_selectors.extend(selectors)
            elif lws >= 2:
                if fields[0] == 'action':
                    #
                    # Assume that all remaining lines are action-related
                    # (I don't know if this is always the case)
                    #
                    nfl_iter.rewind()
                    action_present = True
                    break
                _logger.warning("%s: unable to handle line: %s (owner=%s)",
                                cls.parse.__qualname__,
                                nonfilter_line, filt_output.get_filter_owner())
            elif lws == 1:
                # This is an action line; put the line back, and stop
                # processing
                nfl_iter.rewind()
                action_present = True
                break
            else:
                # This should not happen as all non-filter lines are indented
                _logger.warning("%s: unexpected line: %s (owner=%s)",
                                cls.parse.__qualname__,
                                nonfilter_line, filt_output.get_filter_owner())
        if not action_present and class_handle is None:
            _logger.warning(
                "%s: no action and no dest class for filter %s (owner=%s)",
                        cls.parse.__qualname__, filter_handle,
                        filt_output.get_filter_owner())
        return U32IPFilter(
                        prio=filt_output.get_prio(),
                        dest_class_handle=class_handle,
                        filter_handle=filter_handle,
                        selectors=filter_selectors)
    # pylint: enable=too-many-branches, too-many-locals, too-many-statements

TrafficFilterParser.register_filter(filter_type='u32', protocol='ip',
                                        klass=U32IPFilter)
