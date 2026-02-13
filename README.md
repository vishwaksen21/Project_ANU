# 🌸 ANU - Your Caring AI Companion

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**ANU** is a powerful AI assistant with a sweet Indian-style voice, beautiful pink-purple interface, and 40+ intelligent features.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## ✨ What is ANU?

ANU is an advanced AI assistant designed to be your caring companion throughout the day. With a warm personality, natural voice interactions, and powerful capabilities, ANU helps you with everything from system control to entertainment.

### 🎯 Key Highlights

- 🎤 **Sweet Indian-Style Voice** - Natural female voice (Samantha, 165 WPM)
- 🎨 **Beautiful Interface** - Stunning pink-purple themed GUI with animations
- 🤖 **Powered by Groq** - Lightning-fast AI responses using Llama 3.3 70B
- 🚀 **40+ Features** - System control, calculations, WhatsApp, music, and more
- 💖 **Caring Personality** - Warm, supportive, and helpful responses
- 🔧 **macOS Optimized** - Deep integration with macOS features

---

## 🚀 Features

### 💻 System & Application Control
- Open and close any application
- Get system information
- Lock screen and manage system settings
- Execute safe terminal commands
- Monitor running applications
- Empty trash

### 📱 Communication
- **WhatsApp Integration** with automatic contact import
- Send messages hands-free
- Import all device contacts automatically
- Email operations
- Web search capabilities

### 🧮 Productivity Tools
- Advanced calculator (trigonometry, logarithms, etc.)
- Unit conversions (length, weight, temperature)
- Percentage and tip calculators
- Reminder system
- Quick notes creation
- Clipboard management
- System notifications

### 🎵 Entertainment
- Music control (play, pause, next, previous)
- Tell jokes
- Share fun facts
- Motivational quotes
- Personal compliments

### 📸 Vision & Capture
- Screenshot capture
- Camera control
- Object detection (YOLO)
- Vision analysis

### 📁 File Management
- Create and read files
- File operations
- Text-to-speech with custom voices
- Document management

### 🌤️ Information
- Weather forecasts
- Date and time
- Memory/preferences storage
- Web information retrieval

---

## 🛠️ Installation

### Prerequisites

- macOS (Apple Silicon or Intel)
- Python 3.10 or higher
- Groq API Key ([Get one free](https://console.groq.com))

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/vishwaksen21/Project_ANU.git
cd Project_ANU
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Keys**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Optional
```

4. **Run ANU**
```bash
python3 main.py
```

---

## 🎯 Usage

### Wake Word

ANU responds to her name or direct commands:

```
"ANU, what time is it?"
"ANU, open Safari"
"ANU, tell me a joke"
```

### Direct Commands (No Wake Word Needed)

These words automatically activate ANU:
- `import`, `add`, `send`, `message`, `list`, `show`, `tell`, `play`
- `open`, `volume`, `search`, `create`, `write`, `read`
- `who`, `what`, `when`, `where`, `how`, `why`

### Example Commands

**System Control:**
```
"Open Spotify"
"Close Safari"
"Lock screen"
"What's my system information?"
```

**WhatsApp:**
```
"Import all my contacts from my device"
"Add Ananya's WhatsApp contact with number +919876543210"
"Send Mom a message saying I'll be home late"
```

**Productivity:**
```
"Calculate square root of 144"
"Convert 50 kilometers to miles"
"Remind me to take a break in 30 minutes"
"What's 15% of 2000?"
```

**Entertainment:**
```
"Tell me a joke"
"Share a fun fact"
"Motivate me"
"Play music"
```

---

## 📚 Documentation

Comprehensive guides are available:

- **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)** - Complete feature overview
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Getting started tutorial
- **[COMPLETE_FEATURES_GUIDE.md](COMPLETE_FEATURES_GUIDE.md)** - Detailed feature documentation
- **[TRANSFORMATION_SUMMARY.md](TRANSFORMATION_SUMMARY.md)** - Development history

---

## 🎨 Interface

ANU features a beautiful pink-purple themed interface:

- **Color Scheme:** Hot pink (#FF69B4), Orchid purple (#DA70D6), Light pink (#FFB6C1)
- **Animations:** Flower/star reactor pattern with sparkle effects
- **Design:** Smooth gradients and elegant visualizations
- **Controls:** Click anywhere to pause/resume, ESC to close

---

## 🔧 Technical Stack

- **Language:** Python 3.14
- **GUI Framework:** PyQt6
- **AI Engine:** Groq API (Llama 3.3 70B)
- **Voice:** pyttsx3 + macOS TTS
- **Speech Recognition:** SpeechRecognition with Google API
- **Vision:** Ultralytics YOLO
- **WhatsApp:** Selenium WebDriver
- **System Integration:** AppleScript for macOS

---

## 📋 Requirements

Main dependencies:
- `PyQt6` - GUI framework
- `groq` - AI engine
- `pyttsx3` - Text-to-speech
- `SpeechRecognition` - Voice input
- `selenium` - WhatsApp automation
- `ultralytics` - Computer vision
- `python-dotenv` - Environment management

See `requirements.txt` for complete list.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **OpenAI** for inspiration
- **PyQt6** for the beautiful GUI framework
- **Ultralytics** for YOLO computer vision
- **macOS** for excellent system integration

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](COMPLETE_FEATURES_GUIDE.md)
2. Open an [issue](https://github.com/vishwaksen21/Project_ANU/issues)
3. Contact: vishwaksen21@github.com

---

## 🌟 Star History

If you find ANU helpful, please consider giving it a ⭐!

---

<div align="center">

*ANU - Your caring AI companion* 🌸

[⬆ Back to Top](#-anu---your-caring-ai-companion)

</div>

