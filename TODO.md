# To-Do

## Support more browser/platform combinations.

The only platform-specific code is the data used for automatically locating
cookies files for browsers.

Expand support to include well-known cookie file locations for all significant
browsers on all desktop operating systems.

These platforms should be fully-supported:

- Linux
- MacOS
- Windows

Fully-supported browsers should include:

- Chrome
- Firefox
- Microsoft Edge
- Safari

Also consider supporting other significant browsers, for example:

- Arc
- Brave
- Gnome Web
- Konqueror
- Opera
- Vivaldi

In theory, additional browser support should be mostly a matter of determining
possible file locations and SQL column mappings, if using SQLite.

## Encrypted cookie value decryption.

This is a significant amount of work. It involves switching from a stand-alone
monolithic script to a full-fledged Python project with external dependencies,
like the cryptography library.

Once external dependencies exist, installation and support becomes much more
complicated. Given the author's personal limited need for just MacOS/Safari,
encryption will remain outside the scope of this simple project for now.

On the other hand, the existing code should provide a good structure and
starting point for someone wishing to tackle encryption.

See the following links for more information about possible solutions.

* https://github.com/n8henrie/pycookiecheat
* https://github.com/pyca/cryptography
* https://gist.github.com/DakuTree/428e5b737306937628f2944fbfdc4ffc#file-decryptchromecookies-py
* https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies

## User-specified sorting.

Current sorting is fixed. Allow the user to specify sort order.

## Regular expression filters.

Allow filter expression values to be regular expressions when the assignment
character is '~' rather than '='. E.g. `'value~myvalue-\d+'`.

## Use SQL WHERE and ORDER BY clauses (for SQLite cookie DBs).

For now, cookie databases are queried for all cookies, and then filtered and
sorted in Python post-processing code. But it avoids excess memory consumption
by using iterators, rather than holding all cookies in memory.

## Split up monolithic script code.

Create more easily-navigated library of classes and functions. The issue becomes
how to keep it easy to install. It would need a mechanism for locating its 
library package and modules. It might require a more traditional setup process, 
and rely on packagers, like Pip, Homebrew, Chocolatey, Apt, Snap, etc., to
simplify installation and usage. It adds complexity for users.

## Build a graphical user interface.

Look for a simple cross-platform way to wrap the tool in a GUI. Perhaps Tk would
be good enough.

## Cookie deletion and clearing.

This capability requires the ability to update a database or rewrite the binary
cookies file format without corrupting it.
