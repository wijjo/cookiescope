# Copyright (C) 2023, Steven Cooper
#
# This file is part of Cookiescope.
#
# Cookiescope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cookiescope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cookiescope.  If not, see <https://www.gnu.org/licenses/>.

"""
Cookie scope utilities.
"""

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import IO, Iterator


def warning(*messages: str):
    """
    Display warning messages.

    Args:
        messages: warning messages
    """
    for message in messages:
        sys.stderr.write(f'WARNING: {message}\n')


def error(*messages: str):
    """
    Display error messages.

    Args:
        messages: error messages
    """
    for message in messages:
        sys.stderr.write(f'ERROR: {message}\n')


def abort(*messages: str):
    """
    Display error messages and quit.

    Args:
        messages: error messages
    """
    error(*messages)
    sys.exit(1)


@contextmanager
def open_binary_file(path: Path) -> Iterator[IO]:
    try:
        with path.open('rb') as file:
            yield file
    except PermissionError:
        abort('Permission denied opening file:',
              str(path),
              'Make sure there are no foreground or background browser processes.')
    except (IOError, OSError) as exc:
        abort('Unable to open file due to exception:', str(path), str(exc))
