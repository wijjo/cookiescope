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

from typing import Iterable
from urllib.parse import unquote

from utility import abort

#: Cookie type (plain string dictionary).
Cookie = dict[str, str]
#: ORed attribute filter values.
Filter = tuple[str, list[str]]
#: ANDed filters.
FilterBy = Iterable[Filter]
#: Sort by as sequence of attribute names.
SortBy = Iterable[str]
#: Attribute display order.
ATTRIBUTE_DISPLAY_ORDER = ['domain', 'name', 'path', 'value', 'flags', 'expires', 'created']
#: Default attribute sort by "clause".
DEFAULT_SORT_BY = ['domain', 'path']


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
        filter_expr_parts = filter_expr.split('=', maxsplit=1)
        if len(filter_expr_parts) != 2 or not filter_expr_parts[1]:
            abort(f'Bad name=value filter expression: {filter_expr}')
        filters.append((filter_expr_parts[0], filter_expr_parts[1].split(',')))
    return filters


def filter_cookies(unfiltered_cookies: Iterable[Cookie],
                   filter_by: FilterBy | None,
                   ) -> Iterable[Cookie]:
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
            if name not in cookie:
                break
            for value in values:
                # Normalize comparison by un-quoting and lower-casing cookie values.
                if unquote(cookie[name]).lower().find(value) == -1:
                    break
            else:
                continue
            break
        else:
            yield cookie


def sort_cookies(unsorted_cookies: Iterable[Cookie],
                 sort_by: SortBy | None,
                 ) -> Iterable[Cookie]:
    """
    Sort cookies.

    Args:
        unsorted_cookies: unsorted input cookies
        sort_by: optional attribute names to sort by in priority order

    Returns:
        iterable sorted cookies
    """
    if sort_by is None:
        return unsorted_cookies
    return sorted(unsorted_cookies, key=lambda c: [c[k] for k in sort_by])


def display_cookies(cookies: Iterable[Cookie]):
    """
    Display cookies.

    Args:
        cookies: iterable cookies to display
    """
    for cookie in cookies:
        # Don't assume all possible keys are present in cookie.
        keys1 = [key for key in ATTRIBUTE_DISPLAY_ORDER if key in cookie]
        keys2 = sorted([key for key in cookie.keys() if key not in keys1])
        print('')
        for key in keys1 + keys2:
            print(f'{key}={unquote(cookie[key])}')
