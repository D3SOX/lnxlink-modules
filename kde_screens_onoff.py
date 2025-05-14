"""Turns on or off the screens (KDE)"""
import re
import logging
from shutil import which
from lnxlink.modules.scripts.helpers import syscommand

logger = logging.getLogger("lnxlink")


class Addon:
    """Addon module"""

    def __init__(self, lnxlink):
        """Setup addon"""
        self.name = "Screens OnOff KDE"
        self.lnxlink = lnxlink
        if which("kscreen-doctor") is None:
            raise SystemError("System command 'kscreen-doctor' not found")

    def exposed_controls(self):
        """Exposes to home assistant"""
        return {
            "Screens OnOff KDE": {
                "type": "switch",
                "icon": "mdi:monitor",
            }
        }

    def get_info(self):
        """Gather information from the system"""
        command = "kscreen-doctor --dpms show"
        stdout, _, _ = syscommand(command)
        
        # Check if all screens are on or off
        matches = re.findall(r"dpms mode for screen .+: (\w+)", stdout)
        
        if not matches:
            logger.debug("Screen_onoff error parsing output: %s\n%s", command, stdout)
            return "UNKNOWN"
        
        # If any screen is off, consider the overall status as OFF
        if "off" in matches:
            return "OFF"
        
        return "ON"

    def start_control(self, topic, data):
        """Control system"""
        if data.lower() == "off":
            syscommand("kscreen-doctor --dpms off")
        elif data.lower() == "on":
            syscommand("kscreen-doctor --dpms on")
