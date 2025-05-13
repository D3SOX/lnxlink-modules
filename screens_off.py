"""Turns screens off (Plasma Wayland)"""
import logging
from shutil import which
from lnxlink.modules.scripts.helpers import import_install_package, syscommand

logger = logging.getLogger("lnxlink")


class Addon:
    """Addon module"""

    def __init__(self, lnxlink):
        """Setup addon"""
        self.name = "Screens off"
        self.lnxlink = lnxlink

    def start_control(self, topic, data):
        """Control system"""
        self.lnxlink.temp_connection_callback(True)
        returncode = None
        if which("dbus-send") is not None and returncode != 0:
            _, _, returncode = syscommand("/bin/dbus-send --session --print-reply --dest=org.kde.kglobalaccel /component/org_kde_powerdevil org.kde.kglobalaccel.Component.invokeShortcut string:'Turn Off Screen'")
        if returncode != 0:
            self.lnxlink.temp_connection_callback(False)

    def exposed_controls(self):
        """Exposes to home assistant"""
        return {
            "Turn screens off": {
                "type": "button",
                "icon": "mdi:monitor-off",
            }
        }
