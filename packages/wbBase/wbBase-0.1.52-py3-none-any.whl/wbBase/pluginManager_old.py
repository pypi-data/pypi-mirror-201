from __future__ import annotations

import os
import sys
import traceback
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

import wx

if TYPE_CHECKING:
    from types import ModuleType
    from collections.abc import ItemsView, ValuesView, KeysView
    from .application import App


class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, ModuleType] = {}
        self.pluginDir = d = self.app.pluginDir
        disabledPlugins = self.app.cmdLineArguments.disabledPlugins or []
        if os.path.isdir(d):
            if d not in sys.path:
                sys.path.insert(1, d)
            import __main__ as main

            if "app" not in main.__dict__:
                main.__dict__["app"] = self.app
            plugins = [
                n
                for n in os.listdir(d)
                if os.path.isdir(os.path.join(d, n))
                and not n.startswith(".")
                and not n.startswith("__")
                and n not in disabledPlugins
            ]
            self.loadPlugins(plugins, main)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of "{self.app.AppName}">'

    def __contains__(self, name: str) -> bool:
        return name in self._plugins

    def __iter__(self) -> Iterator[str]:
        return iter(self._plugins)

    def __getitem__(self, name: str) -> ModuleType:
        return self._plugins[name]

    @property
    def app(self) -> App:
        """
        The running Workbench application.
        """
        return wx.GetApp()

    def get(self, key, default=None):
        return self._plugins.get(key, default)

    def keys(self) -> KeysView[str]:
        return self._plugins.keys()

    def items(self) -> ItemsView[str, ModuleType]:
        return self._plugins.items()

    def values(self) -> ValuesView[ModuleType]:
        return self._plugins.values()

    def loadPlugins(self, plugins: List[str], main: ModuleType) -> None:
        self.app.splashMessage("loading Plugins")
        if "output" in plugins:
            self.loadPlugin("output", main)
            plugins.remove("output")
        for name in plugins:
            self.loadPlugin(name, main)
        self.app.splashMessage("Plugins loaded")

    def loadPlugin(self, pluginName: str, main: ModuleType) -> None:
        try:
            self.app.splashMessage(f"loading plugin {pluginName}")
            plugin = __import__(pluginName)
            if hasattr(plugin, "globalObjects"):
                for name in plugin.globalObjects:
                    if name not in main.__dict__ and name not in self.app.globalObjects:
                        main.__dict__[name] = getattr(plugin, name)
                        self.app.globalObjects.append(name)
            self._plugins[pluginName] = plugin
        except ImportError as err:
            print(f"can not load plugin: {err}", pluginName)
            print(traceback.format_exc())
