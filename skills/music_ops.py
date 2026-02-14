"""
Music Control Skill - Control macOS Music app
"""
import subprocess
from typing import List, Dict, Any, Callable
from core.skill import Skill


class MusicSkill(Skill):
    
    @property
    def name(self) -> str:
        return "music_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "play_music",
                    "description": "Play music on macOS Music app",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "pause_music",
                    "description": "Pause music playback",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "play_music": self.play_music,
            "pause_music": self.pause_music
        }

    def play_music(self) -> dict:
        """Play music"""
        try:
            subprocess.run(["osascript", "-e", 'tell application "Music" to play'], check=True)
            return {"status": "success", "message": "▶️ Playing music"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}

    def pause_music(self) -> dict:
        """Pause music"""
        try:
            subprocess.run(["osascript", "-e", 'tell application "Music" to pause'], check=True)
            return {"status": "success", "message": "⏸ Music paused"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}


def register():
    """Register the Music skill"""
    return MusicSkill()
