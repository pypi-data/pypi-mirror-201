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

"""Exceptions raised by the QoS classes
"""

import errno
import os

from typing import Optional

class TcError(Exception):
    """Traffic control error; this is the base exception class
    for all QoS-related exceptions.
    """


class TcConfigError(TcError):
    """Raised when an error is encountered while processing the
    existing queuing discipline configuration of an interface.
    """


class TcParsingError(TcConfigError):
    """Error while parsing the output of the **tc(8)** command.
    """

    def __init__(self, *args, **kwargs):
        self.__line = kwargs.pop('line', None)
        super().__init__(*args, **kwargs)

    def set_line(self, line: str) -> None:
        """Identify the line where the parsing error happened.
        Once set, this cannot be changed.
        Note that it may be set via the constructor.
        """
        if self.__line is None:
            self.__line = line

    def get_line(self) -> Optional[str]:
        """Returns the line where the parsing error was encountered.
        """
        return self.__line

    def __str__(self):
        if self.__line:
            return super().__str__() + ": " + self.__line
        return super().__str__()


class TcExecutionError(TcError):
    """Error executing the **tc(8)** command.
    """

    __RTNETLINK_PREFIX = 'RTNETLINK answers: '
    __RTNETLINK_PREFIX_LEN = len(__RTNETLINK_PREFIX)

    __ERROR_PREFIX = 'Error: '
    __ERROR_PREFIX_LEN = len(__ERROR_PREFIX)

    def __init__(self, msg, procerr=None):
        # tc will report the string corresponding to an
        # errno value prefixed by __RTNETLINK_PREFIX for some
        # failures. We attempt to detect that and save
        # the errno value.
        self.__rtnetlink_errno = 0
        self.__error_message = None
        self.__stderr_line = None
        if procerr is not None:
            self.__init_from_stderr(procerr)
        if self.__stderr_line is not None:
            msg += ': ' + self.__stderr_line
        super().__init__(msg)

    def __init_from_stderr(self, procerr):
        """Initialize attributes from standard error
        """
        if procerr.stderr is None:
            return
        stderr_lines = procerr.stderr.strip().split('\n')
        if not stderr_lines:
            return
        self.__stderr_line = stderr_lines[0]
        # If the netlink exchange includes an error message from the kernel
        # (e.g. as seen in 4.18.0) tc will report that prefixed with the
        # __ERROR_PREFIX above. In this case, we determine the errno from
        # the message string.
        # Otherwise, if netlink exchange reports an errno value, tc will
        # report that prefixed with __RTNETLINK_PREFIX. In this case,
        # we save the error string.
        if self.__stderr_line.startswith(self.__RTNETLINK_PREFIX):
            rtnetlink_msg = self.__stderr_line[self.__RTNETLINK_PREFIX_LEN:]
            for errval in errno.errorcode:
                if os.strerror(errval) == rtnetlink_msg:
                    self.__rtnetlink_errno = errval
                    break
            else:
                self.__error_message = rtnetlink_msg
        elif self.__stderr_line.startswith(self.__ERROR_PREFIX):
            self.__error_message = self.__stderr_line[self.__ERROR_PREFIX_LEN:]

    def get_rtnetlink_errno(self):
        """Return the errno value for this error.
        If 0, no errno was detected.
        """
        return self.__rtnetlink_errno

    def get_error_message(self):
        """Return the netlink error message
        If None, no message was detected.
        """
        return self.__error_message

class TcBandwidthError(TcError):
    """Raised when a bandwidth request cannot be satisfied.
    """
