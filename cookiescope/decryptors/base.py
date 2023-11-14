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
Cookiescope base decryptor.
"""

from abc import ABC, abstractmethod


class DecryptorBase(ABC):
    """Abstract decryptor class."""

    def __init__(self, browser_name: str):
        """
        Base decryptor constructor.

        Args:
            browser_name: browser name
        """
        self.browser_name = browser_name

    @abstractmethod
    def decrypt(self, encrypted_value: bytes) -> str:
        """
        Decrypt a value.

        Args:
            encrypted_value: encrypted value

        Returns:
            decrypted value
        """
        ...
