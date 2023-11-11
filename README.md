# cookiescope

![Logo](./resources/cookiescope-256.png)

Cookiescope is a command line tool to query browser cookies.

Run `cookiescope -h` or (`--help`) for more information.

Big caveat: Chrome encrypted cookie values are not queryable or displayable as
clear text. As mentioned in [TODO.md](./TODO.md), this pulls in dependencies and
complexity that is beyond the current scope. Unfortunately this means that
support for the most popular browser is incomplete.

See TODO.md for hints about missing features and future enhancements.

## Notes

This has been primarily used with MacOS Safari. But it also has been (briefly)
tested with other browsers on MacOS, Windows, and Linux.

Here is what is currently supported:

* Safari on MacOS
* Google Chrome on MacOS and Windows (without value decryption)
* Microsoft Edge on Windows (without value decryption)
* Chromium on Linux (without value decryption)
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
