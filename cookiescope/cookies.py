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
Cookiescope cookie types and functions.
"""

from dataclasses import dataclass
from time import gmtime, strftime
from typing import Iterable
from urllib.parse import quote

from cookiescope.utility import abort, warning


@dataclass
class CookieData:
    """
    Cookie data class.

    All strings are unquoted (URL quoting escape sequences replaced).

    Field order below also determines display order.
    """
    #: Full or partial domain name.
    domain: str
    #: Cookie name.
    name: str
    #: Cookie path.
    path: str
    #: Cookie value (URL-unquoted data string).
    value: str
    #: HTTP-only flag.
    http_only: bool
    #: Is-secure flag.
    secure: bool
    #: Expiration timestamp (Unix UTC seconds since 1970).
    expires: int
    #: Creation timestamp (Unix UTC seconds since 1970 or 0).
    created: int

    def as_strings(self) -> Iterable[tuple[str, str]]:
        """
        Convert fields to (name, value) string pairs

        Returns:
            iterable (name, value) string pairs
        """
        yield 'domain', self.domain
        yield 'name', self.name
        yield 'path', self.path
        yield 'value', self.value
        yield 'http_only', str(self.http_only).lower()
        yield 'secure', str(self.secure).lower()
        if self.expires:
            yield 'expires', strftime('%c', gmtime(self.expires))
        if self.created:
            yield 'created', strftime('%c', gmtime(self.created))

    def as_cookie_file_line(self):
        """
        Convert to Netscape cookie file format line.

        See https://curl.se/docs/http-cookies.html.

        Returns:
            cookie file line
        """
        return '\t'.join([
            f'#HttpOnly_{self.domain}' if self.http_only else self.domain,
            'TRUE',     # subdomains
            self.path,
            'TRUE' if self.secure else 'FALSE',
            str(self.expires),
            self.name,
            quote(self.value),
        ])


# --- Types.
#: Filter field name and possible values handled with logical OR.
Filter = tuple[str, list[str]]
#: Multiple filters handled with logical AND.
FilterBy = Iterable[Filter]
#: Sorting specified as a sequence of field names.
SortBy = Iterable[str]

# --- Constants.
#: Field names supported for filtering.
FILTER_FIELDS = ['domain', 'name', 'path', 'value']
#: Field names supported for sorting.
SORT_FIELDS = ['domain', 'name', 'path', 'value']
#: Default sort fields.
DEFAULT_SORT_FIELDS = ['domain', 'path']


def get_filter_by(filter_exprs: Iterable[str]) -> FilterBy:
    """
    Convert name=value raw filter expressions to filter-by list.

    Values strings are HTTP-escaped. Multiple values may be comma-separated.

    Args:
        filter_exprs: name=value filter expressions

    Returns:
        dictionary mapping attribute names to lists of partial values
    """
    filters: list[Filter] = []
    for filter_expr in filter_exprs:
        expr_parts = filter_expr.split('=', maxsplit=1)
        if len(expr_parts) != 2 or not expr_parts[1] or expr_parts[0] not in FILTER_FIELDS:
            abort(f'Bad name=value filter expression: {filter_expr}')
        name, value = expr_parts
        filters.append((name, value.split(',')))
    return filters


def filter_cookies(unfiltered_cookies: Iterable[CookieData],
                   filter_by: FilterBy | None,
                   ) -> Iterable[CookieData]:
    """
    Filter cookies.

    Filters are ANDed together. Filter values are ORed together.

    Args:
        unfiltered_cookies: unfiltered input cookies
        filter_by: optional (name, values) filter pairs

    Returns:
        iterable filtered cookies
    """
    if filter_by is None:
        return unfiltered_cookies
    # Lower-case the filter values for normalized comparison.
    filter_by = [(name, [value.lower() for value in values]) for name, values in filter_by]
    for cookie in unfiltered_cookies:
        for name, values in filter_by:
            if name not in FILTER_FIELDS:
                warning(f'Ignoring bad filter field name: {name}')
                break
            for value in values:
                # Normalize comparison by lower-casing cookie values.
                if getattr(cookie, name).lower().find(value) == -1:
                    break
            else:
                continue
            break
        else:
            yield cookie


def sort_cookies(unsorted_cookies: Iterable[CookieData],
                 sort_by: SortBy | None,
                 ) -> Iterable[CookieData]:
    """
    Sort cookies.

    Args:
        unsorted_cookies: unsorted input cookies
        sort_by: optional attribute names to sort by in priority order

    Returns:
        iterable sorted cookies
    """
    if not sort_by:
        return unsorted_cookies
    bad_fields: list[str] = []
    sort_fields: list[str] = []
    for sort_field in sort_by:
        if sort_field in SORT_FIELDS and sort_field not in sort_fields:
            sort_fields.append(sort_field)
        else:
            bad_fields.append(sort_field)
    if bad_fields:
        warning(f'Ignoring bad sort field(s): {" ".join(bad_fields)}')
    if not sort_fields:
        return unsorted_cookies

    def get_sort_values(cookie: CookieData) -> list[str]:
        return [getattr(cookie, name) for name in sort_fields]

    return sorted(unsorted_cookies, key=get_sort_values)


def display_cookies(cookies: Iterable[CookieData], heading: str = None):
    """
    Display cookies.

    Args:
        cookies: iterable cookies to display
        heading: optional heading to display
    """
    if heading:
        print(f'=== {heading} ===')
    for cookie in cookies:
        print('')
        for name, value in cookie.as_strings():
            print(f'{name}={value}')


def display_cookie_jar(cookies: Iterable[CookieData]):
    """
    Display cookie jar, i.e. Netscape format text cookies.

    https://curl.se/docs/http-cookies.html

    Args:
        cookies: cookies to display
    """

    for cookie in cookies:
        print(cookie.as_cookie_file_line())
