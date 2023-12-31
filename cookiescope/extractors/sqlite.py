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

import sqlite3
from abc import ABC, abstractmethod
from collections import namedtuple
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import unquote

from cookiescope.cookies import CookieData, FilterBy, SortBy, filter_cookies, sort_cookies
from cookiescope.utility import open_binary_file


class SQLiteCookiesBase(ABC):
    """Base utility class for SQLite cookie access."""

    #: Named tuple that row data is assigned to.
    CanonicalRow = namedtuple(
        'CanonicalRow',
        [
            'domain',
            'name',
            'value',
            'path',
            'has_expires',
            'expires_utc',
            'creation_utc',
            'httponly',
            'secure',
        ]
    )

    #: Must be provided by the subclass.
    DatabaseRow: namedtuple = None

    def __init__(self, path: Path, table_name: str):
        """
        SQLiteCookiesBase constructor.

        Args:
            path: database file path
            table_name: cookies table name
        """
        self.path = path
        self.table_name = table_name
        assert self.DatabaseRow is not None
        # noinspection PyProtectedMember
        columns_string = ", ".join(self.DatabaseRow._fields)
        self.cookie_query = f'SELECT {columns_string} FROM {self.table_name}'

    def is_cookies_db(self) -> bool:
        """
        Check if file is a SQLite cookies database.

        Returns:
            True if file is a SQLite database
        """
        # First sanity-check that the file can be opened at all.
        with open_binary_file(self.path):
            pass
        # Then see if we can query it as a cookies database.
        try:
            connection = sqlite3.connect(self.path)
            try:
                cursor = connection.execute(
                    f"SELECT count(*) from sqlite_master "
                    f"WHERE type = 'table' and name = '{self.table_name}'"
                )
                try:
                    return cursor.fetchone()[0] == 1
                finally:
                    cursor.close()
            finally:
                connection.close()
        except sqlite3.Error:
            return False

    @abstractmethod
    def canonicalize_row(self, row: DatabaseRow) -> CanonicalRow:
        """
        Required method to convert database row to canonical row.
        Args:
            row: database row

        Returns:
            canonical row
        """
        ...

    def generate_cookies(self,
                         filter_by: FilterBy,
                         sort_by: SortBy,
                         ) -> Iterable[CookieData]:
        """Required override: query cookies with optional filtering and sorting."""
        def _generate() -> Iterator[CookieData]:
            connection = sqlite3.connect(self.path)
            try:
                cursor = connection.cursor()
                try:
                    cursor.execute(self.cookie_query)
                    for raw_row in cursor:
                        row = self.canonicalize_row(self.DatabaseRow(*raw_row))
                        yield CookieData(
                            domain=row.domain,
                            name=row.name,
                            path=row.path,
                            value=unquote(row.value),
                            http_only=bool(row.httponly),
                            secure=bool(row.secure),
                            expires=row.expires_utc if row.has_expires else 0,
                            created=row.creation_utc,
                        )
                finally:
                    cursor.close()
            finally:
                connection.close()
        # Avoid excess memory consumption by passing generator to filtering/sorting.
        filtered_cookies = filter_cookies(_generate(), filter_by)
        return sort_cookies(filtered_cookies, sort_by)
