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
Cookiescope generic Chrome browser support.
"""

# Decryption is based on code from the following project. But the code has been
# heavily-modified and reorganized.
#
# https://github.com/n8henrie/pycookiecheat
#
# That project's code is covered by the following license:
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Nathan Henrie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
from collections import namedtuple
from pathlib import Path
from typing import Iterable, Self

from cookiescope.cookies import CookieData, FilterBy, SortBy
from cookiescope.extractors import SQLiteCookiesBase
from .base import BrowserBase, LocationMap


class GenericChromeSQLiteCookies(SQLiteCookiesBase):

    #: Required database row named tuple.
    DatabaseRow = namedtuple(
        'DatabaseRow',
        [
            'host_key',
            'name',
            'value',
            'encrypted_value',
            'path',
            'has_expires',
            'expires_utc',
            'creation_utc',
            'is_httponly',
            'is_secure',
        ],
    )

    # Ignore unresolved references due to excluded platform-specific code.
    # noinspection PyUnresolvedReferences
    def __init__(self, path: Path, name: str):
        """
        SQLiteCookies constructor.

        Args:
            path: cookies database file path
            name: browser name
        """
        if sys.platform == 'darwin':
            from cookiescope.decryptors.macos import MacOSDecryptor
            self.decryptor = MacOSDecryptor(name)
        elif sys.platform == 'linux':
            from cookiescope.decryptors.linux import LinuxDecryptor
            self.decryptor = LinuxDecryptor(name)
        else:
            assert False
        super().__init__(path, 'cookies')

    def canonicalize_row(self, row: DatabaseRow) -> SQLiteCookiesBase.CanonicalRow:
        if row.encrypted_value:
            value = self.decryptor.decrypt(row.encrypted_value)
        else:
            value = row.value
        return SQLiteCookiesBase.CanonicalRow(
            domain=row.host_key,
            name=row.name,
            value=value,
            path=row.path,
            has_expires=row.has_expires,
            expires_utc=row.expires_utc / 1000000 - 11644473600,
            creation_utc=row.creation_utc / 1000000 - 11644473600,
            httponly=row.is_httponly,
            secure=row.is_secure,
        )


class GenericChromeBrowser(BrowserBase):
    """Generic Chrome-based browser implementation."""

    name = 'Chrome (generic)'

    # Should be overridden.
    db_paths: LocationMap = {}

    def __init__(self, file_path: Path, cookies_db: GenericChromeSQLiteCookies):
        """
        Generic Chrome browser base constructor.

        Args:
            file_path: cookies file or database path
        """
        assert self.db_paths
        super().__init__(file_path)
        self.cookies_db = cookies_db

    @classmethod
    def from_file(cls, path: Path) -> Self | None:
        """Required conditional factory method."""
        cookies_db = GenericChromeSQLiteCookies(path, cls.name)
        if not cookies_db.is_cookies_db():
            return None
        return cls(path, cookies_db)

    @classmethod
    def find_cookies(cls, profile: str | None) -> Path | None:
        """Required override to locate the cookies database."""
        return cls.find_file(cls.db_paths)

    def generate_cookies(self, filter_by: FilterBy, sort_by: SortBy) -> Iterable[CookieData]:
        """Required override to generate cookies."""
        return self.cookies_db.generate_cookies(filter_by, sort_by)
