# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Theraverse is a real-time mental health support AI chatbot with video avatar capabilities. It has a three-tier architecture: a Next.js/React frontend, LiveKit Cloud for real-time communication (WebRTC/WebSocket), and a Python backend agent that orchestrates an AI processing pipeline.

**Current state:** The `migration-react-to-next` branch is migrating from the `agent-starter-react/` template (Next.js 15, fully implemented) to `theraverse-next/` (Next.js 16, fresh scaffold). The reference implementation lives in `agent-starter-react/`.

## Repository Structure

```
theraverse/
├── agent.py                    # Python backend agent (main logic)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend container (Python 3.11)
├── fly.toml                    # Fly.io config for backend agent
├── knowledge_base/             # Mental health docs uploaded to Pinecone
├── test_init.py                # Component initialization tests
├── test_livekit_connection.py  # LiveKit connection tests
├── agent-starter-react/        # Reference frontend (fully implemented)
│   ├── components/             # React components (LiveKit, UI, session)
│   ├── hooks/                  # Custom hooks (chat, connection, debug)
│   ├── app/api/                # API routes (connection-details, auth)
│   ├── middleware.ts           # HTTP Basic auth middleware
│   ├── app-config.ts           # App branding/feature config
│   └── lib/                    # Types and utilities
└── theraverse-next/            # Migration target (Next.js 16 scaffold)
```

## Development Commands

### Backend (Python agent)
```bash
source venv/bin/activate
python agent.py dev            # Local development mode
python agent.py start          # Production mode
python test_init.py            # Test component initialization
python test_livekit_connection.py  # Test LiveKit connectivity
```

### Frontend (agent-starter-react)
```bash
cd agent-starter-react
pnpm install                   # Install dependencies
pnpm dev                       # Dev server with Turbopack (port 3000)
pnpm build                     # Production build
pnpm lint                      # ESLint
pnpm format                    # Prettier format
pnpm format:check              # Check formatting
```

### Frontend (theraverse-next)
```bash
cd theraverse-next
pnpm install
pnpm dev                       # Dev server (port 3000)
pnpm build
pnpm lint
```

### Deployment
- Push to `main` triggers GitHub Actions → Fly.io deploy
- Backend: `customersupportagent-hedra` (Singapore region)
- Frontend: `theraverse-agent-web` (Singapore region)

## Architecture

### Agent Processing Pipeline
```
User Speech → [Silero VAD] → [Deepgram STT nova-3] → [OpenAI gpt-4o-mini]
    → (optional) [Pinecone RAG via ask_knowledge_base tool]
    → [Cartesia TTS sonic-2] → [HeyGen LiveAvatar] → User Browser
```

The backend agent (`agent.py`) uses LiveKit Agents v1.4.1. It connects outbound to LiveKit Cloud (no inbound HTTP needed). The frontend generates LiveKit access tokens via the `/api/connection-details` route and connects to rooms over WebRTC.

### Key Integration Points
- **LiveKit Components React SDK** (`@livekit/components-react`) powers the frontend real-time UI
- **Pinecone Assistant** provides RAG over the `knowledge_base/` documents via the `ask_knowledge_base` function tool
- **HeyGen LiveAvatar** generates video avatar from TTS audio (falls back to audio-only on failure)
- Frontend auth uses HTTP Basic auth via Next.js middleware (`AUTH_USERNAME`/`AUTH_PASSWORD` env vars)

## Environment Variables

### Backend (.env at root)
`PINECONE_API_KEY`, `ASSISTANT_NAME`, `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `CARTESIA_API_KEY`, `HEDRA_API_KEY`

### Frontend (.env in agent-starter-react/)
`LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL`, `AUTH_USERNAME`, `AUTH_PASSWORD`

## Tech Stack

- **Frontend:** Next.js 15 (reference) / 16 (migration target), React 19, Tailwind CSS v4, Radix UI, pnpm
- **Backend:** Python 3.11, LiveKit Agents, OpenAI, Deepgram, Cartesia, Silero, HeyGen LiveAvatar, Pinecone
- **Deployment:** Fly.io (Docker), GitHub Actions CI/CD
- **Package manager:** pnpm (frontend), pip with venv (backend)
