# Cookiescope development

## Introduction

This file briefly documents how to work with Cookiescope source code.

Note that Cookiescope is designed to run directly from source, with the help of
a Python virtual environment. So it can serve as an alternative to Pip
installation, even if not interested in working with the source as a developer.

## Source code environment setup

### Prerequisites

Git must be installed.

### Clone the Cookiescope GitHub repository.

```shell
git clone https://github.com/wijjo/cookiescope.git
```

### Running from a local source repository

The `bin` directory has two scripts, `bin/cookiescope` for Linux and MacOS, and
`bin\cookiescope.ps1` for Windows. Use the appropriate script to run Cookiescope
directly from the source repository.

The first run creates a virtual environment in the `venv` subdirectory.

E.g. in Linux or MacOS:

```shell
cd cookiescope

bin/cookiescope
```

E.g. in Windows.

```powershell
cd cookiescope

bin\cookiescope.ps1
```

## Building Cookiescope packages

The following command builds packages in the `dist` subdirectory, e.g. for
uploading to PyPi.

```shell
tools/build.sh
```

## Development notes

See [README.md](./README.md) for general information about what is working and
tested.

All major platforms are supported.

The most popular browsers are supported. Adding a new browser, particularly a
Chrome-based browser, should be easy and involve minimal code.

## Adopt Me!

The current project owner would be more than happy to hand off ownership of this
project. Ideally, it would to someone who is willing to invest time to add
decryption, increase browser/OS coverage, fix bugs, and providing user support
(if demanded).

## Contact:

steve at wijjo.com
