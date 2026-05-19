# Therapist Dashboard Backlog

Backlog for the **therapist tier** — licensed clinicians who oversee AI-led CBT sessions on Theraverse, review patient progress between sessions, intervene during crises, and provide continuity of care.

**Scope decisions:**
- Access model: assigned caseload + shared crisis pool (HIPAA-style scoping with safety override)
- Async review only — no live video sessions in scope
- Clinical workflow lite — free-form notes only, no SOAP/billing/insurance

Companion files:
- [BACKLOG.md](BACKLOG.md) — patient + admin features
- [STORIES.md](STORIES.md) — patient (US-XXX) + admin (AD-XXX) detailed stories

Story IDs in this file use the **TH-XXX** prefix.

---

## Foundation

- [ ] **TH-000 Therapist role & permissions foundation** — Roles table, therapist profiles, patient-therapist assignments, RLS scoping for caseload + crisis pool

## Caseload Management

- [ ] **TH-001 Caseload dashboard** — Cards for assigned patients showing last session, mood trend, alerts
- [ ] **TH-002 Patient search & filter** — Filter by status, mood trend, last activity, risk level
- [ ] **TH-003 Self-assign from crisis pool** — Pick up unassigned flagged patients
- [ ] **TH-004 Reassign patient** — Hand off a patient to another therapist
- [ ] **TH-005 Caseload health metrics** — Active / inactive / at-risk counts at a glance

## Patient Clinical View

- [ ] **TH-006 Patient profile page** — Demographics, goals, summary, assignment history
- [ ] **TH-007 AI session timeline** — Chronological list of all AI sessions with the patient
- [ ] **TH-008 Session transcript reader** — Read full conversation transcripts with CBT data sidebar
- [ ] **TH-009 Mood trajectory chart per patient** — Start vs end mood across all sessions
- [ ] **TH-010 CBT progress tracker** — Distortions identified, thought records, homework completion
- [ ] **TH-011 Vitals & emotion history** — rPPG BPM and Hume emotion timeline per patient
- [ ] **TH-012 Engagement score** — Frequency, duration, dropout risk indicator

## Crisis Pool & Alerts

- [ ] **TH-013 Real-time crisis alert feed** — Live feed of crises across caseload + pool
- [ ] **TH-014 Crisis pool inbox** — Unassigned flagged patients needing review
- [ ] **TH-015 Mark crisis as reviewed** — Status workflow: new → reviewed → resolved
- [ ] **TH-016 Push & email crisis notifications** — Alert therapist when caseload patient triggers crisis

## Clinical Notes (Lite)

- [ ] **TH-017 Patient-level notes** — Free-form, timestamped notes per patient
- [ ] **TH-018 Session-level notes** — Annotations against specific AI sessions
- [ ] **TH-019 Note templates** — Quick-insert common observations
- [ ] **TH-020 Notes timeline view** — Chronological view of all notes per patient

## Patient Communication

- [ ] **TH-021 Send message to patient** — Async message with email notification
- [ ] **TH-022 Patient message inbox** — Read messages from patients
- [ ] **TH-023 Quick prompts library** — Suggested follow-up messages
- [ ] **TH-024 Schedule check-in nudge** — Auto-send "How did your homework go?"

## Care Goals (Lite)

- [ ] **TH-025 Set patient goals** — Free-form goals tracked over time
- [ ] **TH-026 Review goal progress** — Status changes timeline
- [ ] **TH-027 Tag CBT focus areas** — Tags inform agent prompt (e.g., focus on catastrophizing)

## Caseload Analytics & Profile

- [ ] **TH-028 Caseload-wide mood trend** — Aggregated mood across all assigned patients
- [ ] **TH-029 Top distortions across caseload** — Where to focus interventions
- [ ] **TH-030 At-risk patient list** — Declining mood, missed sessions, repeat crises
- [ ] **TH-031 Therapist profile** — Bio, credentials, photo, specialties
- [ ] **TH-032 Notification preferences** — Email/push toggles, caseload capacity limit

---

# Detailed Stories

## TH-000: Therapist Role & Permissions Foundation

**Priority:** Critical
**Effort:** High
**Category:** Foundation

### Description
As an engineering team, we need a role/permissions foundation, so therapists can access only their assigned patients (plus the shared crisis pool) without exposing other patients' data.

### Acceptance Criteria
- [ ] `user_roles` table with role values: `patient`, `therapist`, `admin`
- [ ] `therapist_profiles` table (user_id, display_name, credentials, bio, specialties, max_caseload)
- [ ] `patient_assignments` table (id, patient_id, therapist_id, assigned_at, assigned_by, ended_at nullable)
- [ ] RLS policies: therapists can SELECT `therapy_sessions` and `session_messages` for assigned patients OR for patients with active crisis flags
- [ ] Middleware in [agent-starter-react/lib/supabase/middleware.ts](agent-starter-react/lib/supabase/middleware.ts) enforces role check on `/therapist/*` routes — non-therapists redirected
- [ ] Helper function `getCurrentTherapistAssignments(userId)` returns assigned patient IDs

### Technical Notes
- Build on the `counselor` role mentioned in [STORIES.md](STORIES.md) AD-025
- New migration: `agent-starter-react/supabase/migrations/<timestamp>_therapist_roles.sql`
- Reuse the RLS pattern from [agent-starter-react/supabase/migrations/20260318000000_therapy_sessions.sql](agent-starter-react/supabase/migrations/20260318000000_therapy_sessions.sql)
- Page namespace: `app/(app)/therapist/` route group with role-protected layout

---

## TH-001: Caseload Dashboard

**Priority:** High
**Effort:** Medium
**Category:** Caseload Management

### Description
As a therapist, I want a dashboard listing all my assigned patients with status indicators, so I can quickly see who needs attention and what's happening across my caseload.

### Acceptance Criteria
- [ ] Landing page at `/therapist` shows grid/list of patient cards
- [ ] Each card: anonymized name or ID, last session date, mood trend arrow, total sessions, status pill (stable / monitoring / at-risk / crisis)
- [ ] Empty state: "No patients assigned yet"
- [ ] Sort by: last activity, name, risk level
- [ ] Card count badge: "12 patients (2 at-risk, 1 in crisis)"
- [ ] Click card → navigates to TH-006 patient profile

### Technical Notes
- Page: `agent-starter-react/app/(app)/therapist/page.tsx`
- Component: `agent-starter-react/components/therapist/caseload-grid.tsx`
- Query: join `patient_assignments` → `auth.users` → aggregate latest `therapy_sessions` + `crisis_alerts`
- API route: GET `/api/therapist/caseload`

---

## TH-002: Patient Search & Filter

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Management

### Description
As a therapist with many patients, I want to search and filter my caseload, so I can find specific patients quickly.

### Acceptance Criteria
- [ ] Search bar filters by patient name/email
- [ ] Filter chips: status (stable / at-risk / crisis), last activity (active in 7 days / 30 days / inactive), mood trend (improving / declining / stable)
- [ ] Multiple filters combine (AND logic)
- [ ] Result count updates live
- [ ] "Clear all filters" link

### Technical Notes
- Client-side filtering on data already loaded by TH-001 (avoid extra round trips)
- Component: extends `caseload-grid.tsx`

---

## TH-003: Self-Assign from Crisis Pool

**Priority:** High
**Effort:** Medium
**Category:** Caseload Management

### Description
As a therapist, I want to pick up unassigned patients from the shared crisis pool, so high-risk patients get a clinician quickly even outside business hours.

### Acceptance Criteria
- [ ] Crisis pool tab at `/therapist/crisis-pool`
- [ ] Shows unassigned patients with active crisis flags
- [ ] Each entry: trigger reason, time of crisis, recent transcript snippet, severity
- [ ] "Assign to me" button creates `patient_assignments` row
- [ ] After assignment, patient appears in caseload (TH-001)
- [ ] Optimistic UI update with rollback on failure

### Technical Notes
- Page: `agent-starter-react/app/(app)/therapist/crisis-pool/page.tsx`
- Depends on AD-012 `crisis_alerts` table from [STORIES.md](STORIES.md)
- API routes: GET `/api/therapist/crisis-pool`, POST `/api/therapist/assignments`

---

## TH-004: Reassign Patient

**Priority:** Low
**Effort:** Low
**Category:** Caseload Management

### Description
As a therapist, I want to hand off a patient to another therapist, so I can manage workload and ensure coverage during leave.

### Acceptance Criteria
- [ ] "Reassign" action in patient profile (TH-006)
- [ ] Search/select target therapist from list
- [ ] Optional reason field
- [ ] Sets `ended_at` on current assignment, creates new assignment row
- [ ] Audit trail visible in patient assignment history
- [ ] Confirmation modal before action

### Technical Notes
- API route: PATCH `/api/therapist/assignments/[id]`
- Notification to receiving therapist (depends on TH-016)

---

## TH-005: Caseload Health Metrics

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Management

### Description
As a therapist, I want a quick snapshot of caseload health metrics, so I can gauge my workload and patient outcomes at a glance.

### Acceptance Criteria
- [ ] Stat cards on caseload dashboard: total assigned, active (last 7 days), inactive (no sessions in 30+ days), at-risk count, crisis count
- [ ] Sessions completed this week across caseload
- [ ] Average mood improvement across caseload (last 30 days)
- [ ] Visual indicator if any metric is concerning (e.g., red border on inactive count > 50%)

### Technical Notes
- Aggregated in same `/api/therapist/caseload` response
- Reuse stat card style from existing [agent-starter-react/components/progress-dashboard.tsx](agent-starter-react/components/progress-dashboard.tsx)

---

## TH-006: Patient Profile Page

**Priority:** High
**Effort:** Medium
**Category:** Patient Clinical View

### Description
As a therapist, I want a full clinical profile per patient, so I have one place to understand who they are and where they are in their therapy journey.

### Acceptance Criteria
- [ ] Page at `/therapist/patients/[id]`
- [ ] Header: patient name (or anonymized ID), age (if known), assigned date, status pill
- [ ] Tabs: Overview, Sessions, Mood, CBT Progress, Vitals, Notes, Goals, Messages
- [ ] Overview tab summarizes everything: last session, mood trend, top distortion, current homework, active crisis flag if any
- [ ] Quick actions: Send message, Add note, Set goal, Reassign

### Technical Notes
- Page: `agent-starter-react/app/(app)/therapist/patients/[id]/page.tsx`
- Component: `agent-starter-react/components/therapist/patient-profile.tsx`
- Tabs use existing routing pattern with subroutes
- API route: GET `/api/therapist/patients/[id]/overview`

---

## TH-007: AI Session Timeline

**Priority:** High
**Effort:** Low
**Category:** Patient Clinical View

### Description
As a therapist, I want to see all of a patient's AI sessions in chronological order, so I can track engagement and pick which session to review.

### Acceptance Criteria
- [ ] "Sessions" tab on patient profile
- [ ] List of sessions newest first: date, duration, mood change, distortion identified, homework assigned, crisis flag if any
- [ ] Each row clickable → opens TH-008 transcript
- [ ] Pagination or infinite scroll for long histories
- [ ] Filter: only sessions with crisis flags / only sessions with homework / date range

### Technical Notes
- Reuses [agent-starter-react/app/api/sessions/recent/route.ts](agent-starter-react/app/api/sessions/recent/route.ts) pattern but scoped by `patient_id` and protected by RLS
- API route: GET `/api/therapist/patients/[id]/sessions`

---

## TH-008: Session Transcript Reader

**Priority:** High
**Effort:** Low
**Category:** Patient Clinical View

### Description
As a therapist, I want to read the full transcript of any patient session, so I can understand context and assess AI conversation quality.

### Acceptance Criteria
- [ ] Page at `/therapist/patients/[id]/sessions/[sessionId]`
- [ ] Reuses existing `SessionDetail` chat-bubble layout
- [ ] CBT data sidebar: distortions, thought records, homework, emotion breakdown, vitals
- [ ] Crisis indicator banner if session was flagged
- [ ] Anonymous-mode toggle (hide patient identifiers for screen sharing)
- [ ] Audit log entry recorded when therapist views transcript

### Technical Notes
- Reuse component: [agent-starter-react/components/session-history/session-detail.tsx](agent-starter-react/components/session-history/session-detail.tsx)
- Wrap with therapist-context layout
- Audit log per AD-026 in [STORIES.md](STORIES.md)
- API route: GET `/api/therapist/patients/[id]/sessions/[sessionId]`

---

## TH-009: Mood Trajectory Chart Per Patient

**Priority:** High
**Effort:** Low
**Category:** Patient Clinical View

### Description
As a therapist, I want to see how a patient's mood has changed across sessions, so I can assess whether therapy is working.

### Acceptance Criteria
- [ ] "Mood" tab on patient profile
- [ ] Line chart: start-of-session vs end-of-session mood (red → green)
- [ ] Date range filter (7d / 30d / 90d / all time)
- [ ] Hover shows exact values + session date
- [ ] Aggregate stats: avg start mood, avg end mood, % of sessions with improvement
- [ ] Mood-journal entries (out-of-session) overlaid as dots

### Technical Notes
- Reuses chart pattern from [agent-starter-react/components/progress-dashboard.tsx](agent-starter-react/components/progress-dashboard.tsx)
- Reuses [agent-starter-react/app/api/progress/route.ts](agent-starter-react/app/api/progress/route.ts) logic, scoped by `patient_id`
- API route: GET `/api/therapist/patients/[id]/mood`

---

## TH-010: CBT Progress Tracker

**Priority:** High
**Effort:** Medium
**Category:** Patient Clinical View

### Description
As a therapist, I want to see the patient's CBT progress (distortions, thought records, homework), so I can guide future sessions and identify recurring patterns.

### Acceptance Criteria
- [ ] "CBT Progress" tab on patient profile
- [ ] Distortion frequency bar chart (most common patterns)
- [ ] Recent thought records list with situation → automatic thought → distortion → balanced thought
- [ ] Homework history with assigned/completed status (if completion tracking exists)
- [ ] Insight panel: "Catastrophizing identified in 60% of sessions — consider focused intervention"

### Technical Notes
- Aggregates `cbt_data.insights` and `cbt_data.homework` from patient's `therapy_sessions`
- Component: `agent-starter-react/components/therapist/cbt-progress-tracker.tsx`
- API route: GET `/api/therapist/patients/[id]/cbt-progress`

---

## TH-011: Vitals & Emotion History

**Priority:** Medium
**Effort:** Medium
**Category:** Patient Clinical View

### Description
As a therapist, I want to see physiological and emotional patterns from rPPG and Hume across sessions, so I can correlate biological signals with conversation topics.

### Acceptance Criteria
- [ ] "Vitals" tab on patient profile
- [ ] Heart rate (BPM) timeline across sessions
- [ ] HRV trend across sessions
- [ ] Stress level distribution (low/moderate/high)
- [ ] Top emotions detected aggregated from `cbt_data.emotions`
- [ ] Emotion + transcript overlay (clicking an emotion spike opens the corresponding transcript moment)

### Technical Notes
- Aggregates `cbt_data.emotions` and any future vitals storage
- Note: rPPG vitals are currently sent but may need to be persisted to `cbt_data` (future story)
- API route: GET `/api/therapist/patients/[id]/vitals`

---

## TH-012: Engagement Score

**Priority:** Medium
**Effort:** Medium
**Category:** Patient Clinical View

### Description
As a therapist, I want an engagement score per patient, so I can flag patients at risk of dropping out.

### Acceptance Criteria
- [ ] Composite score 0-100 visible on patient card and profile
- [ ] Inputs: session frequency (last 30 days), avg session duration, days since last session, homework completion rate, mood-journal entries
- [ ] Trend indicator: improving / stable / declining
- [ ] Tooltip explains how the score is calculated
- [ ] Patients with score < 30 surface in TH-030 at-risk list

### Technical Notes
- Computed server-side and cached daily
- API route: GET `/api/therapist/patients/[id]/engagement`

---

## TH-013: Real-Time Crisis Alert Feed

**Priority:** Critical
**Effort:** Low
**Category:** Crisis Pool & Alerts

### Description
As a therapist, I want a live feed of crisis alerts across my caseload and the crisis pool, so I can respond to safety incidents immediately.

### Acceptance Criteria
- [ ] Persistent badge in nav: "🚨 2 active crises"
- [ ] Feed page at `/therapist/alerts`
- [ ] Newest alert first with: patient (anonymizable), trigger reason, transcript snippet, time, severity (keyword vs LLM-flagged)
- [ ] Source label: "Caseload" or "Pool"
- [ ] Click alert → opens session transcript with crisis moment highlighted
- [ ] Filter: status (new / reviewed / resolved), source, date range
- [ ] Real-time updates via Supabase Realtime subscription

### Technical Notes
- Depends on AD-012 `crisis_alerts` table from [STORIES.md](STORIES.md)
- Realtime subscription on `crisis_alerts` filtered by therapist's caseload + pool
- Page: `agent-starter-react/app/(app)/therapist/alerts/page.tsx`

---

## TH-014: Crisis Pool Inbox

**Priority:** High
**Effort:** Low
**Category:** Crisis Pool & Alerts

### Description
As a therapist, I want to see flagged patients with no assigned therapist, so I can pick them up from the shared pool.

### Acceptance Criteria
- [ ] Tab on `/therapist/alerts` filtered to unassigned crises
- [ ] Each entry: trigger reason, time, recent transcript, "Assign to me" button (uses TH-003)
- [ ] Empty state: "No patients in crisis pool — well done team!"
- [ ] Counter showing how many therapists are currently online (optional)

### Technical Notes
- Combines TH-003 self-assign action with TH-013 alert feed view
- Same API route as TH-013, filtered server-side

---

## TH-015: Mark Crisis as Reviewed

**Priority:** High
**Effort:** Low
**Category:** Crisis Pool & Alerts

### Description
As a therapist, I want to update the status of a crisis alert (reviewed / under monitoring / resolved), so the team knows it's been handled.

### Acceptance Criteria
- [ ] Status dropdown on each crisis alert: New, Reviewed, Under Monitoring, Resolved
- [ ] Required note field when changing to Resolved
- [ ] Status change appears in audit log with therapist + timestamp
- [ ] Resolved crises hidden from default feed but accessible via filter

### Technical Notes
- API route: PATCH `/api/therapist/crisis-alerts/[id]`
- Audit log per AD-026 in [STORIES.md](STORIES.md)

---

## TH-016: Push & Email Crisis Notifications

**Priority:** High
**Effort:** Medium
**Category:** Crisis Pool & Alerts

### Description
As a therapist, I want push and email notifications when a caseload patient triggers a crisis, so I can respond even when I'm not actively in the dashboard.

### Acceptance Criteria
- [ ] Email sent to therapist when crisis triggers for assigned patient
- [ ] Web push notification (if browser permission granted)
- [ ] Opt-in / opt-out per channel (email, push) in TH-032 preferences
- [ ] Quiet hours support (no notifications between configured times)
- [ ] Notification deep-links to the alert feed

### Technical Notes
- Email: Resend or SendGrid integration
- Web Push: VAPID keys + service worker
- Triggered by Supabase database webhook on `crisis_alerts` insert
- Preferences stored in `therapist_profiles.notification_preferences` JSONB

---

## TH-017: Patient-Level Notes

**Priority:** High
**Effort:** Low
**Category:** Clinical Notes (Lite)

### Description
As a therapist, I want to add free-form notes about a patient, so I can record observations and treatment decisions over time.

### Acceptance Criteria
- [ ] "Notes" tab on patient profile
- [ ] "+ Add note" button opens text editor
- [ ] Notes show author (therapist), timestamp, content
- [ ] Newest first, full content visible
- [ ] Edit/delete own notes (other therapists' notes are read-only)
- [ ] Markdown formatting supported

### Technical Notes
- New Supabase table: `clinical_notes` (id, patient_id, therapist_id, session_id nullable, content TEXT, created_at, updated_at)
- RLS: therapists can SELECT all notes for assigned patients, INSERT/UPDATE/DELETE own only
- API routes: GET/POST `/api/therapist/patients/[id]/notes`, PATCH/DELETE `/api/therapist/notes/[noteId]`

---

## TH-018: Session-Level Notes

**Priority:** Medium
**Effort:** Low
**Category:** Clinical Notes (Lite)

### Description
As a therapist, I want to attach notes to specific AI sessions, so I can flag particular moments for follow-up.

### Acceptance Criteria
- [ ] "Add note" action visible on session transcript reader (TH-008)
- [ ] Note links to specific session via `session_id` foreign key
- [ ] Session-linked notes also appear in the patient notes tab (TH-017) with session date prefix
- [ ] Optional: attach note to a specific message in the transcript

### Technical Notes
- Reuses `clinical_notes` table from TH-017
- Frontend differentiates patient-level vs session-level notes by `session_id` presence

---

## TH-019: Note Templates

**Priority:** Low
**Effort:** Low
**Category:** Clinical Notes (Lite)

### Description
As a therapist, I want quick-insert note templates for common observations, so I can document faster.

### Acceptance Criteria
- [ ] "Templates" dropdown in note editor
- [ ] Default templates: "Mood improvement noted", "Homework not completed", "Crisis follow-up", "Recommend medication review"
- [ ] Therapist can create personal custom templates
- [ ] Selecting template inserts text at cursor (editable after insertion)

### Technical Notes
- New Supabase table: `note_templates` (id, therapist_id nullable, name, content, is_global)
- Global templates visible to all therapists; personal ones to owner only

---

## TH-020: Notes Timeline View

**Priority:** Low
**Effort:** Low
**Category:** Clinical Notes (Lite)

### Description
As a therapist, I want a chronological timeline of all notes for a patient, so I can quickly review the care narrative.

### Acceptance Criteria
- [ ] Notes tab can switch between "List" and "Timeline" view
- [ ] Timeline shows notes interleaved with major events (sessions, crisis flags, mood changes, goal updates)
- [ ] Visual differentiation between event types
- [ ] Filter: notes only / events only / everything

### Technical Notes
- Composite query joining `clinical_notes`, `therapy_sessions`, `crisis_alerts`, `patient_goals`
- API route: GET `/api/therapist/patients/[id]/timeline`

---

## TH-021: Send Message to Patient

**Priority:** High
**Effort:** Medium
**Category:** Patient Communication

### Description
As a therapist, I want to send asynchronous messages to my patients, so I can check in or follow up between AI sessions.

### Acceptance Criteria
- [ ] "Send message" action on patient profile
- [ ] Composer with subject + body fields
- [ ] Sent messages appear in patient's app inbox AND trigger an email
- [ ] Therapist sees sent message in TH-022 inbox under "Sent"
- [ ] Read receipts when patient opens message
- [ ] Message body supports markdown

### Technical Notes
- New Supabase table: `patient_messages` (id, patient_id, therapist_id, sender enum, subject, body, read_at, created_at)
- RLS: patient can read own messages; therapist can read messages for assigned patients
- Patient-side inbox is a new patient feature (could be added to BACKLOG.md as a follow-up US story)
- Email via Resend with branded template
- API routes: POST `/api/therapist/patients/[id]/messages`

---

## TH-022: Patient Message Inbox

**Priority:** Medium
**Effort:** Low
**Category:** Patient Communication

### Description
As a therapist, I want a unified inbox of messages from all my patients, so I can respond efficiently.

### Acceptance Criteria
- [ ] Inbox page at `/therapist/messages`
- [ ] Threads grouped by patient
- [ ] Unread count badge in nav
- [ ] Click thread → see conversation history + reply composer
- [ ] Filter: unread, by patient, by date

### Technical Notes
- API route: GET `/api/therapist/messages`
- Reuse `patient_messages` from TH-021

---

## TH-023: Quick Prompts Library

**Priority:** Low
**Effort:** Low
**Category:** Patient Communication

### Description
As a therapist, I want pre-written message prompts I can quickly send, so I can encourage patients without typing each time.

### Acceptance Criteria
- [ ] Prompt library accessible from message composer
- [ ] Defaults: "How did your homework go this week?", "Just checking in — how are you feeling?", "I noticed you haven't logged in for a while, everything okay?"
- [ ] Therapist can create personal prompts
- [ ] Selected prompt populates composer (editable before sending)

### Technical Notes
- Reuses `note_templates` table pattern (TH-019) — could share or split into `message_templates`

---

## TH-024: Schedule Check-In Nudge

**Priority:** Low
**Effort:** Medium
**Category:** Patient Communication

### Description
As a therapist, I want to schedule auto-sent check-in nudges based on patient activity, so disengaged patients get prompted without manual effort.

### Acceptance Criteria
- [ ] Configure nudge rules per patient: "If no session in 7 days, send check-in"
- [ ] Nudge text customizable per rule
- [ ] Nudge logged in patient profile (so therapist sees it was sent)
- [ ] Patient receives nudge via in-app message + email
- [ ] Nudge can be paused per patient

### Technical Notes
- New Supabase table: `nudge_rules` (id, patient_id, therapist_id, trigger_condition JSONB, message_template, enabled, last_fired_at)
- Background job (cron / Supabase scheduled function) checks rules nightly

---

## TH-025: Set Patient Goals

**Priority:** Medium
**Effort:** Medium
**Category:** Care Goals (Lite)

### Description
As a therapist, I want to set free-form treatment goals per patient, so we have shared targets to work toward.

### Acceptance Criteria
- [ ] "Goals" tab on patient profile
- [ ] "+ Add goal" with title, description, target date (optional), status (active / achieved / abandoned)
- [ ] Patient can see their own goals in their dashboard (new patient story to follow)
- [ ] Therapist can update status and add progress notes against each goal

### Technical Notes
- New Supabase table: `patient_goals` (id, patient_id, set_by_therapist_id, title, description, target_date, status, created_at)
- RLS: patient sees own goals; therapist sees goals for assigned patients
- API routes: GET/POST/PATCH `/api/therapist/patients/[id]/goals`

---

## TH-026: Review Goal Progress

**Priority:** Medium
**Effort:** Low
**Category:** Care Goals (Lite)

### Description
As a therapist, I want to see goal progress over time, so I can celebrate wins or adjust the treatment plan.

### Acceptance Criteria
- [ ] Goal status changes shown as a timeline
- [ ] Stats: total goals, achieved, active, abandoned
- [ ] Per-goal: list of status changes with timestamps and notes
- [ ] Visual indicator for goals approaching target date

### Technical Notes
- New table: `goal_status_changes` (id, goal_id, old_status, new_status, note, changed_at)

---

## TH-027: Tag CBT Focus Areas

**Priority:** Medium
**Effort:** Medium
**Category:** Care Goals (Lite)

### Description
As a therapist, I want to tag a patient with specific CBT focus areas (e.g., catastrophizing, social anxiety), so the AI agent prioritizes them in future sessions.

### Acceptance Criteria
- [ ] Tag picker on patient profile with predefined CBT concepts (the 12 distortions, common themes)
- [ ] Tags stored per patient
- [ ] Agent reads tags when starting session and includes in system prompt context
- [ ] Therapist can update tags any time
- [ ] Patient can see their own tags

### Technical Notes
- New table: `patient_focus_tags` (id, patient_id, tag, set_by_therapist_id, created_at)
- Agent updates: read tags via participant metadata (similar to existing homework continuity)
- Update [agent.py](agent.py) to include focus tags in `BASE_INSTRUCTIONS` extension

---

## TH-028: Caseload-Wide Mood Trend

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Analytics & Profile

### Description
As a therapist, I want aggregated mood trends across my entire caseload, so I can gauge overall outcomes.

### Acceptance Criteria
- [ ] Chart on caseload dashboard: avg start mood vs avg end mood across all caseload sessions over time
- [ ] Date range filter
- [ ] "% of caseload showing improvement this month" headline number
- [ ] Compare to previous period

### Technical Notes
- Aggregates `cbt_data.mood_ratings` across all assigned patients' sessions
- API route: GET `/api/therapist/analytics/mood`

---

## TH-029: Top Distortions Across Caseload

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Analytics & Profile

### Description
As a therapist, I want to see which cognitive distortions appear most often across my caseload, so I can build expertise and content for common patterns.

### Acceptance Criteria
- [ ] Bar chart: distortion frequency across caseload
- [ ] Date range filter
- [ ] Drill down: click distortion → list of patients exhibiting it
- [ ] Insight panel: "3 of your patients struggle with catastrophizing this month"

### Technical Notes
- Aggregates `cbt_data.insights[].distortion` across all assigned patients
- API route: GET `/api/therapist/analytics/distortions`

---

## TH-030: At-Risk Patient List

**Priority:** High
**Effort:** Medium
**Category:** Caseload Analytics & Profile

### Description
As a therapist, I want a list of at-risk patients prioritized by urgency, so I know who to contact first.

### Acceptance Criteria
- [ ] Page or panel showing patients sorted by risk score (descending)
- [ ] Risk factors visible per patient: declining mood trend, missed sessions, repeat crises, low engagement (TH-012)
- [ ] Bulk action: send check-in message (uses TH-021)
- [ ] Filter: by risk factor type
- [ ] Refresh on demand

### Technical Notes
- Risk score = composite of TH-012 engagement + recent crisis count + mood trend slope
- API route: GET `/api/therapist/at-risk`
- Page or section within `/therapist`

---

## TH-031: Therapist Profile

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Analytics & Profile

### Description
As a therapist, I want a profile page with my credentials and specialties, so patients (and admins) know who I am.

### Acceptance Criteria
- [ ] Settings page at `/therapist/profile`
- [ ] Editable fields: display name, photo, bio, credentials (e.g., "PhD Clinical Psychology"), specialties (tags), languages
- [ ] Visible to admins; patients see their assigned therapist's profile in their own dashboard (new patient story to follow)
- [ ] Validation: can't leave name or credentials blank

### Technical Notes
- Reads/writes to `therapist_profiles` table from TH-000
- API route: GET/PATCH `/api/therapist/profile`

---

## TH-032: Notification Preferences

**Priority:** Medium
**Effort:** Low
**Category:** Caseload Analytics & Profile

### Description
As a therapist, I want to control how and when I get notified, so I can avoid burnout while staying responsive to crises.

### Acceptance Criteria
- [ ] Toggles per channel: email, web push, SMS (future)
- [ ] Toggles per event: crisis alert, new message from patient, daily digest
- [ ] Quiet hours setting (e.g., 10pm–7am)
- [ ] Caseload capacity limit (max patients) — admins won't auto-assign beyond this
- [ ] "Test notification" button

### Technical Notes
- Stored in `therapist_profiles.notification_preferences` JSONB
- API route: GET/PATCH `/api/therapist/preferences`

---

# Priority Quick-Wins (High Impact, Low Effort)

Build these first — highest clinical value relative to engineering effort:

1. **TH-013 Real-time crisis alert feed** — critical for safety, low effort once `crisis_alerts` table exists
2. **TH-001 Caseload dashboard** — primary entry point, queries existing tables
3. **TH-008 Session transcript reader** — reuses existing `SessionDetail` component
4. **TH-017 Patient-level notes** — high clinical value, single new table
5. **TH-009 Mood trajectory per patient** — reuses `/api/progress` logic and chart
6. **TH-014 Crisis pool inbox** — combines TH-013 + TH-003, no new infrastructure

# Critical Dependencies

- **TH-000 Foundation must ship first** — every other story assumes role + assignment scoping exists
- **AD-012 `crisis_alerts` table** (from [STORIES.md](STORIES.md)) — required for TH-013, TH-014, TH-015, TH-016
- **AD-026 Audit log** — required for compliance on TH-008, TH-015, and any patient data access
