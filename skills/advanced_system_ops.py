"""
Advanced System Control - Full macOS access (Personal AI Agent Mode)
"""

import os
import subprocess
import json
import platform
from typing import List, Dict, Any, Callable
from core.skill import Skill


class AdvancedSystemOpsSkill(Skill):

    @property
    def name(self) -> str:
        return "advanced_system_ops"

    # ---------------- TOOL DEFINITIONS ---------------- #

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Open an application on macOS",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string"}
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "close_application",
                    "description": "Close an application on macOS",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string"}
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_running_apps",
                    "description": "List running applications",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_terminal_command",
                    "description": "Execute a terminal command",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "lock_screen",
                    "description": "Lock the macOS screen",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "empty_trash",
                    "description": "Empty macOS trash",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Get system information",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "open_application": self.open_application,
            "close_application": self.close_application,
            "get_running_apps": self.get_running_apps,
            "execute_terminal_command": self.execute_terminal_command,
            "lock_screen": self.lock_screen,
            "empty_trash": self.empty_trash,
            "get_system_info": self.get_system_info
        }

    # ---------------- INTERNAL HELPERS ---------------- #

    def ensure_macos(self):
        return platform.system() == "Darwin"

    # ---------------- APPLICATION CONTROL ---------------- #

    def open_application(self, app_name: str) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            subprocess.run(["open", "-a", app_name], check=True)
            return {"status": "success", "message": f"✓ Opened {app_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def close_application(self, app_name: str) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            script = f'tell application "{app_name}" to quit'
            subprocess.run(["osascript", "-e", script], check=True)
            return {"status": "success", "message": f"✓ Closed {app_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- SYSTEM INFO ---------------- #

    def get_running_apps(self) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            script = '''
            tell application "System Events"
                get name of every process whose background only is false
            end tell
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                check=True
            )

            apps = result.stdout.strip().split(", ")
            return {
                "status": "success",
                "message": "Running Applications:\n• " + "\n• ".join(apps[:20])
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- TERMINAL ---------------- #

    def execute_terminal_command(self, command: str) -> dict:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=20
            )

            output = (result.stdout + result.stderr)[:1000]

            return {
                "status": "success" if result.returncode == 0 else "error",
                "message": output
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- SYSTEM ACTIONS ---------------- #

    def lock_screen(self) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            subprocess.run(["pmset", "displaysleepnow"], check=True)
            return {"status": "success", "message": "✓ Screen locked"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def empty_trash(self) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            script = '''
            tell application "Finder"
                empty trash
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return {"status": "success", "message": "✓ Trash emptied"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_system_info(self) -> dict:
        if not self.ensure_macos():
            return {"status": "error", "message": "Supported only on macOS"}

        try:
            info = []

            version = subprocess.run(
                ["sw_vers", "-productVersion"],
                capture_output=True,
                text=True
            ).stdout.strip()
            info.append(f"macOS: {version}")

            cpu = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True
            ).stdout.strip()
            info.append(f"CPU: {cpu}")

            mem = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True
            ).stdout.strip()
            mem_gb = int(mem) / (1024**3)
            info.append(f"Memory: {mem_gb:.1f} GB")

            uptime = subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True
            ).stdout.strip()
            info.append(f"Uptime: {uptime}")

            return {
                "status": "success",
                "message": "System Information:\n• " + "\n• ".join(info)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


def register():
    """Register the Advanced System Operations skill"""
    return AdvancedSystemOpsSkill()
