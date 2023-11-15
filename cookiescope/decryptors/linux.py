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

import keyring

"""
Cookiescope Linux decryptor.
"""

from cookiescope.utility import abort
from .linux_macos import LinuxMacOSDecryptorBase


class LinuxDecryptor(LinuxMacOSDecryptorBase):
    """Linux decryptor."""

    #: Decryption iteration count.
    iterations = 1

    def get_password(self) -> str:
        """Get storage password - see base class method docstring."""
        password = gnome_get_password(self.browser_name)
        # Try to get password from keyring, which should support KDE / KWallet
        # if dbus-python is installed.
        if password is None:
            password = kde_get_password(self.browser_name)
        if password is None:
            abort('Unable to get storage password.')
        return password


def gnome_get_password(browser_name: str) -> str | None:
    """
    Gnome get storage password.

    Try to get pass from Gnome / libsecret if it seems available
    https://github.com/n8henrie/pycookiecheat/issues/12

    Args:
        browser_name: browser name

    Returns:
        password or None if not available
    """
    keyring_label = f'{browser_name} Safe Storage'
    keyring_item_name = browser_name
    keyring_app_name = browser_name.lower()
    try:
        import gi
        gi.require_version("Secret", "1")
        from gi.repository import Secret
    except ImportError:
        return None
    keyring_attr_name = keyring_item_name
    flags = Secret.ServiceFlags.LOAD_COLLECTIONS
    service = Secret.Service.get_sync(flags)
    gnome_keyring = service.get_collections()
    unlocked_keyrings = service.unlock_sync(gnome_keyring).unlocked
    for unlocked_keyring in unlocked_keyrings:
        for item in unlocked_keyring.get_items():
            if item.get_label() == keyring_label:
                item_app = item.get_attributes().get('application', keyring_attr_name)
                if item_app.lower() == keyring_app_name:
                    item.load_secret_sync()
                    return item.get_secret().get_text()


def kde_get_password(browser_name: str) -> str | None:
    """
    KDE/KWallet get storage password.

    Args:
        browser_name: browser name

    Returns:
        password or None if not available
    """
    keyring_label = f'{browser_name} Safe Storage'
    keyring_item_name = browser_name
    # Should support KDE / KWallet if dbus-python is installed.
    try:
        service_name = f'{keyring_item_name} Keys'
        return keyring.get_password(service_name, keyring_label)
    except RuntimeError:
        return None
