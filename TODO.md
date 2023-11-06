# To-Do

## Fully-support more platforms and browsers.

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

## Support user-specified sorting.

Current sorting is fixed. Allow the user to specify sort order.

## Support regular expression filters.

Allow filter expression values to be regular expressions when the assignment
character is '~' rather than '='. E.g. `'value~myvalue-\d+'`.

## Take advantage of SQL WHERE and ORDER BY clauses (for SQLite cookie DBs).

For now SQLite cookie databases are queried for all cookies, and the filtering
and sorting is performed by Python code post-processing. It would improve
resource efficiency, including processor and memory, to convert external
filtering and sorting to SQL WHERE and ORDER BY clauses in order to handle
everything in the database.

## Split up monolithic script  code.

Create more easily-navigated library of classes and functions.

## Build a graphical user interface.

Look for a simple cross-platform way to wrap the tool in a GUI. Perhaps Tk would
be good enough.

## Support cookie deletion and clearing.

This capability requires the ability to update a database or rewrite the binary
cookies file format without corrupting it.
