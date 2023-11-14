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
Cookiescope Firefox browser support.
"""

from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path
from typing import Iterable, Self

from cookiescope.cookies import CookieData, FilterBy, SortBy
from cookiescope.extractors import SQLiteCookiesBase
from cookiescope.utility import error
from .base import BrowserBase, LocationMap


class FirefoxBrowser(BrowserBase):
    """Firefox browser implementation."""

    name = 'Firefox'

    profiles_ini_paths: LocationMap = {
        'darwin': [
            '~/Library/Application Support/Firefox/profiles.ini',
        ],
        'linux': [
            '~/.mozilla/firefox/profiles.ini',
        ],
        'win32': [
            '~/AppData/Roaming/Mozilla/Firefox/profiles.ini',
        ],
    }

    class SQLiteCookies(SQLiteCookiesBase):

        DatabaseRow = namedtuple(
            'DatabaseRow',
            [
                'host',
                'name',
                'value',
                'path',
                'expiry',
                'creationTime',
                'isHttpOnly',
                'isSecure',
            ],
        )

        def __init__(self, path: Path):
            """
            SQLiteCookies constructor.

            Args:
                path: cookies database file path
            """
            super().__init__(path, 'moz_cookies')

        def canonicalize_row(self, row: DatabaseRow) -> SQLiteCookiesBase.CanonicalRow:
            return SQLiteCookiesBase.CanonicalRow(
                domain=row.host,
                name=row.name,
                value=row.value,
                path=row.path,
                has_expires=row.expiry,
                expires_utc=row.expiry,
                creation_utc=row.creationTime / 1000000,
                httponly=row.isHttpOnly,
                secure=row.isSecure,
            )

    def __init__(self, file_path: Path, cookies_db: SQLiteCookies):
        """
        Browser base constructor.

        Args:
            file_path: cookies file or database path
        """
        super().__init__(file_path)
        self.cookies_db = cookies_db

    @classmethod
    def from_file(cls, path: Path) -> Self | None:
        """Required conditional factory method."""
        cookies_db = cls.SQLiteCookies(path)
        if not cookies_db.is_cookies_db():
            return None
        return cls(path, cookies_db)

    @classmethod
    def find_cookies(cls, profile: str | None) -> Path | None:
        """Required override to find the cookies database file."""
        # NB: Firefox seems to be a bit flakey with how it handles finding the
        # active profile. So in some cases users may need to explicitly specify
        # a profile, because the default may not actually be active.
        profiles = ConfigParser()
        profiles_ini_path = cls.find_file(cls.profiles_ini_paths)
        if profiles_ini_path is None:
            error(f'Unable to find Firefox profiles configuration.')
            return None
        parsed_files = profiles.read(profiles_ini_path)
        if not parsed_files:
            error(f'Unable to parse Firefox profiles configuration: {profiles_ini_path}')
            return None
        # Find the cookies database path.
        if profile:
            # Match specific profile.
            for section in profiles.sections():
                if profiles.get(section, 'Name', fallback=None) == profile:
                    cookies_db_path = profiles.get(section, 'Path', fallback=None)
                    if cookies_db_path is not None:
                        if profiles.get(section, 'IsRelative', fallback=None):
                            return profiles_ini_path.parent / cookies_db_path
                        return Path(cookies_db_path)
                    return None
        # Otherwise look for default profile with cookie file.
        for section in profiles.sections():
            default = profiles.get(section, 'Default', fallback=None)
            if default:
                # Handle the complication of an "Install..." profile providing
                # the active path via the "Default" attribute. That path may be
                # relative without an "IsRelative" attribute to flag as such.
                if default != '1':
                    cookies_db_path = Path(default) / 'cookies.sqlite'
                    if cookies_db_path.is_file():
                        return cookies_db_path
                    return profiles_ini_path.parent / cookies_db_path
                profile_folder = profiles.get(section, 'Path', fallback=None)
                if profile_folder:
                    if profiles.get(section, 'IsRelative', fallback=None):
                        profile_folder = profiles_ini_path.parent / profile_folder
                    else:
                        profile_folder = Path(profile_folder)
                    cookies_db_path = profile_folder / 'cookies.sqlite'
                    if cookies_db_path.is_file():
                        return cookies_db_path
        return None

    def generate_cookies(self,
                         filter_by: FilterBy,
                         sort_by: SortBy,
                         ) -> Iterable[CookieData]:
        """Required override to generate cookies."""
        return self.cookies_db.generate_cookies(filter_by, sort_by)
