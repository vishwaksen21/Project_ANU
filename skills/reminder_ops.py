"""
Reminder Skill - Set reminders and get notifications
"""
import json
import os
from datetime import datetime, timedelta

REMINDERS_FILE = "reminders.json"

def load_reminders():
    """Load reminders from file"""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    """Save reminders to file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def set_reminder(task: str, time_minutes: int = 60) -> dict:
    """
    Set a reminder for a task.
    
    Args:
        task: What to be reminded about
        time_minutes: Time in minutes from now (default: 60)
    
    Returns:
        Confirmation message
    """
    try:
        reminders = load_reminders()
        
        reminder_time = datetime.now() + timedelta(minutes=time_minutes)
        
        reminder = {
            "task": task,
            "time": reminder_time.isoformat(),
            "created": datetime.now().isoformat()
        }
        
        reminders.append(reminder)
        save_reminders(reminders)
        
        time_str = reminder_time.strftime("%I:%M %p")
        return {
            "status": "success",
            "message": f"✓ I'll remind you to '{task}' at {time_str}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to set reminder: {str(e)}"}

def list_reminders() -> dict:
    """
    List all active reminders.
    
    Returns:
        List of reminders
    """
    try:
        reminders = load_reminders()
        
        if not reminders:
            return {"status": "success", "message": "You have no reminders set."}
        
        active_reminders = []
        for reminder in reminders:
            reminder_time = datetime.fromisoformat(reminder['time'])
            if reminder_time > datetime.now():
                time_str = reminder_time.strftime("%I:%M %p on %B %d")
                active_reminders.append(f"• {reminder['task']} - {time_str}")
        
        if not active_reminders:
            return {"status": "success", "message": "You have no active reminders."}
        
        return {
            "status": "success",
            "message": f"Your reminders:\n" + "\n".join(active_reminders)
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to list reminders: {str(e)}"}

def clear_reminders() -> dict:
    """
    Clear all reminders.
    
    Returns:
        Confirmation message
    """
    try:
        save_reminders([])
        return {"status": "success", "message": "✓ All reminders cleared"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear reminders: {str(e)}"}

def register():
    """Register reminder skills"""
    from core.skill import Skill
    skill = Skill("reminders")
    skill.register(
        name="set_reminder",
        func=set_reminder,
        description="Set a reminder for a task at a specific time",
        parameters={
            "task": {"type": "string", "description": "What to be reminded about"},
            "time_minutes": {"type": "integer", "description": "Time in minutes from now (default: 60)"}
        },
        required=["task"]
    )
    
    skill.register(
        name="list_reminders",
        func=list_reminders,
        description="List all active reminders",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="clear_reminders",
        func=clear_reminders,
        description="Clear all reminders",
        parameters={},
        required=[]
    )

    print("Loaded skill: reminder_skill")
    return skill
