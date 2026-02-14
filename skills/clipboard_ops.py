"""
Clipboard and Text Management Operations
"""
import subprocess
import os

def copy_to_clipboard(text: str) -> dict:
    """
    Copy text to clipboard.
    
    Args:
        text: Text to copy to clipboard
    
    Returns:
        Status message
    """
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return {"status": "success", "message": f"✓ Copied to clipboard: {text[:50]}..."}
    except Exception as e:
        return {"status": "error", "message": f"Clipboard error: {str(e)}"}

def get_clipboard() -> dict:
    """
    Get text from clipboard.
    
    Returns:
        Clipboard content
    """
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        content = result.stdout
        if content:
            preview = content[:100] + "..." if len(content) > 100 else content
            return {"status": "success", "message": f"Clipboard content: {preview}"}
        else:
            return {"status": "success", "message": "Clipboard is empty"}
    except Exception as e:
        return {"status": "error", "message": f"Clipboard error: {str(e)}"}

def send_notification(title: str, message: str, sound: bool = True) -> dict:
    """
    Send a system notification.
    
    Args:
        title: Notification title
        message: Notification message
        sound: Play sound with notification
    
    Returns:
        Status message
    """
    try:
        sound_cmd = 'sound name "default"' if sound else ""
        script = f'''
        display notification "{message}" with title "{title}" {sound_cmd}
        '''
        subprocess.run(['osascript', '-e', script], timeout=5)
        return {"status": "success", "message": f"✓ Notification sent: {title}"}
    except Exception as e:
        return {"status": "error", "message": f"Notification error: {str(e)}"}

def text_to_speech(text: str, voice: str = "Samantha", rate: int = 165) -> dict:
    """
    Convert text to speech with custom settings.
    
    Args:
        text: Text to speak
        voice: Voice name (default: Samantha)
        rate: Speech rate (default: 165)
    
    Returns:
        Status message
    """
    try:
        clean_text = text.replace('"', '\\"')
        os.system(f'say -v {voice} -r {rate} "{clean_text}" &')
        return {"status": "success", "message": f"✓ Speaking: {text[:50]}..."}
    except Exception as e:
        return {"status": "error", "message": f"TTS error: {str(e)}"}

def create_quick_note(note_text: str) -> dict:
    """
    Create a quick note in a notes file.
    
    Args:
        note_text: Note content
    
    Returns:
        Status message
    """
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notes_file = "anu_quick_notes.txt"
        with open(notes_file, 'a') as f:
            f.write(f"\n[{timestamp}]\n{note_text}\n")
        
        return {"status": "success", "message": f"✓ Note saved: {note_text[:50]}..."}
    except Exception as e:
        return {"status": "error", "message": f"Note error: {str(e)}"}

def read_notes() -> dict:
    """
    Read all quick notes.
    
    Returns:
        Notes content
    """
    try:
        notes_file = "anu_quick_notes.txt"
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as f:
                content = f.read()
            if content:
                # Show last 500 characters
                preview = content[-500:] if len(content) > 500 else content
                return {"status": "success", "message": f"Your notes:\n{preview}"}
            else:
                return {"status": "success", "message": "No notes found"}
        else:
            return {"status": "success", "message": "No notes file exists yet"}
    except Exception as e:
        return {"status": "error", "message": f"Error reading notes: {str(e)}"}

def register():
    """Register clipboard and utilities skills"""
    from core.skill import Skill
    skill = Skill("clipboard")
    skill.register(
        name="copy_to_clipboard",
        func=copy_to_clipboard,
        description="Copy text to system clipboard",
        parameters={
            "text": {"type": "string", "description": "Text to copy"}
        },
        required=["text"]
    )
    
    skill.register(
        name="get_clipboard",
        func=get_clipboard,
        description="Get text from system clipboard",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="send_notification",
        func=send_notification,
        description="Send a system notification",
        parameters={
            "title": {"type": "string", "description": "Notification title"},
            "message": {"type": "string", "description": "Notification message"},
            "sound": {"type": "boolean", "description": "Play sound (default: true)"}
        },
        required=["title", "message"]
    )
    
    skill.register(
        name="text_to_speech",
        func=text_to_speech,
        description="Convert text to speech with custom voice",
        parameters={
            "text": {"type": "string", "description": "Text to speak"},
            "voice": {"type": "string", "description": "Voice name (default: Samantha)"},
            "rate": {"type": "integer", "description": "Speech rate (default: 165)"}
        },
        required=["text"]
    )
    
    skill.register(
        name="create_quick_note",
        func=create_quick_note,
        description="Create a quick note with timestamp",
        parameters={
            "note_text": {"type": "string", "description": "Note content"}
        },
        required=["note_text"]
    )
    
    skill.register(
        name="read_notes",
        func=read_notes,
        description="Read all quick notes",
        parameters={},
        required=[]
    )

    print("Loaded skill: clipboard_utils_skill")
    return skill
