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
Cookiescope MacOS decryptor.
"""

# See https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies

import base64
import json
import win32crypt
from Crypto.Cipher import AES
from pathlib import Path

from .base import DecryptorBase


class WindowsDecryptor(DecryptorBase):
    """Windows decryptor."""

    def __init__(self, browser_name: str, state_file: Path):
        """
        Base decryptor constructor.

        Args:
            browser_name: browser name
            state_file: state file path used for decryption
        """
        super().__init__(browser_name)
        self.state_file = state_file

    def decrypt(self, encrypted_value: bytes) -> str:
        """
        Windows method to decrypt a value.

        Args:
            encrypted_value: encrypted value

        Returns:
            decrypted value
        """
        with open(self.state_file, 'r') as file:
            encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
        encrypted_key = base64.b64decode(encrypted_key)                                       # Base64 decoding
        encrypted_key = encrypted_key[5:]                                                     # Remove DPAPI
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]  # Decrypt key
        # data = bytes.fromhex('763130...') # the encrypted cookie
        nonce = encrypted_value[3:3+12]
        ciphertext = encrypted_value[3+12:-16]
        tag = encrypted_value[-16:]
        cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
        # noinspection PyTypeChecker
        return cipher.decrypt_and_verify(ciphertext, tag)
