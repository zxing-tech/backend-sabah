# User Stories

---

# USER SCREEN

---

## US-001: Mood Journal Widget

**Priority:** High
**Effort:** Medium
**Category:** Session & Progress

### Description
As a user, I want to log my mood from the home screen without starting a full session, so I can track how I feel daily and see patterns over time.

### Acceptance Criteria
- [ ] Home screen shows a "How are you feeling?" widget
- [ ] User can select an emotion (happy, sad, anxious, angry, calm, stressed) and rate intensity (1-10)
- [ ] Mood entry is saved to Supabase with timestamp and user ID
- [ ] Widget displays a 7-day mood trend as a simple line/bar chart
- [ ] Tapping the chart navigates to a full mood history view

### Technical Notes
- New Supabase table: `mood_journal` (id, user_id, mood_type, intensity, created_at)
- API route: POST/GET `/api/mood-journal`
- Chart library: recharts or chart.js
- Component: `components/mood-journal-widget.tsx`

---

## US-002: Session Streak Counter

**Priority:** Medium
**Effort:** Low
**Category:** Session & Progress

### Description
As a user, I want to see how many sessions I've completed this month and my current streak, so I feel motivated to continue.

### Acceptance Criteria
- [ ] Home screen shows "X sessions this month" with a streak count
- [ ] Streak counts consecutive weeks with at least 1 session
- [ ] Visual indicator (flame icon or similar) when streak is active
- [ ] Streak resets if user goes 7+ days without a session

### Technical Notes
- Query `therapy_sessions` grouped by month/week for current user
- No new tables needed — derive from existing data
- Component: `components/streak-counter.tsx`

---

## US-003: Progress Dashboard

**Priority:** High
**Effort:** High
**Category:** Session & Progress

### Description
As a user, I want a dashboard showing my therapy progress over time, so I can see that CBT is working.

### Acceptance Criteria
- [ ] Mood trajectory chart: plot start-of-session vs end-of-session mood over all sessions
- [ ] Distortion frequency breakdown: which distortions have been identified most
- [ ] Homework completion rate: % of sessions where homework was assigned and acknowledged next session
- [ ] Total sessions, total time spent, average session duration
- [ ] Date range filter (last 7 days, 30 days, all time)

### Technical Notes
- Aggregate data from `therapy_sessions.cbt_data` JSONB column
- API route: GET `/api/progress` with date range params
- Charts: recharts library
- Page: `/dashboard` or `/progress`

---

## US-004: Session Summary Cards

**Priority:** Medium
**Effort:** Low
**Category:** Session & Progress

### Description
As a user, I want to see quick summary cards of my recent sessions on the home screen, so I can recall what we discussed.

### Acceptance Criteria
- [ ] Home screen shows cards for last 3 sessions
- [ ] Each card shows: date, duration, mood change (if available), key distortion identified, homework assigned
- [ ] Tapping a card navigates to the full session detail view
- [ ] Empty state: "No sessions yet — start your first conversation"

### Technical Notes
- Query `therapy_sessions` with `cbt_data` for current user, limit 3
- Reuse existing session-list component patterns
- Component: `components/session-summary-cards.tsx`

---

## US-005: Quick Thought Record Form

**Priority:** High
**Effort:** Medium
**Category:** CBT Tools

### Description
As a user, I want to complete a thought record on my own without starting a voice session, so I can practice CBT techniques anytime.

### Acceptance Criteria
- [ ] Accessible from home screen via "Quick Thought Record" button
- [ ] Multi-step form: Situation → Automatic Thought → Emotion (select + rate 0-10) → Evidence For → Evidence Against → Balanced Thought → New Emotion Rating
- [ ] Saved to Supabase with timestamp
- [ ] View history of completed thought records
- [ ] Optional: share thought record in next voice session for discussion

### Technical Notes
- New Supabase table: `thought_records` (id, user_id, situation, automatic_thought, emotion_type, emotion_intensity, evidence_for, evidence_against, balanced_thought, new_emotion_intensity, created_at)
- API routes: POST/GET `/api/thought-records`
- Page: `/tools/thought-record`
- Multi-step form component with validation

---

## US-006: Breathing Exercise

**Priority:** Medium
**Effort:** Low
**Category:** CBT Tools

### Description
As a user, I want a guided breathing exercise, so I can calm down before or after a session.

### Acceptance Criteria
- [ ] Accessible from home screen via "Breathing" button
- [ ] Animated circle that expands (inhale), holds, and contracts (exhale)
- [ ] Support 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s)
- [ ] Support box breathing (4-4-4-4)
- [ ] Duration selector: 1 min, 3 min, 5 min
- [ ] Calming background color transitions
- [ ] Optional: haptic feedback on mobile

### Technical Notes
- Pure frontend — no backend needed
- CSS animations or framer-motion
- Page: `/tools/breathing`

---

## US-007: Grounding Exercise (5-4-3-2-1)

**Priority:** Medium
**Effort:** Low
**Category:** CBT Tools

### Description
As a user, I want a guided 5-4-3-2-1 sensory grounding exercise, so I can manage acute anxiety or panic.

### Acceptance Criteria
- [ ] Step-by-step guided flow: 5 things you see → 4 things you touch → 3 things you hear → 2 things you smell → 1 thing you taste
- [ ] Each step has a text input or "Next" button
- [ ] Calming visual design with progress indicator
- [ ] Completion screen with encouraging message
- [ ] Optional: save as a journal entry

### Technical Notes
- Pure frontend — no backend needed
- Multi-step wizard component
- Page: `/tools/grounding`

---

## US-008: Cognitive Distortion Flashcards

**Priority:** Low
**Effort:** Low
**Category:** CBT Tools

### Description
As a user, I want to browse flashcards of cognitive distortions with examples, so I can learn to recognize them in my own thinking.

### Acceptance Criteria
- [ ] Swipeable card deck with all 12 distortions
- [ ] Front: distortion name + brief description
- [ ] Back: example thought + how to challenge it
- [ ] Shuffle option
- [ ] "I spotted this one today" button → logs to mood journal or thought record
- [ ] Progress indicator (X of 12)

### Technical Notes
- Static data — no backend needed
- Content from `knowledge_base/08_cbt_cognitive_distortions.txt`
- Component: `components/distortion-flashcards.tsx`

---

## US-009: Goal Setting

**Priority:** Medium
**Effort:** Medium
**Category:** Personalization

### Description
As a user, I want to set my therapy goals, so the AI agent can tailor sessions to what I'm working on.

### Acceptance Criteria
- [ ] Onboarding or settings screen: "What would you like to work on?"
- [ ] Multi-select from: Anxiety, Depression, Stress, Self-esteem, Relationships, Work/School, Sleep, Anger, Grief, Other
- [ ] Optional free-text for specific goals
- [ ] Goals stored in Supabase user profile
- [ ] Goals included in agent system prompt context
- [ ] Editable from settings at any time

### Technical Notes
- New Supabase table or column: `user_profiles.goals` (JSONB)
- Pass goals in LiveKit participant metadata alongside session context
- Agent instructions updated to reference user goals

---

## US-010: Therapist Avatar Picker

**Priority:** Low
**Effort:** Medium
**Category:** Personalization

### Description
As a user, I want to choose my therapist avatar's appearance, so I feel more comfortable during sessions.

### Acceptance Criteria
- [ ] Settings screen with avatar options (different HeyGen avatar IDs)
- [ ] Preview image/video for each avatar
- [ ] Selection saved to user profile in Supabase
- [ ] Agent uses selected avatar ID when starting LiveAvatar session
- [ ] Default avatar if none selected

### Technical Notes
- Store selected avatar_id in user profile
- Pass avatar_id in participant metadata
- Agent reads metadata and passes to `AvatarSession(avatar_id=...)`
- Requires multiple HeyGen avatars set up in their dashboard

---

## US-011: Session Length Preference

**Priority:** Low
**Effort:** Low
**Category:** Personalization

### Description
As a user, I want to choose my session length, so I can fit therapy into my schedule.

### Acceptance Criteria
- [ ] Before starting a session, choose: 3 min, 5 min, 10 min
- [ ] Timer in session view reflects chosen duration
- [ ] Agent adjusts pacing based on time available (shorter = more focused, longer = more exploratory)
- [ ] Preference saved for next session (can change anytime)

### Technical Notes
- Store preference in Supabase user profile or localStorage
- Pass duration to agent via participant metadata
- Update session-view.tsx `MAX_SESSION_SECONDS` from selected duration
- Agent instructions include time awareness

---

## US-012: Emergency Contacts Widget

**Priority:** High
**Effort:** Low
**Category:** Safety & Support

### Description
As a user, I want quick access to emergency contacts from the home screen, so I can get help without starting a session.

### Acceptance Criteria
- [ ] Persistent card/banner on home screen with emergency numbers
- [ ] Befrienders KL: 03-7956 8145 (clickable tel: link)
- [ ] Talian Kasih: 15999 (clickable tel: link)
- [ ] Emergency: 999 (clickable tel: link)
- [ ] Subtle but always visible — not dismissible
- [ ] Mobile: tap to call directly

### Technical Notes
- Static component — no backend needed
- Component: `components/emergency-contacts.tsx`
- Add to home/welcome screen layout

---

## US-013: Resource Library

**Priority:** Low
**Effort:** Medium
**Category:** Safety & Support

### Description
As a user, I want to browse mental health resources and coping strategies, so I can learn and help myself between sessions.

### Acceptance Criteria
- [ ] Page with categorized resources: Anxiety, Depression, Stress, Coping Strategies, Self-Care, Crisis
- [ ] Each resource: title, short description, full content (expandable)
- [ ] Content sourced from existing knowledge_base/ documents
- [ ] Search/filter functionality
- [ ] "Discuss in session" button → saves topic for next session

### Technical Notes
- Content from `knowledge_base/*.txt` files
- Can be static at first, later backed by Pinecone search
- Page: `/resources`

---

## US-014: Crisis Self-Assessment (PHQ-9 / GAD-7)

**Priority:** Medium
**Effort:** Medium
**Category:** Safety & Support

### Description
As a user, I want to take standardized mental health screening questionnaires, so I can understand the severity of my symptoms.

### Acceptance Criteria
- [ ] PHQ-9 (depression) and GAD-7 (anxiety) questionnaires available
- [ ] Standard questions with 0-3 Likert scale responses
- [ ] Auto-scored with severity interpretation (minimal, mild, moderate, moderately severe, severe)
- [ ] Results saved to Supabase with timestamp
- [ ] Track scores over time with a trend chart
- [ ] If score indicates severe: show emergency contacts and recommend professional help
- [ ] Disclaimer: "This is a screening tool, not a diagnosis"

### Technical Notes
- New Supabase table: `assessments` (id, user_id, type, responses JSONB, score, created_at)
- API routes: POST/GET `/api/assessments`
- Page: `/tools/assessment`

---

## US-015: Daily Affirmation / CBT Tip

**Priority:** Low
**Effort:** Low
**Category:** Engagement

### Description
As a user, I want to see a daily CBT tip or affirmation on the home screen, so I'm encouraged to practice CBT thinking throughout the day.

### Acceptance Criteria
- [ ] Rotating card on home screen — changes daily
- [ ] Mix of: CBT tips, affirmations, Socratic questions to reflect on, distortion awareness prompts
- [ ] Example: "Today's thought challenge: When you notice a 'should' statement, ask yourself — who made that rule?"
- [ ] Tap to expand with more detail
- [ ] 30+ entries to avoid repetition within a month

### Technical Notes
- Static JSON/array of tips — no backend needed
- Rotate based on day of year (`new Date().getDate() % tips.length`)
- Component: `components/daily-tip.tsx`

---

## US-016: Homework Reminder Banner

**Priority:** High
**Effort:** Low
**Category:** Engagement

### Description
As a user, I want to see my pending homework from the last session on the home screen, so I remember to practice between sessions.

### Acceptance Criteria
- [ ] Banner on home screen showing homework text from last session
- [ ] "Mark as completed" button → saves completion status
- [ ] Shows days since homework was assigned
- [ ] Disappears after completion or after next session
- [ ] If no homework pending: banner not shown

### Technical Notes
- Query latest `therapy_sessions.cbt_data.homework` for current user
- API route: GET `/api/sessions/homework` + PATCH to mark complete
- Add `homework_completed` boolean to `therapy_sessions` or track in separate table
- Component: `components/homework-banner.tsx`

---

## US-017: Achievements / Badges

**Priority:** Low
**Effort:** Medium
**Category:** Engagement

### Description
As a user, I want to earn badges for therapy milestones, so I feel a sense of progress and accomplishment.

### Acceptance Criteria
- [ ] Badge definitions: First Session, First Thought Record, 3-Day Streak, 7-Day Streak, 5 Distortions Identified, 10 Sessions, Mood Improved, Homework Completed
- [ ] Badges page showing earned (colored) and locked (greyed) badges
- [ ] Toast notification when a new badge is earned
- [ ] Badge count shown on home screen
- [ ] Optional: share badges (screenshot-friendly layout)

### Technical Notes
- New Supabase table: `user_badges` (id, user_id, badge_type, earned_at)
- Badge calculation logic: run on session save or via background job
- API route: GET `/api/badges`
- Page: `/achievements`

---

## US-018: Facial Expression Analysis (Hume AI)

**Priority:** Medium
**Effort:** High
**Category:** Multimodal Emotion Recognition

### Description
As a user, I want the system to detect my facial expressions during a session, so the AI therapist can better understand my emotional state.

### Acceptance Criteria
- [ ] Webcam feed analyzed in real-time during sessions
- [ ] Emotion scores (happy, sad, angry, anxious, surprised, neutral) detected
- [ ] Scores sent to agent via data channel to inform responses
- [ ] Optional: subtle emotion indicator shown to user in session UI
- [ ] Privacy: user must consent, no video stored, analysis is real-time only
- [ ] Graceful degradation if webcam not available

### Technical Notes
- Integrate Hume AI JavaScript SDK on frontend
- Process webcam frames → emotion scores
- Send scores to agent via LiveKit data channel (topic: `emotion_visual`)
- Agent reads scores and adjusts tone/approach
- Requires Hume AI API key and account

---

## US-019: Voice Prosody Analysis (Hume AI)

**Priority:** Medium
**Effort:** High
**Category:** Multimodal Emotion Recognition

### Description
As a user, I want the system to analyze my voice tone during a session, so the AI therapist can detect emotions I may not explicitly state.

### Acceptance Criteria
- [ ] Microphone audio analyzed for prosody features (pitch, speed, energy, tone)
- [ ] Emotion classification from voice: calm, stressed, sad, angry, anxious, happy
- [ ] Results sent to agent in real-time to inform responses
- [ ] Agent can reference detected emotions: "I notice your voice sounds a bit tense — would you like to explore that?"
- [ ] Privacy: no audio stored beyond the session, analysis is real-time only

### Technical Notes
- Integrate Hume AI Prosody API or Expression Measurement API
- Process audio chunks from LiveKit audio track
- Send emotion scores via data channel (topic: `emotion_prosody`)
- Agent instructions updated to reference emotion data when available

---

## US-020: Emotion-Aware Agent Responses

**Priority:** Medium
**Effort:** Medium
**Category:** Multimodal Emotion Recognition

### Description
As a user, I want the AI therapist to adapt its responses based on my detected emotions, so the conversation feels more attuned and empathetic.

### Acceptance Criteria
- [ ] Agent receives visual + prosody emotion scores during conversation
- [ ] Agent adjusts behavior: if high anxiety detected → slower pace, more validation; if sadness detected → more warmth and checking in
- [ ] Agent can gently name observed emotions: "It seems like this topic brings up some strong feelings"
- [ ] Agent does NOT over-rely on detection — always confirms with the user
- [ ] If emotion detection conflicts with user's stated feelings, trust the user

### Technical Notes
- Agent reads emotion data from data channel messages stored in memory
- System prompt updated with emotion-awareness guidelines
- Emotion data included in `cbt_data` for session history
- Depends on US-018 and US-019

---

# ADMIN DASHBOARD

---

## AD-001: User List with Search/Filter

**Priority:** High
**Effort:** Medium
**Category:** User Overview

### Description
As an admin, I want to view all registered users with key metrics, so I can monitor platform usage and identify users who need attention.

### Acceptance Criteria
- [ ] Table view: email, signup date, last session date, total sessions, total time, status
- [ ] Search by email or name
- [ ] Filter by: active (session in last 7 days), inactive (no session in 30+ days), flagged (crisis detected)
- [ ] Sort by any column
- [ ] Pagination (20 per page)
- [ ] Click row → navigate to user detail view (AD-002)

### Technical Notes
- Admin-only page with role check
- Query `auth.users` joined with `therapy_sessions` aggregates
- Admin API routes with RLS bypass (service role key)
- Page: `/admin/users`

---

## AD-002: User Detail View

**Priority:** High
**Effort:** Medium
**Category:** User Overview

### Description
As an admin, I want to view a specific user's full profile and session history, so I can understand their therapy journey and provide support if needed.

### Acceptance Criteria
- [ ] User info: email, signup date, last active, total sessions
- [ ] Session list with dates, durations, mood changes
- [ ] CBT progress: distortions identified, thought records completed, homework history
- [ ] Mood trend chart for this user
- [ ] Crisis flag history with timestamps and reasons
- [ ] Ability to add admin notes about the user
- [ ] Link to full session transcript (AD-007)

### Technical Notes
- Query all `therapy_sessions` + `session_messages` + `cbt_data` for user
- Admin API route: GET `/api/admin/users/[id]`
- Page: `/admin/users/[id]`

---

## AD-003: Active Users Metrics (DAU/WAU/MAU)

**Priority:** Medium
**Effort:** Medium
**Category:** User Overview

### Description
As an admin, I want to see daily, weekly, and monthly active user counts, so I can track platform growth and engagement.

### Acceptance Criteria
- [ ] Line chart showing DAU, WAU, MAU over time (last 90 days)
- [ ] Current values displayed as headline numbers
- [ ] Retention rate: % of users who return within 7 days of first session
- [ ] New vs returning users breakdown
- [ ] Comparison to previous period (e.g., +15% vs last month)

### Technical Notes
- Aggregate `therapy_sessions` by distinct `user_id` per day/week/month
- Cache results for performance (refresh hourly)
- Chart library: recharts
- Page: `/admin/dashboard`

---

## AD-004: Cohort Analysis

**Priority:** Low
**Effort:** High
**Category:** User Overview

### Description
As an admin, I want to see cohort retention analysis, so I can understand how well we retain users over time.

### Acceptance Criteria
- [ ] Cohort table: rows = signup week, columns = weeks since signup
- [ ] Cell values = % of cohort still active (had a session)
- [ ] Color-coded heatmap (green = high retention, red = low)
- [ ] Filterable by date range
- [ ] Export to CSV

### Technical Notes
- Complex aggregate query on `auth.users` signup date + `therapy_sessions`
- Consider pre-computing via a scheduled job or database view
- Page: `/admin/analytics/cohorts`

---

## AD-005: Session Volume Dashboard

**Priority:** High
**Effort:** Low
**Category:** Session Analytics

### Description
As an admin, I want to see session volume over time, so I can understand usage patterns and plan capacity.

### Acceptance Criteria
- [ ] Bar chart: sessions per day (last 30 days)
- [ ] Line chart: sessions per week (last 12 weeks)
- [ ] Headline metrics: total sessions today, this week, this month
- [ ] Average session duration trend
- [ ] Peak usage hours heatmap (hour of day vs day of week)

### Technical Notes
- Aggregate `therapy_sessions` by date/hour
- Simple COUNT/AVG queries with GROUP BY
- Page: `/admin/dashboard` or `/admin/analytics/sessions`

---

## AD-006: Conversation Quality Metrics

**Priority:** Medium
**Effort:** Medium
**Category:** Session Analytics

### Description
As an admin, I want to understand the quality of AI therapy conversations, so I can identify areas for improvement.

### Acceptance Criteria
- [ ] Avg messages per session (trend over time)
- [ ] Tool usage rates: % of sessions using log_mood, log_cbt_insight, set_homework, ask_knowledge_base, flag_crisis
- [ ] Avg mood improvement per session (start mood vs end mood)
- [ ] % of sessions with at least 1 thought record completed
- [ ] % of sessions where homework was assigned
- [ ] Sessions with no user engagement (user didn't speak after greeting)

### Technical Notes
- Aggregate from `session_messages` (message counts) and `therapy_sessions.cbt_data` (tool usage)
- API route: GET `/api/admin/analytics/quality`
- Page: `/admin/analytics/quality`

---

## AD-007: Session Transcript Viewer

**Priority:** Medium
**Effort:** Low
**Category:** Session Analytics

### Description
As an admin, I want to read the full transcript of any session, so I can audit conversation quality and review crisis situations.

### Acceptance Criteria
- [ ] Read-only view of session messages in chat bubble format
- [ ] Session metadata header: user (anonymized option), date, duration, mood change
- [ ] CBT data sidebar: distortions identified, thought records, homework
- [ ] Crisis flag indicator if crisis was detected
- [ ] Search within transcript
- [ ] Access logged for audit trail

### Technical Notes
- Reuse `SessionDetail` component with admin wrapper
- Admin API route: GET `/api/admin/sessions/[id]`
- Add audit log entry when admin views a transcript
- Page: `/admin/sessions/[id]`

---

## AD-008: Drop-off Analysis

**Priority:** Low
**Effort:** Medium
**Category:** Session Analytics

### Description
As an admin, I want to understand where users drop off, so I can improve the user experience and reduce churn.

### Acceptance Criteria
- [ ] Funnel: Login → Start Session → Agent Connected → 1+ Minutes → Session Complete
- [ ] Drop-off rate at each stage
- [ ] Sessions ended before agent spoke (connection issues)
- [ ] Sessions with < 1 minute duration (immediate bounces)
- [ ] Avg time before disconnect for short sessions
- [ ] Filter by date range

### Technical Notes
- Analyze `therapy_sessions` duration_seconds distribution
- Correlate with `session_messages` count (0 messages = no engagement)
- Page: `/admin/analytics/dropoff`

---

## AD-009: Mood Improvement Tracker (Aggregate)

**Priority:** High
**Effort:** Low
**Category:** CBT Effectiveness

### Description
As an admin, I want to see aggregate mood improvement across all users, so I can measure whether CBT therapy is effective.

### Acceptance Criteria
- [ ] Overall stat: "X% of sessions show mood improvement"
- [ ] Average mood change: start intensity vs end intensity
- [ ] Chart: distribution of mood changes (-10 to +10 scale)
- [ ] Breakdown by emotion type (anxiety improvement, sadness improvement, etc.)
- [ ] Trend over time: is effectiveness improving month over month?

### Technical Notes
- Aggregate `cbt_data.mood_ratings` from all `therapy_sessions`
- Compare first and last mood_rating per session
- API route: GET `/api/admin/analytics/mood`
- Page: `/admin/analytics/effectiveness`

---

## AD-010: Top Cognitive Distortions Chart

**Priority:** High
**Effort:** Low
**Category:** CBT Effectiveness

### Description
As an admin, I want to see which cognitive distortions are most common across all users, so I can tailor content and training.

### Acceptance Criteria
- [ ] Bar chart: distortion types ranked by frequency
- [ ] Example: Catastrophizing (34%), All-or-nothing (22%), Mind-reading (18%), ...
- [ ] Filter by date range
- [ ] Drill down: click a distortion → see example situations from sessions (anonymized)
- [ ] Insight: "Most common distortion this month: catastrophizing"

### Technical Notes
- Extract `distortion` field from `cbt_data.insights` across all sessions
- GROUP BY distortion, COUNT, ORDER BY count DESC
- API route: GET `/api/admin/analytics/distortions`

---

## AD-011: Homework Completion Rate

**Priority:** Medium
**Effort:** Medium
**Category:** CBT Effectiveness

### Description
As an admin, I want to track homework completion rates, so I can understand user engagement between sessions.

### Acceptance Criteria
- [ ] % of sessions where homework was assigned
- [ ] % of users who completed assigned homework (self-reported or inferred)
- [ ] Avg time between homework assignment and completion
- [ ] Trend over time
- [ ] List of most commonly assigned homework types

### Technical Notes
- Query `cbt_data.homework` (non-null = assigned)
- Completion tracking requires US-016 (homework banner with "mark complete")
- API route: GET `/api/admin/analytics/homework`

---

## AD-012: Crisis Alert Log

**Priority:** Critical
**Effort:** Low
**Category:** Crisis & Safety

### Description
As an admin, I want a real-time log of all crisis alerts, so I can monitor safety incidents and ensure appropriate responses.

### Acceptance Criteria
- [ ] Real-time feed of crisis events (newest first)
- [ ] Each entry: timestamp, user (email or anonymized ID), trigger reason, transcript snippet
- [ ] Severity indicator: keyword-detected vs LLM-flagged
- [ ] Status: new / reviewed / escalated / resolved
- [ ] Click to view full session transcript
- [ ] Email/Slack notification to admin on new crisis alert
- [ ] Filter by date range, status, user

### Technical Notes
- New Supabase table: `crisis_alerts` (id, user_id, session_id, reason, trigger_type, status, created_at)
- Agent writes to this table via Supabase REST API or saves in cbt_data
- Admin API route: GET/PATCH `/api/admin/crisis-alerts`
- Real-time: Supabase Realtime subscription or polling
- Page: `/admin/crisis`

---

## AD-013: Crisis Response Audit

**Priority:** High
**Effort:** Medium
**Category:** Crisis & Safety

### Description
As an admin, I want to audit how the system handled each crisis, so I can verify compliance and improve response protocols.

### Acceptance Criteria
- [ ] For each crisis alert: did the agent provide emergency contacts? (check transcript)
- [ ] Did the emergency banner display on the frontend? (log event)
- [ ] How long did the user stay after crisis was flagged?
- [ ] Did the user click any emergency contact link?
- [ ] Admin can add notes and mark as "reviewed"
- [ ] Generate compliance report for a date range

### Technical Notes
- Correlate `crisis_alerts` with `session_messages` and frontend click events
- Frontend: log when user taps emergency contact (send event to analytics or Supabase)
- Page: `/admin/crisis/[id]`

---

## AD-014: Flagged User List

**Priority:** High
**Effort:** Low
**Category:** Crisis & Safety

### Description
As an admin, I want to see all users who have triggered crisis detection, so I can prioritize follow-up.

### Acceptance Criteria
- [ ] Table: user email, number of crisis flags, most recent flag date, most recent reason
- [ ] Sort by: frequency (most flags first), recency (most recent first)
- [ ] Status per user: needs review / under monitoring / resolved
- [ ] Click → user detail view with crisis history highlighted
- [ ] Bulk actions: mark as reviewed, assign to counselor

### Technical Notes
- Aggregate `crisis_alerts` by user_id
- Join with `auth.users` for email
- Page: `/admin/crisis/users`

---

## AD-015: Escalation Workflow

**Priority:** Medium
**Effort:** High
**Category:** Crisis & Safety

### Description
As an admin, I want to escalate a flagged user to a human counselor, so high-risk users get professional follow-up.

### Acceptance Criteria
- [ ] "Escalate" button on flagged user or crisis alert
- [ ] Assign to a counselor from a list of available staff
- [ ] Send notification to assigned counselor (email or in-app)
- [ ] Counselor can view user's session history and crisis context
- [ ] Status tracking: escalated → in progress → resolved
- [ ] Notes field for counselor observations
- [ ] Audit trail of all escalation actions

### Technical Notes
- New Supabase tables: `escalations` (id, user_id, assigned_to, status, notes, created_at), `staff` (id, name, email, role)
- Email integration: Resend or SendGrid for notifications
- Page: `/admin/escalations`

---

## AD-016: Response Latency Dashboard

**Priority:** Medium
**Effort:** Medium
**Category:** Agent Performance

### Description
As an admin, I want to monitor the agent's response speed, so I can identify and fix performance bottlenecks.

### Acceptance Criteria
- [ ] Avg end-to-end latency: user stops speaking → agent starts speaking
- [ ] Breakdown: STT latency + LLM latency + TTS latency
- [ ] P50, P90, P99 latency percentiles
- [ ] Trend over time (daily averages)
- [ ] Alert if P90 exceeds threshold (e.g., > 3 seconds)

### Technical Notes
- LiveKit agents SDK may expose timing metrics
- Alternatively, log timestamps at each pipeline stage in agent.py
- Store in Supabase or external metrics system (Grafana/Prometheus)
- Page: `/admin/performance`

---

## AD-017: Avatar Uptime Dashboard

**Priority:** Medium
**Effort:** Low
**Category:** Agent Performance

### Description
As an admin, I want to know how often the HeyGen avatar loads successfully, so I can track reliability and user experience.

### Acceptance Criteria
- [ ] % of sessions with avatar (video) vs audio-only (fallback)
- [ ] Failure reasons breakdown: no credits, concurrency limit, timeout, other
- [ ] Trend over time
- [ ] Alert when avatar failure rate exceeds 20%

### Technical Notes
- Agent already logs "✓ HeyGen LiveAvatar started successfully" and "⚠ Warning: Failed..."
- Parse logs or add structured logging to a Supabase table
- New table or column: `therapy_sessions.avatar_loaded` (boolean)
- Page: `/admin/performance`

---

## AD-018: TTS/STT Error Rates

**Priority:** Medium
**Effort:** Low
**Category:** Agent Performance

### Description
As an admin, I want to track API error rates for TTS, STT, and other services, so I can catch outages early.

### Acceptance Criteria
- [ ] Error rate per service: Cartesia TTS, Deepgram STT, HeyGen, OpenAI, Pinecone
- [ ] Error types: 402 (billing), 429 (rate limit), 500 (server error), timeout
- [ ] Real-time status indicator: green/yellow/red per service
- [ ] Alert on sudden error spike
- [ ] Historical trend (last 7 days)

### Technical Notes
- Structured error logging in agent.py → Supabase table `api_errors` (service, status_code, message, timestamp)
- Or use existing Fly.io log aggregation
- Page: `/admin/performance`

---

## AD-019: API Cost Tracker

**Priority:** Medium
**Effort:** Medium
**Category:** Agent Performance

### Description
As an admin, I want to see estimated API costs per service, so I can manage budget and prevent unexpected charges.

### Acceptance Criteria
- [ ] Estimated daily/weekly/monthly cost per service
- [ ] OpenAI: based on token usage (input + output tokens × price)
- [ ] Cartesia: based on character count × price per character
- [ ] Deepgram: based on audio seconds × price per second
- [ ] HeyGen: based on session minutes × price per minute
- [ ] Pinecone: based on query count
- [ ] Total estimated spend with trend chart
- [ ] Budget alert: notify when projected monthly spend exceeds threshold

### Technical Notes
- Track usage metrics in agent.py (tokens, characters, audio seconds)
- Store in Supabase: `api_usage` (service, metric, value, timestamp)
- Apply pricing formulas from each provider's pricing page
- Page: `/admin/costs`

---

## AD-020: Knowledge Base Manager

**Priority:** Low
**Effort:** High
**Category:** Content & Knowledge Base

### Description
As an admin, I want to manage knowledge base documents from the admin UI, so I can update CBT content without SSH access.

### Acceptance Criteria
- [ ] List all documents in Pinecone assistant with name, upload date, size
- [ ] Upload new documents (txt, pdf, md)
- [ ] Delete documents
- [ ] Preview document content
- [ ] Re-upload/replace a document
- [ ] Changes reflected in agent's knowledge base immediately

### Technical Notes
- Pinecone Assistant API: list_files(), upload_file(), delete_file()
- Admin API routes: GET/POST/DELETE `/api/admin/knowledge-base`
- File upload handling with multipart form data
- Page: `/admin/knowledge-base`

---

## AD-021: RAG Query Log

**Priority:** Low
**Effort:** Medium
**Category:** Content & Knowledge Base

### Description
As an admin, I want to see what users are asking the knowledge base, so I can identify content gaps and improve documentation.

### Acceptance Criteria
- [ ] Log of all `ask_knowledge_base` queries with timestamp, query text, response snippet
- [ ] Most common queries (word cloud or frequency list)
- [ ] Queries with poor/no results (identify content gaps)
- [ ] Filter by date range
- [ ] Link to session where query was made

### Technical Notes
- Log queries in agent.py `ask_knowledge_base` function → Supabase table `rag_queries`
- Table: (id, session_id, query, response_snippet, created_at)
- Page: `/admin/knowledge-base/queries`

---

## AD-022: System Prompt Editor

**Priority:** Medium
**Effort:** Medium
**Category:** Content & Knowledge Base

### Description
As an admin, I want to edit the agent's system prompt from the admin UI, so I can tune behavior without redeploying.

### Acceptance Criteria
- [ ] Text editor showing current BASE_INSTRUCTIONS
- [ ] Syntax-highlighted markdown editor
- [ ] Save → updates stored in Supabase (agent reads from DB instead of hardcoded)
- [ ] Version history: see previous versions and rollback
- [ ] Preview mode: test prompt in a sandbox session before going live
- [ ] Audit log: who changed the prompt and when

### Technical Notes
- New Supabase table: `agent_config` (id, key, value TEXT, updated_by, updated_at)
- Agent reads BASE_INSTRUCTIONS from Supabase on startup (fallback to hardcoded)
- Admin API routes: GET/PUT `/api/admin/agent-config`
- Page: `/admin/agent/prompt`

---

## AD-023: System Health Dashboard

**Priority:** Medium
**Effort:** Medium
**Category:** Platform Operations

### Description
As an admin, I want to see the health of all system components, so I can detect and resolve issues quickly.

### Acceptance Criteria
- [ ] Status indicators for: Fly.io backend, Fly.io frontend, LiveKit Cloud, Supabase, Pinecone, Cartesia, Deepgram, HeyGen
- [ ] For each: up/down status, last checked, response time
- [ ] Active LiveKit rooms count and connected participants
- [ ] Fly.io machine status: CPU, memory, uptime
- [ ] Auto-refresh every 60 seconds
- [ ] Incident history log

### Technical Notes
- Health check endpoints for each service
- Fly.io: `fly status` API or machine API
- LiveKit: server SDK to list rooms
- Others: simple HTTP ping to API endpoints
- Page: `/admin/system`

---

## AD-024: Feature Flags

**Priority:** Medium
**Effort:** Medium
**Category:** Platform Operations

### Description
As an admin, I want to toggle features on/off without redeploying, so I can control the user experience and manage incidents.

### Acceptance Criteria
- [ ] Toggle switches for: Avatar (HeyGen), Crisis Detection, CBT Tools (log_mood, log_cbt_insight, set_homework), Session History, Knowledge Base RAG
- [ ] Changes take effect on next session (not mid-session)
- [ ] Stored in Supabase, read by both frontend and backend
- [ ] Audit log of flag changes
- [ ] Per-user overrides (e.g., enable beta features for specific users)

### Technical Notes
- New Supabase table: `feature_flags` (id, flag_name, enabled BOOLEAN, updated_by, updated_at)
- Frontend reads flags on page load
- Agent reads flags on session start
- Admin API routes: GET/PUT `/api/admin/feature-flags`
- Page: `/admin/features`

---

## AD-025: User Management

**Priority:** High
**Effort:** Medium
**Category:** Platform Operations

### Description
As an admin, I want to manage user accounts, so I can handle support requests and maintain security.

### Acceptance Criteria
- [ ] Invite new users via email
- [ ] Deactivate/reactivate user accounts
- [ ] Reset user password (send reset email)
- [ ] Assign roles: user, admin, counselor
- [ ] View user's last login and session count
- [ ] Delete user and all associated data (GDPR compliance)
- [ ] Export user data (GDPR data portability)

### Technical Notes
- Supabase Auth admin API (service role key)
- Role management via Supabase custom claims or `user_roles` table
- Admin API routes: POST/PATCH/DELETE `/api/admin/users`
- Page: `/admin/users` (extend AD-001)

---

## AD-026: Audit Log

**Priority:** Medium
**Effort:** Low
**Category:** Platform Operations

### Description
As an admin, I want a log of all admin actions, so I can maintain accountability and compliance.

### Acceptance Criteria
- [ ] Log entries for: user viewed transcript, changed feature flag, escalated user, edited prompt, deleted user
- [ ] Each entry: timestamp, admin email, action type, target (user/resource), details
- [ ] Searchable and filterable by action type, admin, date range
- [ ] Immutable (admins cannot delete audit log entries)
- [ ] Exportable to CSV

### Technical Notes
- New Supabase table: `audit_log` (id, admin_id, action, target_type, target_id, details JSONB, created_at)
- RLS: admins can SELECT only, INSERT via service role
- Middleware/helper function that auto-logs admin API calls
- Page: `/admin/audit-log`
