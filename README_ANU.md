# ANU - AI Assistant 💖

A beautiful, voice-controlled AI assistant featuring a stunning feminine-themed HUD interface, advanced automation skills, and a warm, supportive personality. Transformed from JARVIS with love!

## 🌸 What's New in ANU

### ✨ Personality & Voice
- **Female Voice**: Uses Samantha voice on macOS for pleasant, natural speech
- **Warm Personality**: Friendly, caring, and supportive responses
- **New Wake Word**: Say "ANU" instead of "JARVIS"

### 🎨 Beautiful Girl-Themed Interface
- **Color Palette**: 
  - Hot Pink (#FF69B4) & Orchid Purple (#DA70D6)
  - Light Pink accents (#FFB6C1)
  - Deep purple background (#1A0033)
- **Central Reactor**: Flower/star pattern with pulsing glow effects
- **Gradient Visualizations**: Beautiful pink-purple gradients throughout
- **Sparkle Effects**: Twinkling particles around the interface
- **Smooth Animations**: Elegant, flowing movements

### 🚀 New Features

#### 1. **Reminder System** 📝
- Set reminders for tasks
- List all active reminders
- Clear reminders
```
"ANU, remind me to call mom in 30 minutes"
"ANU, what are my reminders?"
"ANU, clear all reminders"
```

#### 2. **Fun & Entertainment** 🎭
- Tell jokes
- Share fun facts
- Motivational quotes
- Sweet compliments
```
"ANU, tell me a joke"
"ANU, share a fun fact"
"ANU, I need motivation"
"ANU, compliment me"
```

#### 3. **Music Control** 🎵
- Play music
- Pause/Resume
- Next/Previous track
```
"ANU, play some music"
"ANU, pause music"
"ANU, next track"
```

## 🌟 Core Features

### 🎤 Dual Modes
- **Voice Mode**: Full hands-free interaction with Samantha's voice
- **Text Mode**: Silent command-line interface (`--text` flag)

### 🧠 Existing Skills

#### 🌐 Web & Communication
- **Web Operations**: Google searches, open websites
- **WhatsApp**: Automated messaging
- **Email**: Email management

#### 👁️ Vision & Sensing
- **Computer Vision**: Real-time object detection (YOLO)
- **Camera Access**: Photo capture and processing
- **Screen Awareness**: Screenshots and analysis
- **Gemini Live**: Advanced multimodal interaction

#### 🛠️ System Control
- **System Operations**: Volume, brightness, app management
- **File Management**: Create, read, organize files
- **Context Awareness**: Date, time, memory tracking

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- macOS (for Samantha voice and some features)
- [Groq API Key](https://console.groq.com/)
- [Gemini API Key](https://ai.google.dev/) (optional)

### Installation

1. **Clone the Repository**
   ```bash
   cd Project_JARVIS
   ```

2. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Setup Environment Variables**
   
   Create a `.env` file:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key  # Optional
   ```

4. **Run ANU**
   ```bash
   python3 main.py
   ```

   Or in text mode:
   ```bash
   python3 main.py --text
   ```

## 💬 Usage Examples

### Wake Word
Use "ANU" as the wake word:
```
"ANU, what time is it?"
"ANU, search for Python tutorials"
"ANU, take a screenshot"
"ANU, tell me a joke"
"ANU, remind me to exercise in 1 hour"
```

### Direct Commands (No wake word needed)
```
"What's the weather?"
"Open Google"
"Create a file"
"Thank you"
```

### GUI Controls
- **Click anywhere**: Pause/Resume ANU
- **ESC key**: Close the application
- **Pink glow**: ANU is active
- **Deep pink**: ANU is paused

## 🎨 Interface Details

### Central Reactor
- Flower/star pattern core with gradient colors
- Pulsing animation synchronized with activity
- Sparkle particles orbiting around

### Side Panels
- **Left**: Hexagonal pattern with alternating pink/purple
- **Right**: Gradient equalizer bars showing activity

### Color Theme
- Primary: Hot Pink (#FF69B4)
- Secondary: Orchid Purple (#DA70D6)
- Accent: Light Pink (#FFB6C1)
- Background: Deep Purple (#1A0033)

## 📋 Requirements

All required packages are in `requirements.txt`:
- groq>=0.4.2
- python-dotenv>=1.0.0
- requests>=2.31.0
- pyttsx3>=2.90
- SpeechRecognition>=3.8.1
- PyAudio>=0.2.11
- PyQt6>=6.6.0
- Pillow>=10.0.0
- opencv-python
- ultralytics
- torch
- torchvision
- pywhatkit
- selenium
- webdriver-manager

## 🔧 Technical Details

### Architecture
- **Engine**: AnuEngine (LLM-powered with Groq)
- **Voice**: Samantha voice via macOS TTS
- **GUI**: PyQt6 with custom painting
- **Skills**: Modular plugin system

### Skills Location
All skills are in the `skills/` directory:
- `datetime_ops.py` - Date/time operations
- `email_ops.py` - Email management
- `file_ops.py` - File operations
- `fun_ops.py` - Jokes and entertainment ✨ NEW
- `memory_ops.py` - Memory/notes
- `music_ops.py` - Music control ✨ NEW
- `reminder_ops.py` - Reminder system ✨ NEW
- `screenshot_ops.py` - Screenshot tools
- `system_ops.py` - System control
- `text_ops.py` - Text processing
- `vision_skill.py` - Computer vision
- `weather_ops.py` - Weather info
- `web_ops.py` - Web operations
- `whatsapp_skill.py` - WhatsApp automation

## 🤝 Contributing

Feel free to add more skills or enhance the interface! The modular design makes it easy to extend ANU's capabilities.

### Adding a New Skill

1. Create a new file in `skills/` directory
2. Define functions with type hints
3. Create a `register(registry)` function
4. ANU will automatically load it on startup!

## 📜 License

This project is open source and available under the MIT License.

## 💝 Credits

Transformed with love from JARVIS to ANU - your friendly, caring AI assistant!

---

**Made with 💖 by Vishwaksen**

Wake word: **ANU** 🌸
