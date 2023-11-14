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
Cookie scope.

Queries and displays browser cookies.

See command line help text for more information.

Binary cookies parsing code was originally based on this project:

https://github.com/ktnjared/BinaryCookieReader.git

It has been heavily modified and expanded here. The original code is probably
not recognizable at this point.
"""

import argparse
import os
from pathlib import Path

from browsers import (
    BrowserBase,
    ChromeBrowser,
    ChromiumBrowser,
    EdgeBrowser,
    FirefoxBrowser,
    GenericChromeBrowser,
    SafariBrowser,
)
from cookies import (
    DEFAULT_SORT_FIELDS,
    display_cookies,
    display_cookie_jar,
    get_filter_by,
)
from utility import abort


#: Command line help description.
CLI_DESCRIPTION = 'Cookie query tool.'
#: Command line help epilog text.
CLI_EPILOG = '''
Cookie source can be a browser name, e.g. "safari", or a cookies file path. A
browser name can followed by ":<profile>" to specify a user profile. E.g.
"firefox:lucy" targets the Firefox profile named "lucy". Otherwise it works with
the default profile.

Filter values match full or partial attribute values. Multiple filter values can
be comma-separated. For the comparison, filter values are HTTP-quoted and
lower-cased, and cookie fields are HTTP-unquoted and also lower-cased.

If you have problems accessing an existing cookies file try quitting all running
browser processes. Some processes may be running in the background, even when
there are no visible windows.

Frequently-used attribute names:
  * value - primary cookie data field
  * name - cookie name
  * domain - website domain responsible for cookie
  * path - website location path string

The following named browsers are supported:
'''.strip()
#: Cookie source argument help.
COOKIE_SOURCE_HELP = 'cookies path or browser[:profile]'
FILTER_HELP = 'name=value expression for filtering on cookie fields'


NAMED_BROWSERS: dict[str, type[BrowserBase]] = {
    'chrome': ChromeBrowser,
    'chromium': ChromiumBrowser,
    'edge': EdgeBrowser,
    'firefox': FirefoxBrowser,
    'safari': SafariBrowser,
}

FILE_CHECK_BROWSERS: list[type[BrowserBase]] = [
    GenericChromeBrowser,
    FirefoxBrowser,
    SafariBrowser,
    ChromiumBrowser,
]


def get_browser_for_cookie_source(cookie_source: str) -> BrowserBase:
    """
    Get browser object based on cookie source (file path or browser name).

    Args:
        cookie_source: file path or browser name

    Returns:
        browser object for processing query
    """
    if os.path.isfile(cookie_source):
        file_path = Path(cookie_source)
        for browser_class in FILE_CHECK_BROWSERS:
            browser = browser_class.from_file(file_path)
            if browser is not None:
                return browser
        abort('Unable to identify browser for file provided.')
    if os.path.sep in cookie_source:
        abort('File not found.')
    cookie_source_parts = cookie_source.lower().split(':', maxsplit=1)
    if len(cookie_source_parts) == 2:
        browser_name, profile = cookie_source_parts
    else:
        browser_name, profile = cookie_source_parts[0], None
    browser_name = browser_name.lower()
    if browser_name not in NAMED_BROWSERS:
        abort(f'Browser not supported: {browser_name}')
    browser_class = NAMED_BROWSERS[browser_name]
    file_path = browser_class.find_cookies(profile)
    if file_path is None:
        abort(f'{browser_class.name} cookies file not found.')
    browser = browser_class.from_file(file_path)
    if browser is None:
        abort(f'{browser_class.name} browser class did not recognize cookies file.',
              str(file_path))
    return browser


def main():
    """Main function."""
    epilog_parts = [CLI_EPILOG] + [f'  - {name}' for name in sorted(NAMED_BROWSERS.keys())]
    arg_parser = argparse.ArgumentParser(
        description=CLI_DESCRIPTION,
        epilog=os.linesep.join(epilog_parts),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_parser.add_argument(dest='COOKIE_SOURCE', help=COOKIE_SOURCE_HELP)
    arg_parser.add_argument(dest='FILTER', nargs='*', help=FILTER_HELP)
    arg_parser.add_argument('-j', '--jar', dest='JAR', action='store_true',
                            help='generate Netscape cookie jar format, e.g. for use with "curl"')
    args = arg_parser.parse_args()
    filter_by = get_filter_by(args.FILTER)
    browser = get_browser_for_cookie_source(args.COOKIE_SOURCE)
    cookies = browser.generate_cookies(filter_by=filter_by, sort_by=DEFAULT_SORT_FIELDS)
    if args.JAR:
        display_cookie_jar(cookies)
    else:
        display_cookies(cookies, heading=f'{browser.name}: {browser.file_path}')


if __name__ == '__main__':
    main()
