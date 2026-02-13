import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Set voice to pleasant Indian-style female voice
def set_female_voice():
    voices = engine.getProperty('voices')
    
    # Try sweet female voices with adjustments for Indian accent feel
    # Preferences: Samantha (most natural), Karen (Australian - closer to Indian English), Moira (Irish - sweet)
    preferred_voices = [
        ("Samantha", 165, 0.95),  # Slightly slower, fuller volume for sweet tone
        ("Karen", 170, 0.95),     # Australian English is closer to Indian English
        ("Moira", 168, 0.95),     # Irish accent, very sweet
        ("Tessa", 170, 0.95),     # South African, also pleasant
        ("Kate", 165, 0.95),      # British, elegant
        ("Victoria", 165, 0.95),  # Also very clear
    ]
    
    for voice_name, rate, volume in preferred_voices:
        for voice in voices:
            if voice_name in voice.name:
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', rate)  # Slightly slower for sweeter sound
                engine.setProperty('volume', volume)  # Fuller volume
                # Add slight pitch variation for sweeter tone
                engine.setProperty('pitch', 1.1)  # Slightly higher pitch (if supported)
                print(f"Voice set to: {voice_name} (Sweet Indian-style female)")
                return
    
    # Last fallback to any female voice
    for voice in voices:
        if "female" in voice.name.lower() or "female" in str(voice.gender).lower():
             engine.setProperty('voice', voice.id)
             engine.setProperty('rate', 165)
             engine.setProperty('volume', 0.95)
             return

set_female_voice()

# Global flag to check if Jarvis is speaking
is_speaking = False

def speak(text):
    global is_speaking
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
    
    # Print first so user sees it even if audio fails
    print(f"ANU: {text}")

    # Set flag to True before speaking
    is_speaking = True
    
    try:
        # On macOS with a GUI/Threading environment, pyttsx3's loop often conflicts 
        # with the main thread event loop (PyQt). Default to system 'say' command on macOS
        # to avoid hangs/crashes unless we are strictly in a non-GUI text mode.
        if sys.platform == "darwin":
            try:
                # Escape quotes to prevent shell injection/errors
                clean_text = text.replace('"', '\\"').replace("'", "")
                # Use Samantha voice with rate adjustment for sweeter, Indian-style speech
                # Rate 165 is slightly slower for a more gentle, caring tone
                os.system(f'say -v Samantha -r 165 "{clean_text}"')
                return
            except Exception as e2:
                print(f"TTS Fallback Error: {e2}")
                # Fall through to pyttsx3 if 'say' fails (unlikely)
    
        # Try pyttsx3
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            
    finally:
        # Ensure flag is reset to False even if errors occur
        is_speaking = False

def listen():
    global is_speaking
    # if system is speaking, don't listen
    if is_speaking:
        return "none"

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio)
            return query.lower()
        except Exception:
            return "none"
