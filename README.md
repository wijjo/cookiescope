# cookiescope

![Logo](./resources/cookiescope-256.png)

## Introduction

Cookiescope is a command line tool to query browser cookies.

See [TODO.md](./TODO.md) for hints about missing features and future enhancements.

## Setup (using a virtual environment)

See [DEVELOPMENT.md](./DEVELOPMENT.md) for an alternative to Pip-installing
Cookiescope. It offers the option to easily run from a source code environment.

On Linux and MacOS the following command sequence creates a virtual environment
and runs Cookiescope, to display help in this case.

```shell
python3 -m venv venv

source venv/bin/activate

pip3 install cookiescope

hash -r

cookiescope -h
```

This is the equivalent command sequence for Windows.

```powershell
py -m venv venv

venv\Scripts\Activate.ps1

pip install cookiescope

cookiescope -h
```

See the Usage section for other useful Cookiescope commands.

## Usage examples

The examples below assume Cookiescope is available through the system path. If 
not, see the section above for how to run it from a local source repository.

### Get help

Cookiescope supports the `-h/--help` options for command line help.

```shell
cookiescope -h
```

### Display all browser cookies

Choose the command example below based on the desired target browser.

```shell
cookiescope chrome

cookiescope edge

cookiescope firefox

cookiescope safari
```

### Display browser cookies for a domain containing specific value data

Note that searches are always partial. In the example below, any cookies with a
domain containing "paypal" and a value containing "me@example.com" will be
displayed.

```shell
cookiescope chrome domain=paypal value=me@example.com 
```

### Display browser cookies in Netscape cookie jar format, e.g. for use with `curl`

The `-j` or `--jar` option selects the cookie jar output format, which can be
useful for testing with `curl`.

```shell
cookiescope chrome -j
```

## Building Cookiescope packages

In a Cookiescope source environment the following command builds packages in the
`dist` subdirectory, e.g. for uploading to PyPI.

```shell
tools/build.sh
```
## Notes

This has been primarily used with MacOS Safari. But it also has been (briefly)
tested with other browsers on MacOS, Windows, and Linux.

Here is what is currently supported:

* Safari on MacOS
* Google Chrome on MacOS and Windows
* Microsoft Edge on Windows
* Chromium on Linux
* Firefox on MacOS, Windows, and Linux

For any developer that wishes to extend it, the framework is designed for easy
expansion and adaptation.

## Contact:

steve at wijjo.com

## Credits

### BinaryCookieReader

The Safari binary cookies parsing code was originally based on the
BinaryCookieReader project:

https://github.com/ktnjared/BinaryCookieReader.git

### Pycookiecheat

The Linux/MacOS decryption code was based on the pycookiecheat project:

https://github.com/n8henrie/pycookiecheat

The code was reorganized to better fit into the structure of Cookiescope.

#### Pycookiecheat MIT License

The pycookiecheat MIT License is copied below:

The MIT License (MIT)

Copyright (c) 2015 Nathan Henrie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
