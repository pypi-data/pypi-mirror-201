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

"""
This module contains parsers to create Python objects from the output
of the **tc(8)** command.
"""

from collections import deque
from typing import Any, Callable, Iterator, List, Optional

from .deps import get_logger
from .exceptions import TcError, TcParsingError
from .handle import Handle


_logger = get_logger("linuxnet.qos.parsers")


class LookaheadIterator:
    """A LookaheadIterator is an iterator that provides the ability to
    put back previously returned tokens.

    Conceptual view of the LookaheadIterator::

                               deque
       +---------------+  +---+---+---+---+---+
       | back-iterator |  | T | T | T |...| T |
       +---------------+  +---+---+---+---+---+
                                ^
                                |
                              Cursor

    * Tokens to the right of the cursor have been consumed.
    * Tokens up to, but not including, the cursor are previously consumed
      tokens that have been put back.
    * New tokens are obtained from the back-iterator.
    * The value of the cursor indicates the number of put-back tokens.
    * The maximum size of the deque is equal to the lookahead.
    """
    def __init__(self, iterable, lookahead: int):
        """
        :param iterable: an iterable object from which we create
            the back-iterator
        :param lookahead: number of tokens of look ahead
        """
        self.__iter = iter(iterable)
        if lookahead <= 0:
            raise ValueError(f'bad lookahead value {lookahead}')
        self.__tokens = deque(maxlen=lookahead)
        self.__cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__cursor == 0:
            token = next(self.__iter)
            self.__tokens.appendleft(token)
        else:
            self.__cursor -= 1
            token = self.__tokens[self.__cursor]
        return token

    def peek(self) -> Optional[Any]:
        """Returns the next token, but does not consume it
        """
        try:
            token = self.__next__()
            self.put_back(token)
            return token
        except StopIteration:
            return None

    def put_back(self, token: str) -> None:
        """Put back the specified token. This must be a token previously
        returned by the iterator (identity is checked, not equality)
        """
        if self.__cursor == len(self.__tokens):
            # Either there are no consumed tokens, or this is an attempt to
            # put back one more tokens than those already consumed.
            raise ValueError('not a consumed token')
        if token is not self.__tokens[self.__cursor]:
            raise ValueError('wrong token')
        self.__cursor += 1

    def rewind(self, step=1) -> 'LookaheadIterator':
        """Put back last ``step`` tokens

        A :exc:`ValueError` will be raised if there are not enough
        tokens to put back.
        """
        avail = len(self.__tokens) - self.__cursor
        if step > avail:
            raise ValueError(f'unable to rewind {step} token(s)')
        self.__cursor += step
        return self


class LineGroupIterator:
    """The LineGroupIterator is used to parse the output of
    ``tc filter ls``. It returns lines one-by-one and is capable of
    single-level backtracking. This allows the filter-specific
    parsing code to return a line back to the iterator if it
    does not belong to it.
    """
    def __init__(self, tc_output: List[str]):
        self.__line_iter = iter(tc_output)
        self.__backtracked_line = None
        self.__current_line = None
        self.__field_iter = None

    def __iter__(self):
        return self

    def __next__(self) -> str:
        """Returns either the backtracked line or the next line from
        the sub-iterator
        """
        if self.__backtracked_line is None:
            self.__current_line = next(self.__line_iter)
        else:
            self.__current_line = self.__backtracked_line
            self.__backtracked_line = None
        self.__field_iter = None
        return self.__current_line

    def next_field(self) -> str:
        """Returns the next field of the current line
        """
        return next(self.get_field_iter())

    def get_field_iter(self) -> Iterator[str]:
        """Returns an iterator over the fields of the current line
        """
        if self.__current_line is None:
            raise TcError("attempt to access next field before line iteration")
        if self.__field_iter is None:
            self.__field_iter = LookaheadIterator(
                                        self.__current_line.split(), 1)
        return self.__field_iter

    def clear_field_iter(self):
        """This method removes the field iterator so that a call
        to :meth:`get_field_iter` will create a new one to scan
        the line from the beginning.
        """
        self.__field_iter = None

    def get_last_line(self) -> str:
        """Returns the last line returned by :meth:`__next__`
        """
        return self.__current_line

    def backtrack(self) -> None:
        """Backtrack the current line.
        """
        if self.__backtracked_line is not None:
            _logger.error("%s: attempt to backtrack twice; current line: %s",
                self.backtrack.__qualname__, self.__backtracked_line)
            raise TcError('attempt to backtrack twice')
        self.__backtracked_line = self.__current_line
        self.__current_line = None
        self.__field_iter = None


class FilterOutputLine:
    """A class that holds a line of filter output.

    One can iterate over the fields of the line::

        def parse_fields(fline: FilterOutputLine):
            for field in fline:
                if field == 'xxx':
                    ...

    The entire line can be returned by using the :func:`str` builtin function.
    """
    def __init__(self, line: str, fields: List[str]):
        """
        :param line: the complete **tc(8)** filter line
        :param fields: list of fields of the line **after** the filter type
        """
        self.__line = line
        self.__fields = fields

    def __iter__(self):
        return iter(self.__fields)

    def __str__(self):
        return self.__line


class FilterOutput:
    """An instance of this class contains the **tc(8)** output for a
    single filter.
    """
    def __init__(self, proto: str, prio: int, filter_type: str, owner: 'QNode'):
        """
        :param proto: filter protocol
        :param prio: filter priority
        :param filter_type: filter type
        :param owner: :class:`QDisc`/:class:`QClass` that owns the filter
        """
        self.__proto = proto
        self.__prio = prio
        self.__filter_type = filter_type
        self.__owner = owner
        # The __filter_lines are the lines starting with the word 'filter'
        # The __nonfilter_lines are the rest.
        self.__filter_lines = []
        self.__nonfilter_lines = []
        self.__nonfilter_lines_iter = None

    def matches(self, proto: str, prio: int, filter_type: str) -> bool:
        """Returns ``True`` if the ``proto``, ``prio``, ``filter_type``
        parameters match with the corresponding attributes of this object.

        :meta private:
        """
        return (self.__proto == proto and self.__prio == prio and
                                        self.__filter_type == filter_type)

    def get_prio(self) -> int:
        """Returns the priority value
        """
        return self.__prio

    def get_proto(self) -> str:
        """Returns the protocol value
        """
        return self.__proto

    def get_filter_type(self) -> str:
        """Returns the filter type
        """
        return self.__filter_type

    def get_filter_owner(self) -> 'QNode':
        """Returns the :class:`QDisc`/:class:`QClass` that owns the filter
        """
        return self.__owner

    def get_first_line(self) -> str:
        """Returns the first line from the **tc(8)** output for this filter
        """
        return str(self.__filter_lines[0])

    def has_nonfilter_lines(self) -> bool:
        """Returns ``True`` if the filter output has any lines not
        starting with the word ``filter``
        """
        return bool(self.__nonfilter_lines)

    def has_actions(self) -> bool:
        """Returns ``True`` if the filter has any actions.

        We assume that any remaining non-filter lines
        are action lines.

        :meta private:
        """
        return (self.has_nonfilter_lines() and
                        self.nonfilter_lines_iter().peek() is not None)

    def add_filter_line(self, line: str, fields: List[str]) -> None:
        """Add a line that starts with ``filter ``

        :meta private:
        """
        self.__filter_lines.append(FilterOutputLine(line, fields))

    def add_line(self, line: str) -> None:
        """Add a non-filter prefixed line

        :meta private:
        """
        self.__nonfilter_lines.append(line)

    def filter_lines_iter(self) -> Iterator[FilterOutputLine]:
        """Returns an iterator that returns :class:`FilterOutputLine`
        instances.
        """
        return iter(self.__filter_lines)

    def nonfilter_lines_iter(self) -> Iterator[str]:
        """Returns an iterator that returns lines (strings)
        """
        if self.__nonfilter_lines_iter is None:
            self.__nonfilter_lines_iter = LookaheadIterator(
                                                self.__nonfilter_lines, 1)
        return self.__nonfilter_lines_iter

    def dump(self, path) -> None:
        """Append the contents of this object to the file at path.
        This is used for debugging.

        :meta private:
        """
        with open(path, "a", encoding='utf-8') as outf:
            for line in self.__filter_lines:
                outf.write(str(line) + '\n')
            for line in self.__nonfilter_lines:
                outf.write(line + '\n')
            outf.write("------------------\n")


def field_advance(producer: Callable[[], str], expected_field: str,
                                has_value=True) -> Optional[str]:
    """We are expecting the next field to be ``expected_field`` optionally
    followed by its value.
    We return that value, or ``None``.
    """
    next_field = None
    try:
        next_field = producer()
        if next_field != expected_field:
            _logger.error("%s: expected '%s', found '%s'",
                field_advance.__qualname__, expected_field, next_field)
            raise TcParsingError(f"expecting '{expected_field}'")
        return producer() if has_value else None
    except StopIteration as stopit:
        if next_field is None:
            raise TcParsingError(f'missing {expected_field}') from stopit
        raise TcParsingError(f'no value for {expected_field}') from stopit


class TrafficFilterParser:
    """Helper class that creates :class:`TrafficFilter` objects from the
    output of the **tc(8)** command.
    """

    #
    # Key: the tuple (filter_type, protocol) - both strings
    # Value: a TrafficFilter subclass
    #
    _filter_class_map = {}

    #
    # Key: the action name (a string)
    # Value: a TrafficAction subclass
    #
    _action_class_map = {}

    def __init__(self, allow_parsing_errors: bool):
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        self.__filter_list = []
        # __iter is a LineGroupIterator
        self.__iter: LineGroupIterator = None

    @classmethod
    def register_filter(cls, *, filter_type: str, protocol: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`TrafficFilter` class).

        This method is intended to be used for adding support for new
        traffic filter types.

        :param filter_type: a **tc(8)** filter type, e.g. ``u32``
        :param protocol: a **tc(8)** protocol name, e.g. ``ip``
        :param klass: the Python class for this ``(filter_type, protocol)``
        """
        cls._filter_class_map[(filter_type, protocol)] = klass

    @classmethod
    def register_action(cls, *, action_name: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`TrafficAction` class).

        This method is intended to be used for adding support for new
        traffic actions.

        :param action_name: **tc(8)** action, e.g. ``police``
        :param klass: the Python class for this action
        """
        cls._action_class_map[action_name] = klass

    @classmethod
    def parse_action(cls, fields: List[str],
                        nfl_iter: Iterator[str]) -> 'TrafficAction':
        """Parse the **tc(8)** output for a traffic action.

        :param fields: fields of the output line identifying the action
            and its arguments; ``fields[0]`` is the action type
        :param nfl_iter: iterator returning the lines after the lines
            that start with 'filter'
        :rtype: a :class:`TrafficAction` instance

        Raises a :exc:`TcParsingError` if unable to parse the action
        """
        action_name = fields[0]
        klass = cls._action_class_map.get(action_name)
        if klass is None:
            raise TcParsingError(f"unknown action {action_name}")
        return klass.parse(fields[1:], nfl_iter)

    def __parse_actions(self, filt_output: FilterOutput,
                                traffic_filter: 'TrafficFilter') -> None:
        """Parse the actions in the FilterOutput
        """
        nfl_iter = filt_output.nonfilter_lines_iter()
        for nonfilter_line in nfl_iter:
            action = None
            try:
                line = nonfilter_line.strip()
                fields = line.split()
                if fields[0] == 'action':
                    if fields[1] != 'order' or len(fields) < 4:
                        raise TcParsingError(
                                        "unable to parse filter action line",
                                        line=nonfilter_line)
                    action = self.parse_action(fields[3:], nfl_iter)
                elif fields[0] == 'police':
                    action = self.parse_action(fields, nfl_iter)
                else:
                    raise TcParsingError(
                            f'unknown field in non-filter line: {fields[0]}',
                            line=nonfilter_line)
                if action is not None:
                    traffic_filter.add_action(action)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                if not self.__allow_parsing_errors:
                    raise
                _logger.warning("action parsing error, '%s'", parserr)

    def __process_filter(self, filt_output: FilterOutput) -> None:
        """Try to create a new :class:`TrafficFilter` from ``filt_output``.
        """
        #
        # Currently we only support 'ip' filters
        #
        line = filt_output.get_first_line()
        protocol = filt_output.get_proto()
        if protocol != 'ip':
            _logger.error("found protocol '%s', expected 'ip' (owner=%s)",
                        protocol, filt_output.get_filter_owner())
            raise TcParsingError(
                f"unable to handle protocol '{protocol}'", line=line)
        filter_type = filt_output.get_filter_type()
        klass = self._filter_class_map.get((filter_type, protocol))
        if klass is None:
            _logger.error("unable to handle filter type '%s' (owner=%s)",
                        filter_type, filt_output.get_filter_owner())
            raise TcParsingError(
                f"unable to handle filter type '{filter_type}'", line=line)
        traffic_filter = klass.parse(filt_output)
        if filt_output.has_actions():
            self.__parse_actions(filt_output, traffic_filter)
        if traffic_filter.get_dest_handle() is None:
            _logger.warning("filter %s has no dest handle (owner=%s)",
                traffic_filter, filt_output.get_filter_owner())
        traffic_filter._mark_as_instantiated()
        self.__filter_list.append(traffic_filter)

    def __advance(self, field_name: str, has_value=True) -> Optional[str]:
        """We are expecting the next field to be ``field_name``
        optionally followed by its value.
        We return that value.
        """
        # Note that self.__iter.next_field is a callable
        return field_advance(self.__iter.next_field, field_name, has_value)

    def parse_output(self, tc_output_lines: List[str],
                                        owner: 'QNode') -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`TrafficFilter` objects; the list can be accessed via
        the :meth:`get_filter_list` method.

        :meta private:
        """
        self.__filter_list = []
        self.__iter = LineGroupIterator(tc_output_lines)
        #
        # Process lines into FilterOutput objects.
        # Each FilterOutput object has the lines of one filter.
        # Once all lines of a filter are seen, invoke the
        # filter's parse method to create the TrafficFilter object.
        #
        filt_output = None
        for line in self.__iter:
            if not line.startswith('filter '):
                if filt_output is None:
                    _logger.error("unexpected filter line: '%s' (owner=%s)",
                                        line, owner)
                    raise TcParsingError('unexpected filter line', line=line)
                filt_output.add_line(line)
                continue
            #
            # We expect a filter line to look like this:
            #   filter protocol <val> pref <int> <type>
            #
            try:
                _ = self.__advance('filter', has_value=False)
                protocol = self.__advance('protocol')
                priostr = self.__advance('pref')
                try:
                    prio = int(priostr)
                except ValueError as valerr:
                    _logger.error("bad filter priority: %s (owner=%s)",
                        priostr, owner)
                    raise TcParsingError(
                        f'bad filter priority: {priostr}') from valerr
                try:
                    filter_type = self.__iter.next_field()
                except StopIteration as stopit:
                    _logger.error(
                        "filter line without filter type: '%s' (owner=%s)",
                            line, owner)
                    raise TcParsingError("missing filter type") from stopit
                if filt_output is None:
                    filt_output = FilterOutput(protocol, prio,
                                                        filter_type, owner)
                    filt_output.add_filter_line(line,
                                    fields=list(self.__iter.get_field_iter()))
                    continue
                if filt_output.matches(protocol, prio, filter_type):
                    filt_output.add_filter_line(line,
                                    fields=list(self.__iter.get_field_iter()))
                    continue
                #
                # Beginning of output for a new filter.
                # Process the one we have.
                #
                self.__process_filter(filt_output)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                parserr.set_line(line)
                if not self.__allow_parsing_errors:
                    raise
                _logger.warning("allowing filter parsing error: %s (owner=%s)",
                                        parserr, owner)
            filt_output = FilterOutput(protocol, prio, filter_type, owner)
            filt_output.add_filter_line(line,
                            fields=list(self.__iter.get_field_iter()))
        if filt_output is not None:
            try:
                self.__process_filter(filt_output)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                parserr.set_line(filt_output.get_first_line())
                if not self.__allow_parsing_errors:
                    raise
                _logger.warning("allowing filter parsing error: %s (owner=%s)",
                                        parserr, owner)

    def get_error_count(self) -> int:
        """Returns number of parsing errors encountered

        :meta private:
        """
        return self.__parsing_errors

    def get_filter_list(self) -> List['TrafficFilter']:
        """Returns a list of :class:`TrafficFilter` objects from the
        parsed output

        :meta private:
        """
        return self.__filter_list

    def get_filter(self) -> Optional['TrafficFilter']:
        """Returns the first :class:`TrafficFilter` from the parsed output,
        or ``None`` if no filter was successfully parsed.

        :meta private:
        """
        return self.__filter_list[0] if self.__filter_list else None


def _group_split(lines: List[str], marker: str) -> List[List[str]]:
    """Given a list of lines, break them into groups of
    consecutive lines, where the first line of each group starts with
    the ``marker`` string.
    """
    group_list = []
    line_group = []
    for line in lines:
        if not line:
            continue
        if line.startswith(marker):
            # Beginning of new line group
            if line_group:
                group_list.append(line_group)
                line_group = []
            line_group.append(line)
        else:
            if line_group:
                line_group.append(line)
            else:
                raise TcParsingError(
                    f"first line does not start with '{marker}'", line=line)
    if line_group:
        group_list.append(line_group)
    return group_list


class QClassOutput:
    """Helper class used for parsing ``tc class ls`` output for a single qclass
    """
    def __init__(self, line_group: List[str]):
        """
        :param line_group: list of lines, guaranteed not to be empty
        """
        self.__line_iter = LineGroupIterator(line_group)
        self.__handle = None
        self.__parent_handle = None
        self.__qclass_line = None
        self.__qdisc_handle = None

    def get_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the queuing class.
        """
        return self.__handle

    def get_parent_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the parent of the
        queuing class.
        """
        return self.__parent_handle

    def get_qdisc_handle(self) -> Optional[Handle]:
        """Returns the :class:`Handle` of a (leaf) qdisc
        """
        return self.__qdisc_handle

    def get_linegroup_iter(self) -> LineGroupIterator:
        """Returns the LineGroupIterator for the tc output lines.

        :meta private:
        """
        return self.__line_iter

    def get_class_line(self) -> str:
        """Returns the **tc(8)** output class line
        """
        return self.__line_iter.get_last_line()

    def get_field_iter(self) -> Iterator[str]:
        """Return an iterator for the (remaining) fields of the class line
        """
        return self.__line_iter.get_field_iter()

    def parse_first_line(self) -> str:
        """Parse the first line and return a string with the qdisc type
        (e.g. 'htb')

        :meta private:
        """
        if self.__qclass_line is not None:
            raise TcError('attempt to parse first line twice')
        self.__qclass_line = next(self.__line_iter)
        field_iter = self.get_field_iter()
        try:
            #
            # All class lines have the form:
            #
            # class <type> <handle> parent <handle> [leaf <qdisc-handle>] ...
            #
            # where the ... part is type-specific
            #
            if next(field_iter) != 'class':
                raise TcParsingError("line does not start with 'class'")
            qdisc_type = next(field_iter)
            # The handle string may not include a major number, e.g.
            #    class mq :1 root
            # or
            #    class mq :1 parent 10:
            #
            # We need to parse the parent handle before we can
            # parse the class handle. If the parent is root, we assume
            # the major number is 0 (so the class handle for the first
            # line will be 0:1)
            handle_str = next(field_iter)
            try:
                handle = Handle.parse(handle_str)
            except TcParsingError:
                handle = None
            parent_field = next(field_iter)
            if parent_field == 'root':
                parent_major = 0 if handle is None else handle.major
                self.__parent_handle = Handle.qdisc_handle(parent_major)
            elif parent_field == 'parent':
                self.__parent_handle = Handle.parse(next(field_iter))
            else:
                raise TcParsingError(
                    f"cannot determine class parent from field {parent_field}")
            if handle is None:
                self.__handle = Handle.parse(handle_str,
                                    default_major=self.__parent_handle.major)
            else:
                self.__handle = handle
            if field_iter.peek() == 'leaf':
                _ = next(field_iter)
                self.__qdisc_handle = Handle.parse(next(field_iter))
            return qdisc_type
        except StopIteration as stopit:
            raise TcParsingError("not enough fields") from stopit


class QClassParser:
    """Helper class that creates :class:`QClass` objects from the
    output of the **tc(8)** command.
    """

    _qclass_map = {}

    def __init__(self, allow_parsing_errors: bool):
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        self.__qclass_list = []

    def get_error_count(self) -> int:
        """Returns number of parsing errors encountered

        :meta private:
        """
        return self.__parsing_errors

    @classmethod
    def register_qclass(cls, ident: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`QClass` class).

        This method is intended to be used for adding support for new
        queuing discipline classes.

        :param ident: the queuing class name that appears in the
            ``tc -s class ls`` output.
        :param klass: the Python class for this queuing class
        """
        cls._qclass_map[ident] = klass

    def parse_output(self, tc_output_lines: List[str]) -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`QClass` objects; the list can be accessed via
        the :meth:`get_qclass_list` method.

        :meta private:
        """
        self.__qclass_list = []
        for line_group in _group_split(tc_output_lines, 'class '):
            qclass_output = QClassOutput(line_group)
            try:
                qdisc_type = qclass_output.parse_first_line()
                klass = self._qclass_map.get(qdisc_type)
                if klass is None:
                    if qdisc_type == 'sfq':
                        # SFQ is classless, so this should never happen;
                        # yet on CentOS 6.10, I observed the following in
                        # the output of 'tc class ls':
                        #
                        # class sfq 202:2c9 parent 202:
                        #
                        # 202: was a SFQ qdisc; the class minor number
                        # changed for every invocation of 'tc class ls'
                        _logger.warning("classless SFQ has a class: %s",
                                qclass_output.get_class_line())
                        continue
                    raise TcParsingError(f"unknown qdisc type {qdisc_type}")
                qclass = klass.parse(qclass_output)
                qclass._parse_stats(qclass_output.get_linegroup_iter())
                self.__qclass_list.append(qclass)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                line = qclass_output.get_class_line()
                if not self.__allow_parsing_errors:
                    parserr.set_line(line)
                    raise
                _logger.warning("%s: parsing error, line='%s'",
                    self.parse_output.__qualname__, line)

    def get_qclass_list(self) -> List['QClass']:
        """Returns a list of :class:`QClass` objects from the
        parsed output

        :meta private:
        """
        return self.__qclass_list

    def get_qclass(self) -> Optional['QClass']:
        """Returns the first :class:`QClass` from the parsed output,
        or ``None`` if no queuing class was successfully parsed.

        :meta private:
        """
        return self.__qclass_list[0] if self.__qclass_list else None


class QDiscOutput:
    """Helper class used for parsing ``tc qdisc ls`` output for a single qdisc
    """
    def __init__(self, line_group: List[str]):
        """
        :param line_group: list of lines, guaranteed not to be empty
        """
        self.__line_iter = LineGroupIterator(line_group)
        self.__handle = None
        self.__parent_handle = None
        self.__refcnt = None
        self.__qdisc_line = None

    def get_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the queuing discipline.
        """
        return self.__handle

    def get_parent_handle(self) -> Optional[Handle]:
        """Returns the (parsed) :class:`Handle` of the parent of this
        queueing discipline, or ``None`` if this is a root qdisc
        """
        return self.__parent_handle

    def get_refcnt(self) -> Optional[int]:
        """Returns reference count of qdisc (``None`` for non-root qdiscs,
        and for some root qdiscs like ``mq``)
        """
        return self.__refcnt

    def get_linegroup_iter(self) -> LineGroupIterator:
        """Returns the LineGroupIterator for the tc output lines.

        :meta private:
        """
        return self.__line_iter

    def get_qdisc_line(self) -> str:
        """Returns the **tc(8)** output qdisc line
        """
        return self.__line_iter.get_last_line()

    def get_field_iter(self) -> Iterator[str]:
        """Return an iterator for the (remaining) fields of the qdisc line
        """
        return self.__line_iter.get_field_iter()

    def parse_first_line(self) -> str:
        """Parse the first line and return a string with the qdisc type
        (e.g. 'htb')

        :meta private:
        """
        if self.__qdisc_line is not None:
            raise TcError('attempt to parse first line twice')
        self.__qdisc_line = next(self.__line_iter)
        field_iter = self.__line_iter.get_field_iter()
        try:
            #
            # All qdisc lines have the form:
            #
            # qdisc <type> <handle> (root refcnt <num> |parent <handle>) ...
            #
            # where the ... part is type-specific
            #
            if next(field_iter) != 'qdisc':
                raise TcParsingError("line does not start with 'qdisc'")
            qdisc_type = next(field_iter)
            self.__handle = Handle.parse(next(field_iter))
            parent_field = next(field_iter)
            if parent_field == 'root':
                # Some root qdiscs like 'mq' do not provide a refcount
                next_field = next(field_iter, None)
                if next_field is None:
                    return qdisc_type
                if next_field != 'refcnt':
                    raise TcParsingError(
                        f"found '{next_field}' after 'root' "
                        "instead of 'refcnt'")
                self.__refcnt = int(next(field_iter))
            elif parent_field == 'parent':
                self.__parent_handle = Handle.parse(next(field_iter),
                                            default_major=self.__handle.major)
            else:
                raise TcParsingError(
                    f"cannot determine qdisc parent from field {parent_field}")
            return qdisc_type
        except StopIteration as stopit:
            raise TcParsingError("not enough fields") from stopit


class QDiscParser:
    """Helper class that creates :class:`QDisc` objects from the
    output of the **tc(8)** command.
    """

    _qdisc_class_map = {}

    def __init__(self, allow_parsing_errors: bool):
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        self.__qdisc_list = []

    def get_error_count(self) -> int:
        """Returns number of parsing errors encountered

        :meta private:
        """
        return self.__parsing_errors

    @classmethod
    def register_qdisc(cls, ident: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`QDisc` class).

        This method is intended to be used for adding support for new
        queuing disciplines.

        :param ident: the qdisc name that appears in the
            ``tc -s qdisc ls`` output.
        :param klass: the Python class for this queuing discipline
        """
        cls._qdisc_class_map[ident] = klass

    def parse_output(self, tc_output_lines: List[str]) -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`QDisc` objects; the list can be accessed via
        the :meth:`get_qdisc_list` method.

        :meta private:
        """
        #
        # High-level logic:
        #   - parse the output into line groups, one for each qdisc; parsing
        #     is at the syntactic level only
        #   - for each group, determine the particular qdisc and let it
        #     parse the output
        #
        # Parsing requirements:
        #  1. The 1st line needs to be partially parsed to determine the
        #     specific qdisc
        #  2. The next 2 lines (with stats) can be parsed by common code
        #     because they are the same across qdisc's
        #  3. Give the option to the qdisc-specific parsing code to parse
        #     the whole output
        #  4. Give the option to the qdisc-specific code to use the
        #     common parsing code
        #
        # Based on the above, the QDiscOutput object contains the common
        # parsing code. Consequently, it also holds parsed fields
        # (like handles etc.)
        #
        self.__qdisc_list = []
        for line_group in _group_split(tc_output_lines, 'qdisc '):
            qdisc_output = QDiscOutput(line_group)
            try:
                qdisc_type = qdisc_output.parse_first_line()
                klass = self._qdisc_class_map.get(qdisc_type)
                if klass is None:
                    raise TcParsingError(f"unknown qdisc {qdisc_type}")
                qdisc = klass.parse(qdisc_output)
                qdisc._parse_stats(qdisc_output.get_linegroup_iter())
                self.__qdisc_list.append(qdisc)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                line = qdisc_output.get_qdisc_line()
                if not self.__allow_parsing_errors:
                    parserr.set_line(line)
                    raise
                _logger.warning("%s: parsing error, line='%s'",
                    self.parse_output.__qualname__, line)

    def get_qdisc_list(self) -> List['QDisc']:
        """Returns a list of :class:`QDisc` objects from the
        parsed output

        :meta private:
        """
        return self.__qdisc_list

    def get_qdisc(self) -> Optional['QDisc']:
        """Returns the first :class:`QDisc` from the parsed output,
        or ``None`` if no queuing discipline was successfully parsed.

        :meta private:
        """
        return self.__qdisc_list[0] if self.__qdisc_list else None
