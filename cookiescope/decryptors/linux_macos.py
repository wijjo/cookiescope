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

# Decryption is based on code from the following project. But the code has been
# heavily-modified and reorganized.
#
# https://github.com/n8henrie/pycookiecheat
#
# That project's code is covered by the following license:
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Nathan Henrie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Cookiescope common Linux/MacOS decryption support.
"""

from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .base import DecryptorBase


class LinuxMacOSDecryptorBase(DecryptorBase, ABC):
    """Linux/MacOS decryptor base class."""

    #: Decryption iteration count (subclass must provide).
    iterations: int = None

    def __init__(self, browser_name: str):
        """
        Linux/MacOS decryptor base class constructor.

        Args:
            browser_name: browser name
        """
        assert self.iterations
        super().__init__(browser_name)
        kdf = PBKDF2HMAC(algorithm=SHA1(), iterations=self.iterations, length=16, salt=b'saltysalt')
        password = self.get_password()
        encryption_key = kdf.derive(password.encode('utf8'))
        algorithm = AES(encryption_key)
        self.cipher = Cipher(algorithm=algorithm, mode=CBC(b' ' * 16))

    @abstractmethod
    def get_password(self) -> str:
        """
        Required method to get the storage password.

        Returns:
            password
        """
        ...

    def decrypt(self, encrypted_value: bytes) -> str:
        """
        Common Linux/MacOS method to decrypt a value.

        Args:
            encrypted_value: encrypted value

        Returns:
            decrypted value
        """
        # Encrypted cookies should be prefixed with 'v10' or 'v11' according to the
        # Chromium code. Strip it off.
        encrypted_value = encrypted_value[3:]
        decryptor = self.cipher.decryptor()
        decrypted = decryptor.update(encrypted_value) + decryptor.finalize()
        # Strip padding and decode.
        last = decrypted[-1]
        if isinstance(last, int):
            return decrypted[:-last].decode('utf8')
        # noinspection PyTypeChecker
        return decrypted[: -ord(last)].decode('utf8')
