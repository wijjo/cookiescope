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
Binary cookies handling.
"""

from io import BytesIO
from pathlib import Path
from struct import unpack
from urllib.parse import unquote

from cookiescope.cookies import CookieData
from cookiescope.utility import abort, open_binary_file
from typing import AnyStr, IO, Iterator, Self


class BinaryCookiesExtractor:
    """Binary cookies file reader and data extractor/decoder."""

    def __init__(self, stream: IO):
        """
        Binary cookies extractor constructor.

        Args:
            stream: file stream to read cookies from
        """
        self._stream = stream

    def get_bytes(self, length: int, expect: bytes = None) -> AnyStr:
        """
        Extract bytes from stream.

        Args:
            length: number of bytes
            expect: optional expected value to check

        Returns:
            extracted bytes
        """
        value = self._stream.read(length)
        if expect is not None and value != expect:
            abort(f'Expected bytes "{expect}", found "{value}".')
        return value

    def get_string(self, length: int, encoding: str = 'utf-8', expect: str = None) -> str:
        """
        Extract string from stream.

        Args:
            length: number of characters
            encoding: optional encoding (default: utf-8)
            expect: optional expected value to check

        Returns:
            extracted string value
        """
        raw_value = self.get_bytes(length)
        value = raw_value.decode(encoding)
        if expect is not None and value != expect:
            abort(f'Expected string "{expect}", found "{value}".')
        return value

    def get_header_integer(self) -> int:
        """
        Extract integer from stream header (big-endian integer format).

        Returns:
            extracted integer value
        """
        return unpack('>i', self.get_bytes(4))[0]

    def get_integer(self) -> int:
        """
        Extract integer from stream body (little-endian integer format).

        Returns:
            extracted integer value
        """
        return unpack('<i', self.get_bytes(4))[0]

    def get_flags(self) -> tuple[bool, bool]:
        """
        Extract flag string from stream by checking flag integer bits.

        Returns:
            extracted (secure, http_only) boolean flags
        """
        flags = self.get_integer()
        return bool(flags & 0x00000001), bool(flags & 0x00000004)

    def get_attribute(self) -> str:
        """
        Extract attribute value from stream.

        Returns:
            extracted attribute value
        """
        value = ''
        byte = self.get_bytes(1)
        while unpack('<b', byte)[0] != 0:
            value += byte.decode('utf-8')
            byte = self.get_bytes(1)
        return value

    def get_date_time(self) -> int:
        """
        Extract date/time string value from stream.

        Returns:
            extracted seconds since 1970 (Unix epoch) as integer
        """
        # Expiry date is in Mac epoch format: Starts from 1/Jan/2001 (978307200 in seconds)
        return int(unpack('<d', self.get_bytes(8))[0] + 978307200)

    def get_block(self, length) -> Self:
        """
        Get sub-extractor for stream block.

        Args:
            length: block length

        Returns:
            block sub-extractor
        """
        return self.__class__(BytesIO(self.get_bytes(length)))

    def set_offset(self, offset: int):
        """
        Set stream offset (position).

        Args:
            offset: byte offset
        """
        self._stream.seek(offset)


def is_binary_cookies_file(path: Path) -> bool:
    """
    Check if file appears to be a binary cookies file.

    Args:
        path: file path

    Returns:
        True if the file contains binary cookies
    """
    with open_binary_file(path) as binary_file:
        extractor = BinaryCookiesExtractor(binary_file)
        if extractor.get_string(4, encoding='ascii') != 'cook':
            return False
        return True


def generate_binary_cookies(path: Path) -> Iterator[CookieData]:
    """
    Generate cookies by reading file and extracting individual cookies.

    Args:
        path: file path

    Returns:
        cookie iterator
    """
    with open_binary_file(path) as binary_file:
        extractor = BinaryCookiesExtractor(binary_file)
        extractor.get_string(4, encoding='ascii', expect='cook')
        num_pages = extractor.get_header_integer()
        page_sizes = [extractor.get_header_integer() for _idx in range(num_pages)]
        page_blocks = [extractor.get_block(length) for length in page_sizes]
        for page_block in page_blocks:
            page_block.get_bytes(4, expect=bytes([0, 0, 1, 0]))
            num_cookies = page_block.get_integer()
            cookie_offsets = [page_block.get_integer() for _idx in range(num_cookies)]
            page_block.get_bytes(4, expect=bytes([0, 0, 0, 0]))
            for offset in cookie_offsets:
                page_block.set_offset(offset)
                cookie_size = page_block.get_integer()
                cookie_block = page_block.get_block(cookie_size)
                cookie_block.get_bytes(4)  # unknown
                secure, http_only = cookie_block.get_flags()
                cookie_block.get_bytes(4)  # unknown
                url_offset = cookie_block.get_integer()
                name_offset = cookie_block.get_integer()
                path_offset = cookie_block.get_integer()
                value_offset = cookie_block.get_integer()
                cookie_block.get_bytes(8)  # end of cookie
                expires = cookie_block.get_date_time()
                created = cookie_block.get_date_time()
                cookie_block.set_offset(url_offset - 4)
                domain = cookie_block.get_attribute()
                cookie_block.set_offset(name_offset - 4)
                name = cookie_block.get_attribute()
                cookie_block.set_offset(path_offset - 4)
                path = cookie_block.get_attribute()
                cookie_block.set_offset(value_offset - 4)
                value = unquote(cookie_block.get_attribute())
                yield CookieData(
                    domain=domain,
                    name=name,
                    path=path,
                    value=value,
                    http_only=http_only,
                    secure=secure,
                    expires=expires,
                    created=created,
                )
