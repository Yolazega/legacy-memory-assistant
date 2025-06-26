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

---

## 🗣️ Live Proxy Avatar Feature (Personal Use)

**Legacy Memory Assistant** includes a powerful **Live Proxy Avatar** mode that allows your AI assistant to temporarily respond on behalf of you when you're unavailable.

### How It Works

> The system allows a "Live Proxy Avatar" mode, where the AI assistant temporarily responds on behalf of the user when they are unavailable.
>
> For example, a family member may ask: "Where did Mom store the vacation documents?" — and the assistant responds using the user's stored contextual memory and speech style.
>
> This mode can be scheduled (e.g. between 10 PM and 7 AM) or triggered manually.

### Key Features

- **Contextual Memory Access**: The avatar draws from your stored conversations, documents, and personal knowledge base
- **Speech Style Mimicry**: Responds using your documented communication patterns and preferences
- **Scheduled Availability**: Configure automatic proxy mode during specific hours (sleep, work, travel)
- **Manual Activation**: Instantly enable proxy mode when needed
- **Truthful Responses Only**: The avatar will not fabricate answers, but only respond using available vectorized knowledge and documented conversations
- **Confidence Indicators**: Clearly indicates when information is uncertain or unavailable

### Example Interactions

```
Family Member: "Where did Mom store the vacation documents?"
Proxy Avatar: "Based on our conversation from last week, I stored the vacation documents in the filing cabinet, second drawer, under 'Travel 2024'."

Family Member: "What time does Dad usually wake up?"
Proxy Avatar: "From our daily routines, I typically wake up around 6:30 AM on weekdays and 7:30 AM on weekends."

Family Member: "Did Mom mention anything about the doctor's appointment?"
Proxy Avatar: "I don't have any recorded conversations about a doctor's appointment. You might want to check directly when I'm available."
```

### Privacy & Safety

- **Limited Scope**: Only accesses information you've explicitly shared with the system
- **No Fabrication**: Never invents information that doesn't exist in your memory bank
- **Access Controls**: Define who can interact with your proxy avatar
- **Audit Trail**: Complete log of all proxy interactions for your review
- **Immediate Override**: You can instantly disable proxy mode and take over any conversation

---

## 🏢 Enterprise Use Case: Internal Company Memory Mode

The same architecture powering **Legacy Memory Assistant** can be adapted for **organizational use**, creating a shared conversational memory system for teams and companies.

### Team Knowledge Proxy

> Teams can create a shared conversational memory system that logs daily interactions, project decisions, or workflows. This enables team members to later query the assistant about:
>
> - "What did we decide about the Q4 budget in the last meeting?"  
> - "Where is the internal documentation for onboarding new hires?"
>
> The assistant can act as a "knowledge proxy" when colleagues are on leave or unavailable, reducing response time and email overload.

### Enterprise Architecture

#### Deployment Options
- **Internal Server Hosting**: Complete on-premises deployment for maximum security
- **Encrypted Cloud Storage**: Secure cloud deployment with enterprise-grade encryption
- **Hybrid Configuration**: Critical data on-premises, with cloud processing for scalability

#### Security & Compliance
- **Modular Permission Structures**: Role-based access control for different team members
- **Data Access Roles**: Fine-grained permissions for sensitive information
- **Live Update Syncing**: Real-time synchronization across team members
- **Compliance Ready**: Built-in support for SOC 2, GDPR, HIPAA, and other standards

### Integration Capabilities

The enterprise version seamlessly integrates with existing workplace tools:

- **Slack Integration**: Direct bot access within Slack channels and DMs
- **Microsoft Teams**: Native Teams app with full conversation context
- **Internal Dashboards**: Custom web interfaces for knowledge management
- **Email Integration**: Smart email response suggestions based on team knowledge
- **Calendar Systems**: Meeting context and decision tracking
- **Project Management**: Integration with Jira, Asana, Monday.com, and similar tools

### Use Cases

#### Knowledge Management
```
Team Member: "What was the decision about the new server architecture?"
Company AI: "In the infrastructure meeting on March 15th, the team decided to go with AWS EKS for container orchestration, with a budget of $50K for the first year."
```

#### Onboarding & Training
```
New Employee: "How do I set up the development environment?"
Company AI: "Based on our engineering team's documentation, here's the setup process: [provides step-by-step guide from team knowledge base]"
```

#### Cross-Department Communication
```
Marketing Team: "What's the latest update on the product launch timeline?"
Company AI: "According to the product team's last update, the launch is scheduled for Q2 2024, with beta testing starting next month."
```

### Enterprise Benefits

- **Reduced Email Overload**: Instant access to team knowledge without constant messaging
- **Improved Continuity**: Seamless operation when team members are on leave or unavailable
- **Faster Decision Making**: Quick access to previous decisions and context
- **Enhanced Onboarding**: New employees can quickly understand team processes and decisions
- **Knowledge Preservation**: Institutional knowledge captured and searchable
- **Cross-Team Collaboration**: Breaking down silos with shared accessible knowledge

### Implementation Considerations

- **Privacy Policies**: Respects company privacy requirements and data governance
- **Data Retention**: Configurable retention periods for different types of information
- **Access Auditing**: Complete audit trails for compliance and security
- **Gradual Rollout**: Pilot programs with specific teams before company-wide deployment
- **Training Programs**: Comprehensive training for effective system adoption

---

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
git clone https://github.com/Yolazega/legacy-memory-assistant.git
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
