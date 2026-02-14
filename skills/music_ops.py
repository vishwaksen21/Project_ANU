"""
Music Player Skill - Play, pause, and control music (basic macOS integration)
"""
import os
import subprocess

def play_music(song_name: str = "") -> dict:
    """
    Play music on macOS Music app.
    
    Args:
        song_name: Optional song name to search for
    
    Returns:
        Status message
    """
    try:
        if song_name:
            # Try to play specific song
            script = f'''
            tell application "Music"
                activate
                play (first track whose name contains "{song_name}")
            end tell
            '''
        else:
            # Just play whatever is queued
            script = '''
            tell application "Music"
                activate
                play
            end tell
            '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            msg = f"♪ Now playing {song_name}" if song_name else "♪ Music started"
            return {"status": "success", "message": msg}
        else:
            return {"status": "error", "message": "Couldn't start music. Is Music app installed?"}
    except Exception as e:
        return {"status": "error", "message": f"Music error: {str(e)}"}

def pause_music() -> dict:
    """
    Pause music on macOS Music app.
    
    Returns:
        Status message
    """
    try:
        script = '''
        tell application "Music"
            pause
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"status": "success", "message": "⏸ Music paused"}
        else:
            return {"status": "error", "message": "Couldn't pause music"}
    except Exception as e:
        return {"status": "error", "message": f"Music error: {str(e)}"}

def next_track() -> dict:
    """
    Skip to next track.
    
    Returns:
        Status message
    """
    try:
        script = '''
        tell application "Music"
            next track
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], capture_output=True)
        return {"status": "success", "message": "⏭ Skipped to next track"}
    except Exception as e:
        return {"status": "error", "message": f"Music error: {str(e)}"}

def previous_track() -> dict:
    """
    Go to previous track.
    
    Returns:
        Status message
    """
    try:
        script = '''
        tell application "Music"
            previous track
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], capture_output=True)
        return {"status": "success", "message": "⏮ Went to previous track"}
    except Exception as e:
        return {"status": "error", "message": f"Music error: {str(e)}"}

def register():
    """Register music control skills"""
    from core.skill import Skill
    skill = Skill("music")
    skill.register(
        name="play_music",
        func=play_music,
        description="Play music on macOS Music app",
        parameters={
            "song_name": {"type": "string", "description": "Optional: name of song to play"}
        },
        required=[]
    )
    
    skill.register(
        name="pause_music",
        func=pause_music,
        description="Pause music playback",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="next_track",
        func=next_track,
        description="Skip to next music track",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="previous_track",
        func=previous_track,
        description="Go to previous music track",
        parameters={},
        required=[]
    )

    print("Loaded skill: music_skill")
    return skill
