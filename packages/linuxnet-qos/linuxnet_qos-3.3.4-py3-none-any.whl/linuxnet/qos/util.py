# Copyright (c) 2021, Panagiotis Tsirigotis

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

"""This module provides utility functions
"""

import logging
import subprocess

from .deps import get_logger
from .exceptions import TcExecutionError

_logger = get_logger("linuxnet.qos.util")


def run_command(runner, cmd, operation, log_process_error=True):
    """Use the runner callable (which accepts the same arguments as
    subprocess.run) to execute the command in cmd.
    The operation parameter holds a description of what the command
    is supposed to do.
    """
    try:
        return runner(cmd, check=True,
                        universal_newlines=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as procerr:
        if log_process_error:
            _logger.exception("%s: %s: command failed: '%s'",
                     run_command.__qualname__,
                     operation,
                     ' '.join(cmd))
        raise TcExecutionError(operation + ' failed',
                                    procerr=procerr) from procerr
    except Exception as err:    # pylint: disable=broad-except
        _logger.exception("%s: %s: command failed: '%s'",
                     run_command.__qualname__,
                     operation,
                     ' '.join(cmd))
        raise TcExecutionError(operation + ' failed') from err

def run_subprocess(*args, **kwargs):
    """This function consumes the 'execute_always' parameter (it does
    nothing with it).

    When implementing a dryrun option for code that is using this library,
    it is useful to provide the option for some commands to be invoked
    even in dryrun mode. These are typically read-only commands like
    'tc qdisc ls'. The code that uses the output of such commands will
    set the execute_always flag to True so that the command is
    actually executed.

    Callables used in place of this function need to be aware of
    the execute_always flag.
    """
    kwargs.pop('execute_always', None)
    # pylint: disable=subprocess-run-check
    return subprocess.run(*args, **kwargs)
    # pylint: enable=subprocess-run-check


def _init_debug_logging(loglevel=logging.INFO):
    """Helper method to initialize logging to stdout
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)
    root_logger.addHandler(logging.StreamHandler())
