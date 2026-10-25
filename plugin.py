from __future__ import annotations

import os
import shutil

from LSP.plugin import IsApplicableContext
from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PluginStartError

# What makes a folder a Statac site, as Statac reads it: its settings, or
# a folder of its pages.
SETTINGS = "statac.yaml"
CONTENT = "content"

# Where each way of installing Statac puts it, for an editor started
# without the shell's path: Homebrew, the install script, Cargo, Scoop and
# winget.
INSTALLED = [
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/home/linuxbrew/.linuxbrew/bin",
    "~/.local/bin",
    "~/.cargo/bin",
    "~/scoop/shims",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Links"),
]

NOT_FOUND = (
    "Statac isn't installed, or Sublime Text can't find it. Install it as "
    "statac.dev/install says, or give its path as `command` in LSP-statac's settings."
)


def in_a_site(path: str | None) -> bool:
    """Whether the file at `path` is in a Statac site: a folder above it
    holds `statac.yaml` or a `content` folder."""
    if not path:
        return False
    folder = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.isfile(os.path.join(folder, SETTINGS)):
            return True
        if os.path.isdir(os.path.join(folder, CONTENT)):
            return True
        above = os.path.dirname(folder)
        if above == folder:
            return False
        folder = above


def found(program: str) -> str | None:
    """Where `program` is: on the path, or where an installer puts it."""
    on_path = shutil.which(program)
    if on_path:
        return on_path
    for folder in INSTALLED:
        folder = os.path.expanduser(folder)
        # Without LOCALAPPDATA the winget folder is relative, and would be
        # read from wherever Sublime Text was started.
        if not os.path.isabs(folder):
            continue
        at = shutil.which(program, path=folder)
        if at:
            return at
    return None


class Statac(LspPlugin):
    @classmethod
    def is_applicable_async(cls, context: IsApplicableContext) -> bool:
        return super().is_applicable_async(context) and in_a_site(context.view.file_name())

    @classmethod
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        command = context.configuration.command
        if not command:
            raise PluginStartError(NOT_FOUND)
        program = os.path.expanduser(command[0])
        at = program if os.path.isabs(program) and os.path.isfile(program) else found(program)
        if not at:
            raise PluginStartError(NOT_FOUND)
        context.configuration.command = [at] + command[1:]


def plugin_loaded() -> None:
    Statac.register()


def plugin_unloaded() -> None:
    Statac.unregister()
