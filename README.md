# Legacy Memory Assistant

A hybrid AI-based personal memory preservation system designed for secure, private, and long-term digital legacy management. This project allows users to record, archive, and replay meaningful life events using speech, text, and visuals through a locally managed AI system connected to a visual avatar interface.

## 🎯 Project Purpose

**Legacy Memory Assistant** enables individuals to:

- Securely store daily conversations, reflections, and important life moments
- Organize and annotate memories for future viewing by family members
- Use local AI models to maintain complete control over data privacy
- Provide loved ones with an interactive avatar that can recount stored thoughts and emotions in the user's voice and persona

### Example Use Case
> "When I pass away, my children can access memories via a talking avatar that speaks in my voice and shares stories I've recorded throughout my life."

## 🏗️ System Architecture

The project runs in a **hybrid architecture**, combining:

- **Local Inference (Jetson Orin NX)** for real-time audio/text capture and privacy filtering
- **PC Backend (RTX 5060Ti + Ryzen 7)** for heavy processing, TTS synthesis, backups, and avatar rendering

### Data Flow
1. **Input Capture** → Speech, text, and optional visual input
2. **Local Processing** → AI analysis and emotion detection
3. **Secure Storage** → Encrypted local database with vector indexing
4. **Avatar Interface** → Interactive playback system for authorized users

## ✨ Key Features

### 🎤 Input Capture
- **Real-time Speech Transcription** using Whisper or custom ASR
- **Camera Input** (optional) for emotional state analysis
- **Manual Text Input** for annotations and memory tagging

### 🧠 AI Memory Engine
- **Speech-to-Text Processing** with high accuracy
- **Emotion Classification** from voice and facial expressions
- **Conversation Context Modeling** for coherent memory retrieval
- **Vector Database** (Chroma/FAISS) with timestamped, semantically indexed entries

### 👤 Avatar Interaction Interface
- **2D/3D Avatar Rendering** with emotional expressions
- **Text-to-Speech Engine** with voice cloning capabilities
- **Emotion-based Visual Cues** matching recorded emotional states
- **Interactive Playback System** for authorized heirs

### 🎯 Personalization
- **User-specific Vocabulary** and writing style recognition
- **Memory Tagging System** ("this is for my daughter", "family legacy")
- **Long-term Profile Adaptation** that improves over time
- **Custom Voice Model Training** for authentic avatar speech

### 🔒 Security & Privacy
- **Local-only Storage** by default with SSD encryption
- **Optional Cloud Sync** with locally-held encryption keys
- **Event-based Access Control** (will-triggered or key-based memory access)
- **Full Data Ownership** - users control all recordings
- **Audit Logs** with complete transparency

## 📁 Project Structure

```
/legacy-memory-assistant
│
├── README.md                    # This file
├── LICENSE                      # Creative Commons BY-NC-SA 4.0
├── requirements.txt             # Python dependencies
│
├── /docs                        # Documentation
│   └── architecture_diagram.png # System architecture visual
│
├── /src                         # Core application code
│   ├── memory_manager.py        # Memory storage and retrieval
│   ├── speech_to_text.py        # Audio processing and transcription
│   ├── tts_avatar_interface.py  # Avatar rendering and TTS
│   └── vector_store.py          # Semantic search and indexing
│
└── /samples                     # Example data and demos
    └── demo_conversation.json   # Sample conversation format
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- NVIDIA GPU (recommended for local AI processing)
- Microphone and speakers/headphones
- Optional: Camera for emotion detection

### Installation
```bash
git clone https://github.com/yourusername/legacy-memory-assistant.git
cd legacy-memory-assistant
pip install -r requirements.txt
```

### Basic Usage
```python
from src.memory_manager import MemoryManager
from src.speech_to_text import SpeechProcessor

# Initialize the system
memory = MemoryManager()
speech = SpeechProcessor()

# Record a memory
audio_data = speech.listen()
transcript = speech.transcribe(audio_data)
memory.store_memory(transcript, emotion="happy", tags=["family"])
```

## 💡 Example Interactions

### Recording Memories
```
User: "I want to tell my children about the day they were born..."
System: [Recording] "Memory tagged for 'children' and 'birth stories'"
```

### Avatar Playback (Future Access)
```
Child: "What did Mom say about my birth?"
Avatar: [In mother's voice] "Oh sweetheart, the day you were born was the most beautiful day of my life..."
```

## 🔮 Planned Features

- **Multilingual Support** (German + English + more)
- **Sentiment-aware Voice Rendering** (emotional expressions)
- **Automatic Life Summary Generation**
- **Progressive Web App** for mobile access
- **Biometric Authentication** for secure memory access
- **Advanced Emotion Recognition** from voice patterns

## 📋 Technical Requirements

### Minimum System Requirements
- **CPU**: Multi-core processor (Ryzen 5+ or equivalent)
- **GPU**: NVIDIA RTX 3060 or better (for local AI)
- **RAM**: 16GB+ recommended
- **Storage**: 500GB+ SSD for memory archives
- **OS**: Linux (Ubuntu 20.04+) or Windows 10/11

### Recommended Setup
- **Jetson Orin NX** for edge processing
- **Desktop PC** with RTX 4060+ for avatar rendering
- **High-quality Microphone** for clear audio capture
- **Webcam** (optional) for emotion detection

## 🛡️ Privacy & Ethics

This project is built with **privacy-first principles**:

- **No Cloud Dependency** - everything runs locally by default
- **User Data Control** - memories can be viewed, edited, or deleted anytime
- **Transparent Processing** - all AI operations are explainable
- **Ethical AI Use** - no manipulation or artificial personality creation
- **Family-focused** - designed for genuine legacy preservation

## 📜 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

- ✅ **Share** — copy and redistribute the material
- ✅ **Adapt** — remix, transform, and build upon the material
- ❌ **No Commercial Use** — not for commercial purposes
- 📝 **Attribution Required** — must give appropriate credit
- 🔄 **ShareAlike** — derivatives must use the same license

For commercial licensing inquiries, please contact the project maintainers.

## 🤝 Contributing

We welcome contributions that align with our privacy-first, ethical approach:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines
- Respect user privacy in all implementations
- Include tests for new features
- Follow Python PEP 8 style guidelines
- Update documentation for any API changes

## ⚠️ Important Disclaimer

This software is **not a medical device** and is not intended for:
- Psychological treatment or therapy
- Memory substitution or medical intervention
- Clinical or healthcare applications

**Responsibility**: Users are responsible for the ethical use of recorded memories and should obtain appropriate consent when sharing personal recordings with others.

## 📞 Support & Contact

- **Issues**: Please use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and community interaction
- **Security**: For security concerns, please email [security contact to be added]

---

**Legacy Memory Assistant** - Preserving memories with intention, privacy, and love.

*"Technology should serve humanity's deepest needs - the need to be remembered, to connect across time, and to leave something meaningful for those we love."* 