"""
Advanced System Control - Full system and application access
"""
import os
import subprocess
import json

def open_application(app_name: str) -> dict:
    """
    Open any application on macOS.
    
    Args:
        app_name: Name of the application (e.g., "Safari", "Chrome", "VS Code")
    
    Returns:
        Status message
    """
    try:
        # Common application mappings
        app_mappings = {
            "chrome": "Google Chrome",
            "safari": "Safari",
            "firefox": "Firefox",
            "vscode": "Visual Studio Code",
            "code": "Visual Studio Code",
            "terminal": "Terminal",
            "finder": "Finder",
            "mail": "Mail",
            "messages": "Messages",
            "facetime": "FaceTime",
            "notes": "Notes",
            "calendar": "Calendar",
            "photos": "Photos",
            "music": "Music",
            "spotify": "Spotify",
            "slack": "Slack",
            "discord": "Discord",
            "zoom": "zoom.us",
            "whatsapp": "WhatsApp",
            "telegram": "Telegram",
            "calculator": "Calculator",
            "settings": "System Settings",
            "preferences": "System Settings",
            "xcode": "Xcode",
            "word": "Microsoft Word",
            "excel": "Microsoft Excel",
            "powerpoint": "Microsoft PowerPoint",
            "notion": "Notion",
            "obsidian": "Obsidian",
        }
        
        # Normalize app name
        app_name_lower = app_name.lower().strip()
        actual_app_name = app_mappings.get(app_name_lower, app_name)
        
        # Use AppleScript to open application
        script = f'tell application "{actual_app_name}" to activate'
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            return {"status": "success", "message": f"✓ Opened {actual_app_name}"}
        else:
            # Try using 'open' command as fallback
            result2 = subprocess.run(['open', '-a', actual_app_name], 
                                   capture_output=True, text=True, timeout=5)
            if result2.returncode == 0:
                return {"status": "success", "message": f"✓ Opened {actual_app_name}"}
            else:
                return {"status": "error", "message": f"Could not find application: {app_name}"}
    except Exception as e:
        return {"status": "error", "message": f"Error opening app: {str(e)}"}

def close_application(app_name: str) -> dict:
    """
    Close/quit an application.
    
    Args:
        app_name: Name of the application to close
    
    Returns:
        Status message
    """
    try:
        script = f'tell application "{app_name}" to quit'
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            return {"status": "success", "message": f"✓ Closed {app_name}"}
        else:
            # Try killall as fallback
            subprocess.run(['killall', app_name], capture_output=True)
            return {"status": "success", "message": f"✓ Terminated {app_name}"}
    except Exception as e:
        return {"status": "error", "message": f"Error closing app: {str(e)}"}

def get_running_apps() -> dict:
    """
    List all currently running applications.
    
    Returns:
        List of running apps
    """
    try:
        script = '''
        tell application "System Events"
            get name of every process whose background only is false
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            apps = result.stdout.strip().split(", ")
            apps_list = "\n• ".join(apps[:15])  # Show first 15 apps
            return {"status": "success", "message": f"Running applications:\n• {apps_list}"}
        else:
            return {"status": "error", "message": "Could not get running apps"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def execute_terminal_command(command: str) -> dict:
    """
    Execute a safe terminal command.
    
    Args:
        command: Terminal command to execute (safe commands only)
    
    Returns:
        Command output
    """
    try:
        # Whitelist of safe commands
        safe_commands = [
            'ls', 'pwd', 'date', 'whoami', 'hostname', 'uptime', 
            'df', 'du', 'top', 'ps', 'which', 'echo', 'cal', 'bc'
        ]
        
        # Extract the base command
        base_cmd = command.strip().split()[0]
        
        if base_cmd not in safe_commands:
            return {"status": "error", "message": f"Command '{base_cmd}' is not in the safe list"}
        
        # Execute command
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, timeout=10)
        
        output = result.stdout[:500]  # Limit output
        if result.returncode == 0:
            return {"status": "success", "message": f"Output:\n{output}"}
        else:
            return {"status": "error", "message": f"Error: {result.stderr[:200]}"}
    except Exception as e:
        return {"status": "error", "message": f"Command error: {str(e)}"}

def lock_screen() -> dict:
    """
    Lock the computer screen.
    
    Returns:
        Status message
    """
    try:
        subprocess.run(['pmset', 'displaysleepnow'], check=True)
        return {"status": "success", "message": "✓ Screen locked"}
    except:
        # Fallback method
        try:
            script = '''
            tell application "System Events"
                keystroke "q" using {control down, command down}
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return {"status": "success", "message": "✓ Screen locked"}
        except Exception as e:
            return {"status": "error", "message": f"Could not lock screen: {str(e)}"}

def empty_trash() -> dict:
    """
    Empty the trash/bin.
    
    Returns:
        Status message
    """
    try:
        script = '''
        tell application "Finder"
            empty trash
        end tell
        '''
        subprocess.run(['osascript', '-e', script], timeout=30)
        return {"status": "success", "message": "✓ Trash emptied"}
    except Exception as e:
        return {"status": "error", "message": f"Error emptying trash: {str(e)}"}

def get_system_info() -> dict:
    """
    Get comprehensive system information.
    
    Returns:
        System information
    """
    try:
        # Get various system info
        info = []
        
        # macOS version
        version = subprocess.run(['sw_vers', '-productVersion'], 
                               capture_output=True, text=True).stdout.strip()
        info.append(f"macOS: {version}")
        
        # Computer name
        name = subprocess.run(['scutil', '--get', 'ComputerName'], 
                            capture_output=True, text=True).stdout.strip()
        info.append(f"Computer: {name}")
        
        # CPU info
        cpu = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                           capture_output=True, text=True).stdout.strip()
        info.append(f"CPU: {cpu}")
        
        # Memory
        mem = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                           capture_output=True, text=True).stdout.strip()
        mem_gb = int(mem) / (1024**3)
        info.append(f"Memory: {mem_gb:.1f} GB")
        
        # Disk space
        df_output = subprocess.run(['df', '-h', '/'], 
                                  capture_output=True, text=True).stdout
        disk_line = df_output.split('\n')[1]
        disk_parts = disk_line.split()
        info.append(f"Disk: {disk_parts[3]} free of {disk_parts[1]}")
        
        # Uptime
        uptime = subprocess.run(['uptime'], 
                              capture_output=True, text=True).stdout.strip()
        info.append(f"Uptime: {uptime.split('up')[1].split(',')[0].strip()}")
        
        return {"status": "success", "message": "System Information:\n• " + "\n• ".join(info)}
    except Exception as e:
        return {"status": "error", "message": f"Error getting system info: {str(e)}"}

def register(registry):
    """Register advanced system control skills"""
    registry.register(
        name="open_application",
        func=open_application,
        description="Open any application (Safari, Chrome, VS Code, Spotify, etc.)",
        parameters={
            "app_name": {"type": "string", "description": "Name of the application to open"}
        },
        required=["app_name"]
    )
    
    registry.register(
        name="close_application",
        func=close_application,
        description="Close/quit an application",
        parameters={
            "app_name": {"type": "string", "description": "Name of the application to close"}
        },
        required=["app_name"]
    )
    
    registry.register(
        name="get_running_apps",
        func=get_running_apps,
        description="List all currently running applications",
        parameters={},
        required=[]
    )
    
    registry.register(
        name="execute_terminal_command",
        func=execute_terminal_command,
        description="Execute safe terminal commands (ls, pwd, date, whoami, etc.)",
        parameters={
            "command": {"type": "string", "description": "Terminal command to execute"}
        },
        required=["command"]
    )
    
    registry.register(
        name="lock_screen",
        func=lock_screen,
        description="Lock the computer screen",
        parameters={},
        required=[]
    )
    
    registry.register(
        name="empty_trash",
        func=empty_trash,
        description="Empty the trash/bin",
        parameters={},
        required=[]
    )
    
    registry.register(
        name="get_system_info",
        func=get_system_info,
        description="Get comprehensive system information (OS, CPU, memory, disk, uptime)",
        parameters={},
        required=[]
    )

    print("Loaded skill: advanced_system_skill")
