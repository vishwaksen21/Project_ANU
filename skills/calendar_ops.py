"""
Calendar Operations Skill for ANU
Manage calendar events on macOS
"""

import subprocess
import os
from datetime import datetime, timedelta
from core.skill import Skill

def add_calendar_event(title, start_time=None, duration=60, notes=""):
    """
    Add an event to the default calendar
    
    Args:
        title: Event title/description
        start_time: Start time (e.g., "2026-02-14 15:30" or "in 2 hours" or "tomorrow at 9am")
        duration: Duration in minutes (default: 60)
        notes: Additional notes for the event
    """
    try:
        # Parse start_time
        if not start_time:
            # Default to 1 hour from now
            event_start = datetime.now() + timedelta(hours=1)
        elif "in" in start_time.lower():
            # Parse relative time like "in 2 hours", "in 30 minutes"
            event_start = _parse_relative_time(start_time)
        elif "tomorrow" in start_time.lower():
            # Parse "tomorrow at 9am"
            event_start = _parse_tomorrow_time(start_time)
        else:
            # Try to parse absolute time
            try:
                event_start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            except:
                try:
                    event_start = datetime.strptime(start_time, "%H:%M")
                    # Add today's date
                    event_start = datetime.now().replace(hour=event_start.hour, minute=event_start.minute, second=0, microsecond=0)
                except:
                    return f"❌ Could not parse time '{start_time}'. Try formats like '15:30', '2026-02-14 15:30', 'in 2 hours', or 'tomorrow at 9am'"
        
        event_end = event_start + timedelta(minutes=duration)
        
        # Format dates for AppleScript
        start_str = event_start.strftime("%m/%d/%Y %I:%M %p")
        end_str = event_end.strftime("%m/%d/%Y %I:%M %p")
        
        # AppleScript to add event
        script = f'''
        tell application "Calendar"
            tell calendar "Calendar"
                make new event with properties {{summary:"{title}", start date:date "{start_str}", end date:date "{end_str}", description:"{notes}"}}
            end tell
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"❌ Error adding event: {result.stderr}"
        
        return f"✅ Event '{title}' added to your calendar!\n📅 {event_start.strftime('%B %d, %Y at %I:%M %p')} ({duration} minutes)"
        
    except Exception as e:
        return f"❌ Error adding calendar event: {str(e)}"


def get_todays_events():
    """Get today's calendar events"""
    try:
        # AppleScript to get today's events
        script = '''
        tell application "Calendar"
            set todayStart to current date
            set time of todayStart to 0
            set todayEnd to todayStart + (24 * hours)
            
            set eventList to {}
            repeat with cal in calendars
                set calEvents to (every event of cal whose start date ≥ todayStart and start date < todayEnd)
                repeat with evt in calEvents
                    set eventInfo to (summary of evt) & "|" & (start date of evt as string) & "|" & (end date of evt as string)
                    set end of eventList to eventInfo
                end repeat
            end repeat
            return eventList
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"❌ Error getting events: {result.stderr}"
        
        output = result.stdout.strip()
        
        if not output:
            return "📅 No events scheduled for today."
        
        # Parse events
        events = output.split(", ")
        
        if not events:
            return "📅 No events scheduled for today."
        
        response = "📅 Today's Schedule:\n\n"
        
        for i, event_data in enumerate(events, 1):
            try:
                parts = event_data.split("|")
                if len(parts) >= 2:
                    title = parts[0].strip()
                    start = parts[1].strip()
                    
                    response += f"{i}. {title}\n"
                    response += f"   Time: {start}\n\n"
            except:
                continue
        
        return response.strip()
        
    except Exception as e:
        return f"❌ Error getting events: {str(e)}"


def get_upcoming_events(days=7):
    """
    Get upcoming events for the next N days
    
    Args:
        days: Number of days to look ahead (default: 7)
    """
    try:
        script = f'''
        tell application "Calendar"
            set startDate to current date
            set endDate to startDate + ({days} * days)
            
            set eventList to {{}}
            repeat with cal in calendars
                set calEvents to (every event of cal whose start date ≥ startDate and start date < endDate)
                repeat with evt in calEvents
                    set eventInfo to (summary of evt) & "|" & (start date of evt as string)
                    set end of eventList to eventInfo
                end repeat
            end repeat
            return eventList
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"❌ Error getting upcoming events: {result.stderr}"
        
        output = result.stdout.strip()
        
        if not output:
            return f"📅 No events scheduled for the next {days} days."
        
        events = output.split(", ")
        
        response = f"📅 Upcoming Events (Next {days} Days):\n\n"
        
        for i, event_data in enumerate(events, 1):
            try:
                parts = event_data.split("|")
                if len(parts) >= 2:
                    title = parts[0].strip()
                    start = parts[1].strip()
                    
                    response += f"{i}. {title}\n"
                    response += f"   {start}\n\n"
            except:
                continue
        
        return response.strip()
        
    except Exception as e:
        return f"❌ Error getting upcoming events: {str(e)}"


def _parse_relative_time(time_str):
    """Parse relative time like 'in 2 hours', 'in 30 minutes'"""
    time_str = time_str.lower()
    now = datetime.now()
    
    if "hour" in time_str:
        hours = int(''.join(filter(str.isdigit, time_str)))
        return now + timedelta(hours=hours)
    elif "minute" in time_str:
        minutes = int(''.join(filter(str.isdigit, time_str)))
        return now + timedelta(minutes=minutes)
    elif "day" in time_str:
        days = int(''.join(filter(str.isdigit, time_str)))
        return now + timedelta(days=days)
    else:
        return now + timedelta(hours=1)


def _parse_tomorrow_time(time_str):
    """Parse time like 'tomorrow at 9am', 'tomorrow at 15:30'"""
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Extract time part
    if "at" in time_str:
        time_part = time_str.split("at")[-1].strip()
        
        # Parse formats like "9am", "9:30am", "15:30"
        time_part = time_part.replace("am", "").replace("pm", "").strip()
        
        if ":" in time_part:
            parts = time_part.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
        else:
            hour = int(time_part)
            minute = 0
        
        # Adjust for PM if specified
        if "pm" in time_str.lower() and hour < 12:
            hour += 12
        
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
    else:
        # Default to 9am
        return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)


# Register the skill
def register():
    class CalendarSkill(Skill):
        @property
        def name(self):
            return "calendar_skill"
        
        def get_tools(self):
            return [
                {
                    "type": "function",
                    "function": {
                        "name": "add_calendar_event",
                        "description": "Add an event to the calendar. Supports various time formats: absolute ('2026-02-14 15:30'), relative ('in 2 hours'), or descriptive ('tomorrow at 9am')",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Event title/description"
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Start time. Formats: '15:30', '2026-02-14 15:30', 'in 2 hours', 'tomorrow at 9am'. Leave empty for 1 hour from now."
                                },
                                "duration": {
                                    "type": "integer",
                                    "description": "Duration in minutes (default: 60)",
                                    "default": 60
                                },
                                "notes": {
                                    "type": "string",
                                    "description": "Additional notes for the event",
                                    "default": ""
                                }
                            },
                            "required": ["title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_todays_events",
                        "description": "Get all events scheduled for today",
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
                        "name": "get_upcoming_events",
                        "description": "Get upcoming events for the next N days",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "days": {
                                    "type": "integer",
                                    "description": "Number of days to look ahead (default: 7)",
                                    "default": 7
                                }
                            },
                            "required": []
                        }
                    }
                }
            ]
        
        def get_functions(self):
            return {
                "add_calendar_event": add_calendar_event,
                "get_todays_events": get_todays_events,
                "get_upcoming_events": get_upcoming_events
            }
    
    return CalendarSkill()
