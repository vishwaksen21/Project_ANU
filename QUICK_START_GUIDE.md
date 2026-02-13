# 🌸 ANU - Quick Start Guide

## 🎀 Meet ANU!

ANU is your friendly, caring AI assistant with a beautiful feminine interface and warm personality!

---

## 🚀 Starting ANU

```bash
cd Project_JARVIS
python3 main.py
```

The beautiful pink-purple GUI will open, and ANU will greet you!

---

## 💬 How to Talk to ANU

### Wake Word: "ANU"

Just say "ANU" followed by your request:

```
"ANU, what time is it?"
"ANU, how are you today?"
"ANU, help me with something"
```

### Direct Commands (No Wake Word Needed)

For common actions, you can skip the wake word:

```
"What's the weather?"
"Open Google"
"Search for..."
"Create a file"
"Hello!"
"Thank you"
```

---

## 🎨 Beautiful Interface Features

### 🌺 Central Reactor
- **Flower/star pattern** that pulses with ANU's activity
- **Pink-purple gradients** flowing smoothly
- **Sparkle effects** orbiting around the core

### 🎪 Color Meanings
- **Pink Glow** = ANU is active and listening
- **Deep Pink** = ANU is paused (click to resume)
- **Purple Accents** = Decorative animations

### 🖱️ GUI Controls
- **Click anywhere** → Pause/Resume ANU
- **Press ESC** → Close ANU
- **Enjoy the animations** → Watch the sparkles!

---

## 🆕 NEW FEATURES

### 1. 📝 Reminders

**Set a Reminder:**
```
"ANU, remind me to call mom in 30 minutes"
"ANU, set a reminder to exercise in 1 hour"
"ANU, remind me about the meeting in 2 hours"
```

**Check Reminders:**
```
"ANU, what are my reminders?"
"ANU, list my reminders"
```

**Clear Reminders:**
```
"ANU, clear all reminders"
"ANU, delete my reminders"
```

### 2. 🎭 Fun & Entertainment

**Tell a Joke:**
```
"ANU, tell me a joke"
"ANU, make me laugh"
```

**Share a Fun Fact:**
```
"ANU, tell me something interesting"
"ANU, share a fun fact"
```

**Motivate Me:**
```
"ANU, I need motivation"
"ANU, inspire me"
"ANU, give me encouragement"
```

**Compliment Me:**
```
"ANU, compliment me"
"ANU, say something nice"
```

### 3. 🎵 Music Control

**Play Music:**
```
"ANU, play some music"
"ANU, play my favorite song"
```

**Control Playback:**
```
"ANU, pause music"
"ANU, next track"
"ANU, previous song"
```

---

## 💡 Existing Features

### 🌐 Web & Search
```
"ANU, search for Python tutorials"
"ANU, open YouTube"
"ANU, Google artificial intelligence"
```

### 📧 Communication
```
"ANU, send an email"
"ANU, send a WhatsApp message"
```

### 📸 Vision & Camera
```
"ANU, take a photo"
"ANU, take a screenshot"
"ANU, detect objects"
```

### 🗂️ File Management
```
"ANU, create a file called notes.txt"
"ANU, read my file"
"ANU, list my files"
```

### ⚙️ System Control
```
"ANU, what's the volume?"
"ANU, increase brightness"
"ANU, open settings"
```

### 📅 Time & Date
```
"ANU, what time is it?"
"ANU, what's today's date?"
```

### 🌤️ Weather
```
"ANU, what's the weather?"
"ANU, will it rain today?"
```

### 📝 Notes & Memory
```
"ANU, remember that I like coffee"
"ANU, what do you remember about me?"
```

---

## 🎤 Voice Tips

ANU uses **Samantha's voice** - a pleasant, natural-sounding female voice!

### For Best Results:
1. Speak clearly and naturally
2. Use the wake word "ANU" for better recognition
3. Keep background noise minimal
4. Speak at a normal pace

---

## 🎨 Customization Ideas

Want to make ANU even more yours? Here are some ideas:

### Change Colors
Edit `gui/app.py` and modify:
```python
PRIMARY_COLOR = QColor("#FF69B4")  # Your favorite pink
SECONDARY_COLOR = QColor("#DA70D6")  # Your favorite purple
```

### Add Your Own Jokes
Edit `skills/fun_ops.py` and add to the `JOKES` list!

### Change Voice Speed
Edit `core/voice.py`:
```python
engine.setProperty('rate', 175)  # Slower: 150, Faster: 200
```

---

## 🔧 Troubleshooting

### ANU Not Responding to Voice?
1. Check microphone permissions
2. Ensure PyAudio is installed
3. Try text mode: `python3 main.py --text`

### GUI Not Showing?
1. Ensure PyQt6 is installed
2. Check if DISPLAY is set (if on SSH)
3. Try: `pip3 install PyQt6 --upgrade`

### Voice Not Working?
1. ANU uses macOS's 'say' command
2. Test: `say -v Samantha "Hello"`
3. If it works, ANU's voice should work too!

---

## 💝 ANU's Personality

ANU is designed to be:
- **Caring** - Always supportive and understanding
- **Friendly** - Warm and approachable
- **Helpful** - Ready to assist with any task
- **Positive** - Encouraging and uplifting
- **Smart** - Intelligent and capable

---

## 🌟 Fun Interactions

Try these fun commands:

```
"ANU, how are you?"
"ANU, tell me about yourself"
"ANU, what can you do?"
"ANU, thank you"
"ANU, you're amazing"
"ANU, I need help"
"ANU, cheer me up"
```

---

## 📞 Example Conversation

**You:** "ANU, hello!"

**ANU:** "Hello! I'm ANU, your AI assistant. How can I help you today?"

**You:** "ANU, tell me a joke"

**ANU:** "Why don't scientists trust atoms? Because they make up everything!"

**You:** "ANU, that's funny! Remind me to laugh again in 10 minutes"

**ANU:** "✓ I'll remind you to 'laugh again' at 2:45 PM"

**You:** "ANU, what's the weather?"

**ANU:** "Let me check the weather for you..."

**You:** "ANU, play some music"

**ANU:** "♪ Music started"

**You:** "Thank you ANU!"

**ANU:** "You're welcome! I'm always here to help!"

---

## 🎉 Enjoy ANU!

ANU is here to make your day brighter, help you be more productive, and be a caring companion.

**Remember:**
- Wake word: **"ANU"**
- Pause/Resume: **Click anywhere on GUI**
- Exit: **Press ESC**
- Have fun! **💕**

---

*Made with 💖*
*Your friendly AI companion, ANU* 🌸
