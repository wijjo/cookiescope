# cookiescope

![Logo](./resources/cookiescope-256.png)

Cookiescope is a command line tool to query browser cookies.

Run `cookiescope -h` or (`--help`) for more information.

Note that Chrome cookie values are not displayable as clear text due to
encryption. People have attempted various solutions, but it has proven to be a
moving target.

See TODO.md for hints about missing features and future enhancements.

## Contact:

steve at wijjo.com

## Notes

This has only been primarily used with MacOS Safari. But it also has been
tested with other browsers on MacOS, Windows, and Linux.

Here is what is currently supported:

* Safari on MacOS
* Google Chrome on MacOS and Windows (1)
* Microsoft Edge on Windows (1)
* Chromium on Linux (1)
* Firefox on MacOS, Windows, and Linux

(1) Encrypted values are hidden.

For any developer that wishes to extend it, the framework is designed for easy
expansion and adaptation.

**The current project owner would be more than happy to hand off ownership of
this project.** Ideally, it would to someone who is willing to invest time in
increasing browser/OS coverage, fixing bugs, and providing support.

## Credits

Binary cookies parsing code was originally based on this project:
https://github.com/ktnjared/BinaryCookieReader.git
