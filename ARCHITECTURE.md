# Theraverse - Technical Architecture

## System Overview

Theraverse is a real-time mental health support chatbot with video avatar capabilities, powered by AI services and real-time communication infrastructure.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Next.js 15 React Frontend                           │ │
│  │                      (Port 3000 - Turbopack)                           │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │  Welcome     │  │  Session     │  │  Chat UI     │                │ │
│  │  │  Screen      │  │  View        │  │  Components  │                │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
│  │                                                                        │ │
│  │  ┌────────────────────────────────────────────────────────┐           │ │
│  │  │        LiveKit Components React SDK                     │           │ │
│  │  │  - Room management                                      │           │ │
│  │  │  - Audio/Video tracks                                   │           │ │
│  │  │  - Real-time transcription display                      │           │ │
│  │  │  - Avatar video rendering                               │           │ │
│  │  └────────────────────────────────────────────────────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ WebSocket (WSS)
                                      │ WebRTC (Audio/Video)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LIVEKIT CLOUD INFRASTRUCTURE                         │
│                    (wss://theravest-mjc5x82u.livekit.cloud)                 │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          Room Management                                │ │
│  │  - Participant handling                                                 │ │
│  │  - Track publishing/subscribing                                         │ │
│  │  - Agent dispatch                                                       │ │
│  │  - WebRTC SFU (Selective Forwarding Unit)                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Agent Dispatch
                                      │ (Worker Protocol)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PYTHON BACKEND AGENT                                │
│                        (LiveKit Agents Framework v1.4.1)                     │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         Agent Worker Process                            │ │
│  │                                                                          │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    AgentSession Pipeline                         │  │ │
│  │  │                                                                  │  │ │
│  │  │   ┌──────────┐    ┌──────────┐    ┌──────────┐   ┌──────────┐  │  │ │
│  │  │   │  Silero  │───▶│ Deepgram │───▶│  OpenAI  │──▶│ Cartesia │  │  │ │
│  │  │   │   VAD    │    │   STT    │    │   LLM    │   │   TTS    │  │  │ │
│  │  │   │          │    │ (nova-3) │    │(gpt-4o-  │   │(sonic-2) │  │  │ │
│  │  │   │          │    │          │    │  mini)   │   │          │  │  │ │
│  │  │   └──────────┘    └──────────┘    └──────────┘   └──────────┘  │  │ │
│  │  │        │                │               │              │        │  │ │
│  │  │   Voice Activity    Speech to      AI Response    Text to      │  │ │
│  │  │   Detection         Text           Generation    Speech        │  │ │
│  │  │                                                                  │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                          │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    Hedra Avatar Session                          │  │ │
│  │  │  - Receives audio stream from TTS                                │  │ │
│  │  │  - Generates lip-synced video avatar                             │  │ │
│  │  │  - Publishes video track to LiveKit room                         │  │ │
│  │  │  - Uses: customer_service2_resized.jpg (525x768)                 │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                          │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    Assistant Agent                               │  │ │
│  │  │  - Instructions: Mental health support persona                   │  │ │
│  │  │  - Tools: ask_knowledge_base()                                   │  │ │
│  │  │  - Generates empathetic, supportive responses                    │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
           │                    │                    │                  │
           │                    │                    │                  │
           ▼                    ▼                    ▼                  ▼
    ┌──────────┐        ┌──────────┐        ┌──────────┐      ┌──────────┐
    │ Deepgram │        │  OpenAI  │        │ Cartesia │      │  Hedra   │
    │   API    │        │   API    │        │   API    │      │   API    │
    │          │        │          │        │          │      │          │
    │ STT      │        │ GPT-4o   │        │ TTS      │      │ Avatar   │
    │ Service  │        │ Mini     │        │ Voice    │      │ Video    │
    └──────────┘        └──────────┘        └──────────┘      └──────────┘
                                │
                                │ Function Tool Call
                                │ ask_knowledge_base()
                                ▼
                        ┌──────────────┐
                        │  Pinecone    │
                        │  Assistant   │
                        │  API         │
                        │              │
                        │ Assistant:   │
                        │ "theravest"  │
                        │              │
                        │ Knowledge:   │
                        │ - Crisis     │
                        │ - Anxiety    │
                        │ - Depression │
                        │ - Coping     │
                        │ - Stress     │
                        │ - Therapy    │
                        │ - Self-care  │
                        └──────────────┘
```

---

## Component Details

### 1. Frontend (Next.js 15 React)

**Technology Stack:**
- Framework: Next.js 15.4.5 with Turbopack
- UI: React 19 with TypeScript
- Styling: Tailwind CSS
- Real-time: @livekit/components-react 2.9.14

**Key Components:**
- `welcome.tsx` - Landing page with branding
- `session-view.tsx` - Active session UI with video/chat
- `chat-entry.tsx` - Message display components
- `app-config.ts` - Global configuration

**Features:**
- Real-time audio/video rendering
- Live transcription display
- Chat interface
- Responsive design
- 30-second agent availability timeout

---

### 2. Backend Python Agent

**Technology Stack:**
- Framework: LiveKit Agents v1.4.1
- Language: Python 3.11
- Environment: Virtual environment (venv)

**Core Plugins:**
```python
STT:  deepgram.STT(model="nova-3", language="multi")
LLM:  openai.LLM(model="gpt-4o-mini")
TTS:  cartesia.TTS(model="sonic-2", voice="f786b574...")
VAD:  silero.VAD.load()
Avatar: hedra.AvatarSession(avatar_image=...)
```

**Processing Pipeline:**

1. **Audio Input** → Silero VAD detects speech
2. **Speech-to-Text** → Deepgram transcribes audio
3. **LLM Processing** → OpenAI GPT-4o-mini generates response
   - May call `ask_knowledge_base()` function tool
   - Retrieves info from Pinecone if needed
4. **Text-to-Speech** → Cartesia synthesizes audio
5. **Avatar Generation** → Hedra creates lip-synced video
6. **Output** → Audio + Video published to LiveKit room

**Agent Characteristics:**
- Compassionate mental health support persona
- Empathetic, non-judgmental responses
- Crisis-aware (encourages professional help)
- Knowledge-enhanced via Pinecone

---

### 3. LiveKit Cloud Infrastructure

**Purpose:** Real-time communication layer

**Capabilities:**
- WebRTC Selective Forwarding Unit (SFU)
- Room and participant management
- Agent worker dispatch
- Track publishing/subscribing
- Low-latency media routing

**Region:** Singapore South East

**Protocol:** WebSocket (WSS) + WebRTC

---

### 4. External AI Services

#### Deepgram (Speech-to-Text)
- Model: nova-3
- Multi-language support
- Real-time transcription
- Low latency (~100ms)

#### OpenAI (Language Model)
- Model: gpt-4o-mini
- Mental health support instructions
- Function calling capability
- Conversational responses

#### Cartesia (Text-to-Speech)
- Model: sonic-2
- Voice ID: f786b574-daa5-4673-aa0c-cbe3e8534c02
- Natural, expressive voice
- Low latency synthesis

#### Hedra (Video Avatar)
- Real-time avatar generation
- Lip-sync from audio input
- Avatar image: customer_service2_resized.jpg (525x768)
- Publishes video track to room

#### Pinecone (Knowledge Base)
- Assistant name: theravest
- Vector database for RAG
- 7 mental health documents
- Semantic search enabled

**Knowledge Base Topics:**
1. Crisis resources
2. Understanding anxiety
3. Understanding depression
4. Coping strategies
5. Stress management
6. Seeking professional help
7. Self-care and wellness

---

## Data Flow

### User Question Flow:

```
User speaks
    ↓
Browser captures audio → WebRTC → LiveKit Room
    ↓
Agent receives audio track
    ↓
Silero VAD detects speech
    ↓
Deepgram transcribes → "What helps with anxiety?"
    ↓
OpenAI LLM receives transcription
    ↓
LLM calls ask_knowledge_base("anxiety coping strategies")
    ↓
Pinecone searches knowledge base → Returns relevant info
    ↓
LLM generates response with knowledge context
    ↓
Cartesia synthesizes speech from response
    ↓
Hedra generates avatar video from audio
    ↓
Audio + Video tracks published to LiveKit
    ↓
Browser receives and renders → User sees/hears response
```

---

## Configuration Files

### Environment Variables (.env)
```bash
PINECONE_API_KEY=...
ASSISTANT_NAME=theravest
LIVEKIT_URL=wss://theravest-mjc5x82u.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
OPENAI_API_KEY=...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
HEDRA_API_KEY=...
```

### Frontend Config (app-config.ts)
```typescript
companyName: 'MindfulAI'
pageTitle: 'Mental Health Support'
pageDescription: 'Connect with your compassionate AI mental health companion'
startButtonText: 'Start Conversation'
```

---

## Network Architecture

```
Port 3000 (Frontend)
    ↓ HTTP/HTTPS
Browser ←→ Next.js Dev Server

WSS (Secure WebSocket)
    ↓
Browser ←→ LiveKit Cloud ←→ Python Agent

WebRTC (Peer Connection)
    ↓
Browser ←→ LiveKit Cloud (SFU)

HTTPS REST APIs
    ↓
Python Agent → Deepgram API
Python Agent → OpenAI API
Python Agent → Cartesia API
Python Agent → Hedra API
Python Agent → Pinecone API
```

---

## Scalability Considerations

**Horizontal Scaling:**
- Multiple agent workers can be deployed
- LiveKit handles load balancing
- Each session gets dedicated agent process

**Resource Requirements:**
- Frontend: Node.js server (minimal)
- Backend: Python process per session (~100MB RAM)
- Services: API rate limits apply

**Session Limits:**
- LiveKit room capacity: 100+ participants
- Agent workers: Limited by server resources
- Pinecone: Based on plan limits

---

## Security

**Data Protection:**
- All communication over WSS/HTTPS
- WebRTC encryption
- No conversation data stored locally
- Third-party API keys secured in .env

**Privacy:**
- Real-time processing only
- No conversation persistence (unless configured)
- Compliant with mental health guidelines

---

## Deployment Architecture

```
Development:
    localhost:3000 (Frontend)
    Local Python process (Backend)
    ↓
Production (Recommended):
    Vercel/Netlify (Frontend)
    Cloud VM/Container (Backend Agent)
        - AWS EC2 / Google Cloud Compute
        - Docker container recommended
        - Auto-scaling group
    LiveKit Cloud (Managed service)
```

---

## Future Enhancements

1. **Multi-language Support**
   - Deepgram already supports multi-language
   - Extend knowledge base translations

2. **Session Persistence**
   - Store conversation history
   - User authentication
   - Progress tracking

3. **Analytics**
   - Usage metrics
   - Sentiment analysis
   - Effectiveness tracking

4. **Enhanced Knowledge Base**
   - More mental health topics
   - Regular content updates
   - Personalized recommendations

---

## Technical Debt / Known Issues

1. **Connection Retries:**
   - Occasional "unexpected message type: 258" warnings
   - Auto-reconnection working but could be more robust

2. **Avatar ID Support:**
   - Pre-created Hedra avatar IDs not working
   - Currently using image-based generation only

3. **Frontend Timeout:**
   - Fixed at 30 seconds
   - Could be made configurable

4. **Error Handling:**
   - Some error messages could be more user-friendly
   - Need better fallback strategies

---

## Performance Metrics

**Latency Targets:**
- Speech detection: <100ms (Silero VAD)
- Transcription: ~200-500ms (Deepgram)
- LLM response: 1-3s (OpenAI)
- TTS synthesis: ~500ms (Cartesia)
- Avatar generation: ~500ms (Hedra)
- **Total round-trip: 2-5 seconds**

**Bandwidth:**
- Audio: ~50 kbps
- Video (avatar): ~500 kbps
- Total per session: ~550 kbps

---

Last Updated: February 8, 2026
Version: 1.0
