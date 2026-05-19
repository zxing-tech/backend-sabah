# Product Backlog

## Session & Progress

- [ ] **Mood journal widget** — Daily mood check-in on home screen (tap to log mood without starting a session), shows weekly trend graph
- [ ] **Session streak counter** — "You've completed 5 sessions this month" with streak to encourage consistency
- [ ] **Progress dashboard** — Mood trajectory over time, distortions identified, homework completion rate
- [ ] **Session summary cards** — Quick glance at last 3 sessions with key takeaways (distortion, reframe, homework)

## CBT Tools (self-service, no session needed)

- [ ] **Quick thought record form** — Text-based form to do a thought record anytime (situation → thought → distortion → reframe), saved to Supabase
- [ ] **Breathing exercise** — Guided 4-7-8 or box breathing with animated visual (great for pre-session anxiety)
- [ ] **Grounding exercise** — 5-4-3-2-1 sensory grounding tool
- [ ] **Cognitive distortion flashcards** — Swipeable cards to learn/review the 10+ distortions

## Personalization

- [ ] **Goal setting** — "What do you want to work on?" (anxiety, depression, stress, relationships) — feeds into agent context
- [ ] **Therapist avatar picker** — Choose from different avatar styles/personalities
- [ ] **Session length preference** — 3 min / 5 min / 10 min options

## Safety & Support

- [ ] **Emergency contacts widget** — Always-visible quick access to Befrienders KL (03-7956 8145) / Talian Kasih (15999)
- [ ] **Resource library** — Curated articles, videos, coping strategies from the knowledge base
- [ ] **Crisis self-assessment** — PHQ-9 or GAD-7 screening questionnaire with scoring

## Engagement

- [ ] **Daily affirmation / CBT tip** — Rotating card on the home screen
- [ ] **Homework reminder banner** — Banner showing pending homework from last session with "Mark complete" button
- [ ] **Achievements / badges** — "First thought record", "7-day streak", "Identified 5 distortions"

## Multimodal Emotion Recognition (MER)

- [ ] **Facial expression analysis** — Visual emotion detection via webcam using Hume AI
- [ ] **Voice prosody analysis** — Aural emotion detection from speech patterns using Hume AI
- [ ] **Emotion-aware agent** — Feed emotion scores to CBT agent so it can adapt responses in real-time

---

# Admin Dashboard

## User Overview

- [ ] **User list with search/filter** — Table of all registered users with email, signup date, last session, total sessions, status (active/inactive/flagged)
- [ ] **User detail view** — Click into a user to see their full session history, mood trends, CBT progress, and crisis flags
- [ ] **Active users metrics** — DAU / WAU / MAU charts, retention curves, churn tracking
- [ ] **Cohort analysis** — Group users by signup week, track engagement over time

## Session Analytics

- [ ] **Session volume dashboard** — Total sessions per day/week/month, avg session duration, peak usage hours
- [ ] **Conversation quality metrics** — Avg messages per session, tool usage rates (log_mood, log_cbt_insight, set_homework), knowledge base queries
- [ ] **Session transcript viewer** — Read-only view of any session's full transcript (with appropriate access controls)
- [ ] **Drop-off analysis** — Where users disconnect early, sessions with no user speech, bounce rate

## CBT Effectiveness

- [ ] **Mood improvement tracker** — Aggregate mood change across all users (start vs end of session), show % of sessions with positive mood shift
- [ ] **Top cognitive distortions** — Bar chart of most common distortions identified across all users (e.g., catastrophizing 34%, all-or-nothing 22%)
- [ ] **Homework completion rate** — % of users who received homework and showed follow-through in next session
- [ ] **Thought record stats** — Total thought records completed, avg reframe quality, most common situations

## Crisis & Safety

- [ ] **Crisis alert log** — Real-time feed of all crisis flags with timestamp, user (anonymized), trigger reason, transcript snippet
- [ ] **Crisis response audit** — Did the agent provide contacts? Did the user stay on the call? Follow-up actions needed?
- [ ] **Flagged user list** — Users who triggered crisis detection, with frequency and recency indicators
- [ ] **Escalation workflow** — Ability to assign a flagged user to a human counselor or send a follow-up check-in

## Agent Performance

- [ ] **Response latency** — Avg time from user speech end to agent speech start (STT + LLM + TTS pipeline)
- [ ] **Avatar uptime** — % of sessions where HeyGen avatar loaded successfully vs audio-only fallback
- [ ] **TTS/STT error rates** — Track Cartesia 402s, Deepgram failures, HeyGen credit exhaustion
- [ ] **Tool call success rate** — How often each function tool (log_mood, flag_crisis, etc.) is called vs errors
- [ ] **API cost tracker** — Estimated daily/monthly spend across OpenAI, Cartesia, Deepgram, HeyGen, Pinecone

## Content & Knowledge Base

- [ ] **Knowledge base manager** — Upload, edit, delete documents in Pinecone from the admin UI
- [ ] **RAG query log** — What users are asking the knowledge base, which docs are retrieved, relevance scores
- [ ] **Prompt/instructions editor** — Edit the agent's system prompt (BASE_INSTRUCTIONS) from the admin without redeploying

## Platform Operations

- [ ] **System health dashboard** — Fly.io machine status, LiveKit room count, active connections, memory/CPU
- [ ] **Feature flags** — Toggle features on/off (avatar, crisis detection, CBT tools, session history)
- [ ] **User management** — Invite users, reset passwords, deactivate accounts, manage roles (admin/user)
- [ ] **Audit log** — Track admin actions (who changed what, when)

---

## Admin Dashboard Priority (high impact, low effort)

1. **Crisis alert log** — critical for safety compliance, data already in Supabase
2. **Session volume dashboard** — basic analytics from `therapy_sessions` table
3. **Top cognitive distortions** — aggregatable from `cbt_data.insights`
4. **User list** — simple query on `auth.users` + `therapy_sessions`

---

# User Screen Priority (high impact, low effort)

1. **Homework reminder banner** — data already in `cbt_data.homework`
2. **Emergency contacts widget** — static component, high safety value
3. **Mood trend chart** — data already in `cbt_data.mood_ratings`, just needs a chart
