#!/usr/bin/env python3
#
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
Cookiescope Safari browser support.
"""

from pathlib import Path
from typing import Iterable, Self

from cookiescope.extractors import generate_binary_cookies, is_binary_cookies_file
from cookiescope.cookies import Cookie, FilterBy, SortBy, filter_cookies, sort_cookies
from .base import BrowserBase, LocationMap


class SafariBrowser(BrowserBase):
    """Safari browser implementation."""

    name = 'Safari'

    cookies_paths: LocationMap = {
        'darwin': [
            '~/Library/Containers/com.apple.Safari/Data/Library/Cookies/Cookies.binarycookies',
            '~/Library/Cookies/Cookies.binarycookies',
        ],
    }

    @classmethod
    def from_file(cls, path: Path) -> Self | None:
        """Required conditional factory method."""
        return cls(path) if is_binary_cookies_file(path) else None

    @classmethod
    def find_cookies(cls, profile: str | None) -> Path | None:
        """Required method to locate the cookies file."""
        return cls.find_file(cls.cookies_paths)

    def generate_cookies(self, filter_by: FilterBy, sort_by: SortBy) -> Iterable[Cookie]:
        """Required override: query cookies with optional filtering and sorting."""
        filtered_cookies = filter_cookies(generate_binary_cookies(self.file_path), filter_by)
        return sort_cookies(filtered_cookies, sort_by)
