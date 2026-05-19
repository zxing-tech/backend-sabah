# Customer Support Agent Setup Guide

## Current Status

### ✅ Completed
- Python 3.14 virtual environment created at `venv/`
- Core dependencies installed:
  - `livekit-agents` (v1.4.1) - Core agent framework
  - `python-dotenv` - Environment variable management
  - `Pillow` - Image processing
  - `pinecone` with assistant plugin - Vector database

### ❌ Pending
- LiveKit plugins (google, cartesia, deepgram, silero, hedra, noise-cancellation)
- Frontend setup (pnpm + dependencies)
- Environment variables configuration
- Avatar image path update

## Known Issues

### Plugin Installation Problem
The LiveKit plugins have complex dependency conflicts when installed via pip. The dependency resolver gets stuck trying to find compatible versions.

**Attempted Solutions:**
1. ❌ Installing from `requirements.txt` - Hung on dependency resolution
2. ❌ Installing with extras `pip install 'livekit-agents[plugins]'` - Extras not available
3. ❌ Installing plugins individually - Same dependency conflicts
4. 🔄 Installing LiveKit CLI tool - In progress

## Required API Keys

You need to obtain these API keys and add them to your `.env` file:

```bash
# Pinecone (Vector Database)
PINECONE_API_KEY=xxx
ASSISTANT_NAME=xxx

# LiveKit (Real-time Communication)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=xxx
LIVEKIT_API_SECRET=xxx

# Google Gemini (LLM)
GOOGLE_API_KEY=xxx

# Deepgram (Speech-to-Text)
DEEPGRAM_API_KEY=xxx

# Cartesia (Text-to-Speech)
CARTESIA_API_KEY=xxx

# Hedra (Avatar)
HEDRA_API_KEY=xxx
```

### Where to Get API Keys

- **Pinecone**: https://app.pinecone.io
- **LiveKit**: https://cloud.livekit.io
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **Deepgram**: https://console.deepgram.com
- **Cartesia**: https://cartesia.ai
- **Hedra**: https://www.hedra.com

## Code Changes Needed

### 1. Update Avatar Image Path

In `agent.py` line 61, change the hardcoded path:

```python
# Current (won't work):
avatar_image = Image.open("/Users/jimmybradford/Downloads/rep.png")

# Change to your own image:
avatar_image = Image.open("/Users/capzman/path/to/your/avatar.png")
```

## Recommended Next Steps

### Option 1: Use LiveKit CLI (When Installation Completes)

```bash
# Check available templates
lk app create --help

# Create new project with proper dependencies
lk app create --template voice-assistant-python my-new-agent

# Copy your custom code
cp agent.py my-new-agent/
```

### Option 2: Get Help from LiveKit Community

- **Discord/Slack**: https://livekit.io/join-slack
- **GitHub**: https://github.com/livekit/agents/issues
- Ask for a working `requirements.txt` for agents with plugins

### Option 3: Use Docker

If available, Docker can bypass local dependency issues:

```bash
# Create a Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "agent.py", "dev"]
```

## Frontend Setup (Once Backend Works)

```bash
cd agent-starter-react

# Copy environment template
cp .env.example .env

# Edit .env with your LiveKit credentials

# Install dependencies (pnpm should be installed by now)
pnpm install

# Run development server
pnpm dev
```

Then open http://localhost:3000

## Running the Application

### Backend (Terminal 1):
```bash
cd /Users/capzman/Projects/jxong/livekit/customerSupportAgent-hedra
source venv/bin/activate
python agent.py dev
```

### Frontend (Terminal 2):
```bash
cd agent-starter-react
pnpm dev
```

## Troubleshooting

### If plugins still won't install:
1. Try Python 3.11 instead of 3.14 (more stable with LiveKit)
2. Use a fresh virtual environment
3. Install plugins one at a time and note which one fails
4. Contact LiveKit support with error details

### If the agent crashes:
- Check that all API keys are valid
- Ensure the avatar image path exists
- Check LiveKit server is accessible
- Review logs for specific error messages

## Project Structure

```
customerSupportAgent-hedra/
├── agent.py                    # Your main agent code
├── .env                        # API keys (create this!)
├── .env.example                # Template for API keys
├── requirements.txt            # Python dependencies (needs fixing)
├── venv/                       # Python virtual environment
└── agent-starter-react/        # React frontend
    ├── .env                    # Frontend config (create this!)
    └── package.json            # Node dependencies
```

## Additional Resources

- LiveKit Agents Docs: https://docs.livekit.io/agents/
- Pinecone Assistant: https://docs.pinecone.io/guides/assistant/
- Example Projects: https://github.com/livekit-examples
