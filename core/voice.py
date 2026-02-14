import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Set voice to classic Indian girl with cute voice
def set_female_voice():
    voices = engine.getProperty('voices')
    
    # Try voices optimized for cute, sweet Indian girl sound
    # Preferences: Veena (Indian), Nicky (faster, cuter), Samantha (most natural), Karen (Australian)
    preferred_voices = [
        ("Veena", 175, 0.98),      # Indian English - if available (High priority!)
        ("Nicky", 180, 0.98),      # Young, cute sounding
        ("Samantha", 170, 0.98),   # Natural, slightly faster for cuteness
        ("Karen", 175, 0.98),      # Australian English (similar to Indian English)
        ("Moira", 175, 0.98),      # Irish accent, very sweet
        ("Tessa", 175, 0.98),      # South African, pleasant
    ]
    
    for voice_name, rate, volume in preferred_voices:
        for voice in voices:
            if voice_name in voice.name:
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', rate)  # Balanced for cute, energetic tone
                engine.setProperty('volume', volume)  # Full, clear volume
                # Higher pitch for cuter, more youthful sound
                try:
                    engine.setProperty('pitch', 1.2)  # Higher pitch for cute voice
                except:
                    pass  # Some engines don't support pitch
                print(f"Voice set to: {voice_name} (Classic Indian girl with cute voice)")
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
                # Try Veena (Indian English) first, then Nicky (cute), then Samantha
                # Rate 175-180 for energetic, cute tone with higher pitch
                # Try voices in priority order
                voice_options = [
                    ("Veena", 180),    # Indian English
                    ("Nicky", 185),    # Cute, young sounding
                    ("Samantha", 175), # Natural fallback
                ]
                
                # Check which voices are available
                available_voices = os.popen('say -v "?"').read().lower()
                
                for voice, rate in voice_options:
                    if voice.lower() in available_voices:
                        os.system(f'say -v {voice} -r {rate} "{clean_text}"')
                        return
                
                # Ultimate fallback
                os.system(f'say -v Samantha -r 175 "{clean_text}"')
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
