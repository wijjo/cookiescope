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
Cookiescope Google Chrome browser support.
"""

from .base import LocationMap
from .chrome_generic import GenericChromeBrowser


class ChromeBrowser(GenericChromeBrowser):
    """Chrome browser implementation."""
    name = 'Chrome'
    db_paths: LocationMap = {
        'darwin': [
            '~/Library/Application Support/Google/Chrome/Default/Cookies',
        ],
        'linux': [
            '~/.config/chrome/Cookies',
        ],
        'win32': [
            '~/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies',
        ],
    }
