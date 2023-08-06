from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List

import yaml


@dataclass
class PluginInfo:
    Name: str
    Installation: str = "optional"


@dataclass
class ApplicationInfo:
    AppName: str = "Application"
    AppDisplayName: str = ""
    VendorName: str = "WorkBench"
    VendorDisplayName: str = ""
    Description: str = "WorkBench GUI Application"
    Copyright: str = ""
    URL: str = "https://gitlab.com/workbench2/wbbase"
    Plugins: List[PluginInfo] = field(default_factory=list)

    def __post_init__(self):
        if not self.AppDisplayName:
            self.AppDisplayName = self.AppName
        if not self.VendorDisplayName:
            self.VendorDisplayName = self.VendorName
        if not self.Copyright:
            self.Copyright = f"(c) {datetime.now().year} by {self.VendorDisplayName}"

    @classmethod
    def fromString(cls, text: str) -> ApplicationInfo:
        data: Dict[str, Any] = yaml.safe_load(text)
        appinfo = cls()
        for attr in (
            "AppName",
            "AppDisplayName",
            "VendorName",
            "VendorDisplayName",
            "Description",
            "Copyright",
            "URL",
        ):
            setattr(appinfo, attr, data.get(attr, getattr(appinfo, attr)))
        plugins = data.get("Plugins", [])
        if plugins:
            appinfo.Plugins.clear()
        for plugin in plugins:
            appinfo.Plugins.append(
                PluginInfo(plugin["Name"], plugin.get("Installation", "optional"))
            )
        return appinfo


sampleInfo = """
AppName: SampleWorkbench
AppDisplayName: Sample-Workbench
VendorName: SampleVendor
VendorDisplayName: Sample Vendor Inc.
Copyright: (c) 2013-2023 by Andreas Eigendorf
Description: Sample Workbench GUI Application
Plugins:
- Name: output
  Installation: required
- Name: shell
  Installation: default
- Name: loglist
"""
if __name__ == "__main__":
    appinfo = ApplicationInfo.fromString(sampleInfo)
    print(asdict(appinfo))
    p1 = PluginInfo("test")
    p2 = PluginInfo("test")
    print(p1 == p2)
