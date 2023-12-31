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

Decryption is coded and tested as follows:
- MacOS with Chrome.
- Linux (Debian) with Chromium running in a Gnome desktop environment.
- Windows with Edge and Chrome.

Useful related links:

* https://github.com/n8henrie/pycookiecheat
* https://github.com/pyca/cryptography
* https://gist.github.com/DakuTree/428e5b737306937628f2944fbfdc4ffc#file-decryptchromecookies-py
* https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies

## User-specified sorting.

Current sorting is hard-coded. In the future allow users to specify sort order.

## Enhance filters.

Allow filter expression values to be regular expressions when the assignment
character is '~' rather than '='. E.g. `'value~myvalue-\d+'`.

Support date comparison with ">" and "<" applied to standard date strings.

Support other field comparisons, like booleans, if they are useful.

## Cookie deletion and clearing.

This capability requires the ability to update a database or rewrite the binary
cookies file format without corrupting it.

## Use SQL WHERE and ORDER BY clauses (for SQLite cookie DBs).

For now, cookie databases are queried for all cookies, and then filtered and
sorted in Python post-processing code. But it avoids excess memory consumption
by using iterators, rather than holding all cookies in memory.

## Build a graphical user interface.

Look for a simple cross-platform way to wrap the tool in a GUI. Perhaps Tk would
be good enough.
