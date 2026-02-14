import os
import sys
import argparse
import threading 
import time
from dotenv import load_dotenv
from core.voice import speak, listen
from core.registry import SkillRegistry
from core.engine import AnuEngine
from gui.app import run_gui as run_gui_app

# Load Env
load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY not found.")
    sys.exit(1)

def anu_loop(pause_event, registry, args):
    """
    Main loop for ANU, running in a separate thread.
    Checks pause_event to determine if it should listen/process.
    """
    # Initialize Engine
    anu = AnuEngine(registry)

    if args.text:
        print("ANU: Hello! I'm ANU, your AI assistant. How can I help you today? (Text Mode)")
    else:
        speak("Hello! I'm ANU, your AI assistant. How can I help you today?")

    while True:
        # Check for pause
        if pause_event.is_set():
            time.sleep(0.5)
            continue

        if args.text:
            try:
                user_query = input("YOU: ").lower()
            except EOFError:
                break
        else:
            user_query = listen()
            
        # Double check pause after listening (in case paused during listen)
        if pause_event.is_set():
            continue

        if user_query == "none" or not user_query: continue
        
        if "quit" in user_query: 
            print("Shutting down ANU...")
            speak("Goodbye! Have a wonderful day!")
            break
        
        # Wake word / Command filtering Logic
        direct_commands = [
            "open", "volume", "search", "create", "write", "read", "make",
            "who", "what", "when", "where", "how", "why", "thank", "hello", "hi",
            "import", "add", "send", "message", "list", "show", "tell", "play"
        ]
        
        is_direct = any(cmd in user_query for cmd in direct_commands)
        
        # Changed wake word from "jarvis" to "anu"
        if "anu" not in user_query and not is_direct:
            print(f"Ignored: {user_query}")
            continue
            
        clean_query = user_query.replace("anu", "").strip()
        
        try:
            print(f"Thinking: {clean_query}")
            response = anu.run_conversation(clean_query)
            
            # Check pause before speaking response
            if pause_event.is_set():
                continue

            if response:
                if args.text:
                    print(f"ANU: {response}")
                else:
                    speak(response)
        except Exception as e:
            print(f"Main Loop Error: {e}")
            if args.text:
                print("ANU: I'm experiencing a system error. Please try again.")
            else:
                speak("I'm experiencing a system error. Please try again.")

def main():
    print("Starting ANU...")
    parser = argparse.ArgumentParser(description="ANU - AI Assistant")
    parser.add_argument("--text", action="store_true", help="Run in text mode (no voice I/O)")
    args = parser.parse_args()

    # 1. Setup Pause Event
    pause_event = threading.Event()
    context = {"pause_event": pause_event}

    # 2. Initialize Registry and Load Skills
    print("Loading skills...")
    registry = SkillRegistry()
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    registry.load_skills(skills_dir, context=context)
    
    # 3. Start ANU Loop in Background Thread
    print("Starting ANU...")
    t = threading.Thread(target=anu_loop, args=(pause_event, registry, args), daemon=True)
    t.start()
    
    # 4. Start GUI in Main Thread (Required for PyQt)
    print("Launching GUI...")
    run_gui_app(pause_event)

if __name__ == "__main__":
    main()
