"""
pluginManager
========================================================

Test new PluginManager class.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

from typing import TYPE_CHECKING

import wx

if TYPE_CHECKING:
    from wbBase.application import App


class PluginManager(dict):
    def __init__(self):
        super().__init__()
        self.loadPlugins()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of "{self.app.AppName}">'

    @property
    def app(self) -> App:
        """
        The running Workbench application.
        """
        return wx.GetApp()

    def loadPlugins(self):
        app = self.app
        app.splashMessage("loading plugins")
        available_plugins = {}
        entryPoints = entry_points(group="wbbase.plugin")
        if entryPoints:
            available_plugins = {e.name: e for e in entryPoints}
        appInfo_plugins = app.info.Plugins
        disabled_plugins = app.cmdLineArguments.disabledPlugins or []
        for plugin in appInfo_plugins:
            if plugin.Installation == "exclude":
                continue
            name = plugin.Name
            if name in disabled_plugins:
                continue
            app.splashMessage(f"loading plugin {name}")
            if name in available_plugins:
                self[name] = available_plugins[name].load()
            elif plugin.Installation == "required":
                wx.LogError(
                    "Missing required plugin\n\n"
                    f"Can't load plugin '{name}'\n"
                    "Application will terminate."
                )
                sys.exit(1)
