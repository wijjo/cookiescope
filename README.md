# cookiescope

![Logo](./resources/cookiescope-256.png)

## Introduction

Cookiescope is a command line tool to query browser cookies.

See [TODO.md](./TODO.md) for hints about missing features and future enhancements.

## Prerequisites

### Command line environment with Git

For now, this is set up to run in a command line environment directly from a
local cloned Git repository.

## Setup and basic usage

Clone the Cookiescope GitHub repository.

```shell
git clone https://github.com/wijjo/cookiescope.git

cd cookiescope
```

### Getting help

Cookiescope supports the `-h/--help` options for command line help.

In MacOS or Linux:

```shell
bin/cookiscope -h
```

In Windows:

```powershell
bin\cookiescope.ps1 -h
```

Subsequent examples will omit the `bin` directory and the script extension, if
any, and just mention `cookiescope`. Note that you can either add the `bin`
directory to your path, or create a symbolic link to the appropriate Cookiescope
script in an existing directory that is already in your execution path.

## Usage examples

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

## Adopt Me!

The current project owner would be more than happy to hand off ownership of this
project. Ideally, it would to someone who is willing to invest time to add
decryption, increase browser/OS coverage, fix bugs, and providing user support
(if demanded).

## Contact:

steve at wijjo.com

## Credits

Binary cookies parsing code was originally based on this project:
https://github.com/ktnjared/BinaryCookieReader.git
