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
Cookiescope base browser class.
"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Self

from cookiescope.cookies import CookieData, FilterBy, SortBy

#: Mapping of platform to possible file locations.
LocationMap = dict[str, Iterable[str | Path]]


class BrowserBase(ABC):
    """Abstract browser class."""

    name: str = None

    def __init__(self, file_path: Path):
        """
        Browser base constructor.

        Args:
            file_path: cookies file or database path
        """
        self.file_path = file_path

    @classmethod
    @abstractmethod
    def from_file(cls, path: Path) -> Self | None:
        """
        Required conditional factory method..

        Args:
            path: file path

        Returns:
            browser instance if the file belongs to browser
        """
        ...

    @classmethod
    @abstractmethod
    def find_cookies(cls, profile: str | None) -> Path | None:
        """
        Required method to find the cookies file.

        Args:
            profile: optional profile name

        Returns:
            cookies file path if found
        """
        ...

    @abstractmethod
    def generate_cookies(self, filter_by: FilterBy, sort_by: SortBy) -> Iterable[CookieData]:
        """
        Required method to generate cookies with optional filtering and sorting.

        Args:
            filter_by: filters as a mapping of attribute names to filtered values
            sort_by: sort by named attributes in order provided
        """
        ...

    @classmethod
    def find_file(cls, location_map: LocationMap) -> Path | None:
        """
        Utility method to search for a file given multiple possible platform-specific paths.

        Args:
            location_map: possible file locations mapped by platform

        Returns:
            found path
        """
        if sys.platform not in location_map:
            return None
        for path in location_map[sys.platform]:
            path = Path(path).expanduser()
            if path.is_file():
                return path
        return None
