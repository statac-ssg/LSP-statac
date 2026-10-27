# LSP-statac

[Statac](https://statac.dev)'s language server in Sublime Text, through
the [LSP](https://packagecontrol.io/packages/LSP) package. In a Statac
site, Sublime Text shows each problem `statac check` finds as you type,
and offers completion, hover, go to definition, find references and
fixes. When you rename a page's file, the links to it are updated.

It needs Statac 0.7.0 or later. With an earlier Statac, Sublime Text says
only that the server stopped.

## Installing

1. Install [Statac](https://statac.dev/install/).
2. In Sublime Text, run Package Control: Install Package, and install
   `LSP`, then `LSP-statac`.
3. Open a folder that holds a Statac site: a `statac.yaml` file, or a
   `content` folder.

The server starts for a file inside a site and leaves every other file
alone.

## Keys

Sublime Text gives hover, fixes and go to definition no key of its own.
To add them, run Preferences: Key Bindings and add these lines to your
own key bindings, choosing other keys if these are taken:

```json
[
    {
        "keys": ["primary+k", "primary+i"],
        "command": "lsp_hover",
        "context": [{"key": "lsp.session_with_capability", "operand": "hoverProvider"}]
    },
    {
        "keys": ["primary+."],
        "command": "lsp_code_actions",
        "context": [{"key": "lsp.session_with_capability", "operand": "codeActionProvider"}]
    },
    {
        "keys": ["f12"],
        "command": "lsp_symbol_definition",
        "args": {"side_by_side": false, "force_group": true, "fallback": true, "group": -1},
        "context": [
            {"key": "lsp.session_with_capability", "operand": "definitionProvider"},
            {"key": "auto_complete_visible", "operand": false}
        ]
    }
]
```

Find references is on <kbd>Shift</kbd>+<kbd>F12</kbd> already. To rename
a page's file and update the links to it, run LSP: Rename Path, or choose
LSP: Rename… on the file in the sidebar.

## Settings

Sublime Text looks for `statac` on the path, then where Homebrew, the
install script, Cargo, Scoop and winget put it. To use another, run
Preferences: LSP-statac Settings and give its whole path:

```json
{
    "command": ["/path/to/statac", "lsp"]
}
```

## More

- [Editors](https://statac.dev/editors/), in Statac's documentation.
- [Issues](https://git.statac.dev/statac/LSP-statac/issues).

## Licence

MIT or Apache-2.0, at your choice: [LICENSE-MIT](LICENSE-MIT),
[LICENSE-APACHE](LICENSE-APACHE).
