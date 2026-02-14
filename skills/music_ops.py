"""
Music Control Skill - Control macOS Music app and Spotify
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
                    "description": "Play music on Spotify or Apple Music",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search": {
                                "type": "string",
                                "description": "Song name, artist, or album to search and play"
                            },
                            "app": {
                                "type": "string",
                                "description": "Music app to use: 'spotify' or 'music' (default: spotify)",
                                "default": "spotify"
                            }
                        },
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
                        "properties": {
                            "app": {
                                "type": "string",
                                "description": "Music app: 'spotify' or 'music'",
                                "default": "spotify"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "next_track",
                    "description": "Skip to next track",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app": {
                                "type": "string",
                                "description": "Music app: 'spotify' or 'music'",
                                "default": "spotify"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "previous_track",
                    "description": "Go to previous track",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app": {
                                "type": "string",
                                "description": "Music app: 'spotify' or 'music'",
                                "default": "spotify"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "play_music": self.play_music,
            "pause_music": self.pause_music,
            "next_track": self.next_track,
            "previous_track": self.previous_track
        }

    def play_music(self, search: str = None, app: str = "spotify") -> dict:
        """Play music on Spotify or Apple Music"""
        try:
            app_name = "Spotify" if app.lower() == "spotify" else "Music"
            
            if search:
                # Search and play specific track
                if app.lower() == "spotify":
                    script = f'''
                    tell application "Spotify"
                        activate
                        delay 1
                        set search_results to search "{search}"
                        delay 2
                        play (item 1 of search_results)
                    end tell
                    '''
                else:  # Apple Music
                    script = f'''
                    tell application "Music"
                        activate
                        play (first track whose name contains "{search}")
                    end tell
                    '''
            else:
                # Just play/resume
                script = f'''
                tell application "{app_name}"
                    activate
                    play
                end tell
                '''
            
            subprocess.run(["osascript", "-e", script], check=True, timeout=10)
            
            if search:
                return {"status": "success", "message": f"▶️ Playing '{search}' on {app_name}"}
            else:
                return {"status": "success", "message": f"▶️ Playing music on {app_name}"}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": f"{app_name} took too long to respond"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}

    def pause_music(self, app: str = "spotify") -> dict:
        """Pause music"""
        try:
            app_name = "Spotify" if app.lower() == "spotify" else "Music"
            script = f'tell application "{app_name}" to pause'
            subprocess.run(["osascript", "-e", script], check=True)
            return {"status": "success", "message": f"⏸ Music paused on {app_name}"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}

    def next_track(self, app: str = "spotify") -> dict:
        """Skip to next track"""
        try:
            app_name = "Spotify" if app.lower() == "spotify" else "Music"
            script = f'tell application "{app_name}" to next track'
            subprocess.run(["osascript", "-e", script], check=True)
            return {"status": "success", "message": f"⏭ Next track on {app_name}"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}

    def previous_track(self, app: str = "spotify") -> dict:
        """Go to previous track"""
        try:
            app_name = "Spotify" if app.lower() == "spotify" else "Music"
            script = f'tell application "{app_name}" to previous track'
            subprocess.run(["osascript", "-e", script], check=True)
            return {"status": "success", "message": f"⏮ Previous track on {app_name}"}
        except Exception as e:
            return {"status": "error", "message": f"Music error: {str(e)}"}


def register():
    """Register the Music skill"""
    return MusicSkill()
