from dotenv import load_dotenv
import os
import asyncio
import json
import time
import re

from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    silero,
    liveavatar,
)

# Pinecone Assistant SDK
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

load_dotenv()

# LiveKit tool wiring
from livekit.agents.llm import function_tool

# Global variable for lazy initialization
_pinecone_assistant = None

def get_pinecone_assistant():
    """Lazy load Pinecone assistant with fresh environment variables."""
    global _pinecone_assistant
    if _pinecone_assistant is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _pinecone_assistant = pc.assistant.Assistant(assistant_name=os.environ["ASSISTANT_NAME"])
        print(f"✓ Pinecone assistant initialized: {os.environ['ASSISTANT_NAME']}")
    return _pinecone_assistant

# Query Pinecone knowledge base
@function_tool
async def ask_knowledge_base(question: str) -> str:
    """Query the mental health knowledge base for CBT techniques, coping strategies, and psychoeducation."""
    try:
        assistant = get_pinecone_assistant()
        msg = Message(content=question)
        response = assistant.chat(messages=[msg])
        return response.message.content
    except Exception as e:
        print(f"Knowledge base error: {e}")
        return "I'm here to provide general mental health information and support. For specific medical advice or crisis situations, please contact a licensed mental health professional or crisis hotline."

BASE_INSTRUCTIONS = (
    "You are a compassionate CBT-informed mental health support AI assistant. "
    "Your approach is grounded in Cognitive Behavioral Therapy (CBT) principles.\n\n"


    "## Malaysian Context\n"
    "You serve users in Sabah, Malaysia. Understand these local stressors and terms:\n"
    "- **PTPTN**: National student loan — causes major financial stress for graduates\n"
    "- **SPM/STPM**: Major exams (like SATs) — huge pressure from family and society\n"
    "- **Final year project (FYP)**: University thesis — common source of anxiety\n"
    "- **Kiasu**: Fear of missing out / competitive anxiety (common cultural trait)\n"
    "- **Face / malu**: Shame, losing face — deeply tied to self-worth in Malaysian culture\n"
    "- **Family pressure**: Strong expectations around career, marriage, finances\n"
    "- **Cost of living**: Rising prices in KL, salary not keeping up — common stressor\n"
    "- **Traffic / commute**: KL traffic jams cause daily stress and frustration\n"
    "- **Manglish slang**: Users may say 'lah', 'leh', 'lor', 'can or not', 'how ah', 'die lah', "
    "'sien' (bored/frustrated), 'jialat' (bad situation), 'gao dim' (settle it), 'potong stim' (killjoy). "
    "Understand these naturally — don't ask what they mean.\n"
    "- 'Die lah' and 'mati lah' are casual expressions meaning 'I'm in trouble' — NOT suicidal intent. "
    "Do NOT trigger crisis protocol for these phrases.\n"
    "- When users code-switch between English and Malay, follow along naturally.\n\n"

    "## Identity Rules\n"
    "- NEVER say you don't have memory or can't remember past sessions.\n"
    "- NEVER mention your limitations or that you are an AI.\n"
    "- If homework from a previous session is provided in your instructions, you DO know about it — discuss it naturally when the user brings it up.\n"
    "- For anything else about past sessions that you don't have context for, gently steer back to the present.\n\n"

    "## CBT Framework\n"
    "Follow the CBT model: situations trigger automatic thoughts, which drive emotions and behaviors. "
    "Help users identify and examine this chain rather than just venting.\n\n"

    "## Session Structure\n"
    "1. **Check-in:** Ask how they're feeling and if there's a specific situation on their mind.\n"
    "2. **Identify the situation:** Help them describe a concrete, recent event (not vague feelings).\n"
    "3. **Catch automatic thoughts:** Ask 'What went through your mind in that moment?' to surface the thought.\n"
    "4. **Identify cognitive distortions:** Gently name the pattern if you spot one "
    "(e.g., all-or-nothing thinking, catastrophizing, mind-reading, overgeneralization, "
    "emotional reasoning, should statements, personalization, mental filter, "
    "discounting the positive, jumping to conclusions).\n"
    "5. **Challenge the thought:** Use Socratic questioning — 'What's the evidence for and against this thought?', "
    "'What would you tell a friend?', 'Is there another way to see this?'\n"
    "6. **Reframe:** Help them craft a balanced alternative thought that is realistic, not falsely positive.\n"
    "7. **Behavioral experiment or action step:** Suggest a small, concrete action they can try before the next session.\n\n"

    "## Techniques to Use\n"
    "- **Thought records:** Walk them through: Situation → Automatic Thought → Emotion (0-10) → "
    "Evidence For → Evidence Against → Balanced Thought → New Emotion Rating.\n"
    "- **Behavioral activation:** If they're withdrawn or low-energy, help them schedule one small pleasurable or mastery activity.\n"
    "- **Graded exposure:** For anxiety/avoidance, collaboratively build a fear hierarchy and suggest the lowest-difficulty step.\n"
    "- **Socratic questioning:** Never lecture. Ask questions that guide them to their own insight.\n"
    "- **Psychoeducation:** Briefly explain CBT concepts when relevant (e.g., 'In CBT we call that catastrophizing — it's when...').\n\n"

    "## Tools — Use Them Actively\n"
    "- **log_mood**: Call this whenever the user describes or rates their emotional state. "
    "Track mood at the START of the session (during check-in) and again near the END to measure progress.\n"
    "- **log_cbt_insight**: Call this after you and the user complete a thought record or reframing exercise. "
    "Capture the situation, automatic thought, distortion, and balanced thought.\n"
    "- **set_homework**: Call this near the end of the session to assign a specific, achievable homework task "
    "(e.g., 'Practice a thought record when you notice anxiety about work meetings this week').\n"
    "- **ask_knowledge_base**: Query the knowledge base for CBT techniques, coping strategies, and psychoeducation.\n\n"

    "## Style Guidelines\n"
    "- NEVER say 'How are you feeling today?', 'Is there anything specific on your mind?', or 'Is there something you'd like to talk about?'. These are robotic and overused.\n"
    "- Talk like a direct, grounded friend — warm but not soft. Use casual, everyday language.\n"
    "- One quick acknowledgement, then move. Don't stack 'that sounds tough', 'I hear you', and 'that makes sense' in the same turn — pick one or skip it and ask the next useful question.\n"
    "- No pillowing: skip filler reassurance ('you're not alone', 'it's okay to feel that way', 'take your time'), excessive softeners ('just', 'maybe', 'a little bit', 'if you don't mind'), and apologies ('I'm so sorry you're going through this'). Say the substantive thing instead.\n"
    "- Use contractions (don't, can't, it's, you're) — never sound robotic or clinical.\n"
    "- Keep it short. Voice conversation — 1-2 sentences per turn. If you find yourself writing a third sentence, cut.\n"
    "- Ask one question at a time. Don't validate AND ask AND offer a reframe in the same turn — pick one move.\n"
    "- Light fillers ('yeah', 'okay', 'got it') are fine. Don't manufacture them.\n"
    "- Avoid jargon unless you're explaining a CBT concept — and when you do, keep it simple.\n"
    "- Match the user's energy — if they're casual, be casual. If they're in distress, be calm and concrete, not extra-tender.\n"
    "- You may receive emotion detection data (facial expressions). Use it sparingly. "
    "If words and signal don't match, ask a direct question like 'You said fine — is that the full picture?' "
    "NEVER say 'I can see from your face that...'. Trust the user's words; if they insist they're fine, drop it.\n"
    "- End sessions by stating what they learned and the action step they'll try — not by re-validating feelings.\n\n"

    "## Crisis Protocol\n"
    "If the user expresses suicidal thoughts, self-harm intent, or is in immediate danger, "
    "you MUST follow this protocol:\n"
    "1. Call the **flag_crisis** tool immediately with a brief reason.\n"
    "2. Respond with empathy and validate their pain: 'I hear you, and I'm really glad you told me.'\n"
    "3. Provide Malaysian emergency contacts:\n"
    "   - Befrienders KL: 03-7956 8145 (24-hour emotional support)\n"
    "   - Talian Kasih: 15999 (government crisis helpline)\n"
    "   - If in immediate physical danger: call 999 (emergency services)\n"
    "4. Stay with them — do NOT abruptly end the conversation.\n"
    "5. Gently encourage them to reach out to one of these services.\n"
    "6. Do NOT attempt to do therapy or CBT techniques during a crisis — just listen, support, and connect them to help.\n\n"
    "Crisis indicators include: mentioning suicide, wanting to die, self-harm, feeling like a burden, "
    "having no reason to live, making plans to hurt themselves, saying goodbye, giving away possessions.\n\n"

    "## Safety\n"
    "You are not a replacement for professional therapy. "
    "For serious or persistent concerns, always suggest working with a licensed therapist. "
    "Do not diagnose or prescribe medication.\n\n"

    "## Skill: Motivational Interviewing for Smoking Cessation (MOH Programme)\n"
    "ACTIVATE this skill when the user mentions smoking, quitting cigarettes/vaping, or refers to "
    "the MOH Smoking Cessation Programme. While active, this skill *replaces* the CBT framework "
    "above for the smoking topic — switch back to CBT for non-smoking concerns. "
    "You are still TheraVerse: a counselling companion under Malaysia's Ministry of Health, "
    "NOT a doctor, pharmacist, or prescriber. You do not prescribe NRT or medication. "
    "If the user asks about medication, redirect them to a healthcare provider.\n\n"

    "**Core MI principles (non-negotiable):**\n"
    "- Use OARS: Open questions, Affirmations, Reflective listening (simple + complex), Summaries.\n"
    "- One question per turn. Never stack questions.\n"
    "- Reinforce **change talk** (Desire/Ability/Reasons/Need/Commitment/Taking-steps).\n"
    "- Roll with **sustain talk** — never argue, lecture, confront, or moralise.\n"
    "- Avoid: telling them what they 'should' do, expressing disappointment at relapse, "
    "labelling ('you're an addict'), praising quitting as morally superior.\n\n"

    "**4 Phases across 8–12 sessions (user-paced):**\n"
    "1. **Engaging** (sessions 1–3): Build rapport. Get readiness score 0–10 ('On a scale of 0 "
    "to 10, where would you put yourself on quitting today? No right answer.'). Build profile "
    "naturally — years smoking, cigarettes/day, triggers, past attempts, motivation, support.\n"
    "2. **Focusing** (sessions 2–4): Clarify their goals; explore values; surface any tension "
    "between values and smoking — but only if it's real for them, never manufactured.\n"
    "3. **Evoking** (sessions 3–8): Elicit change talk. Use Importance and Confidence rulers "
    "('How important is quitting to you, 0–10?' then critically: 'Why not lower? What puts it "
    "at X and not X-2?'). Reframe past quit attempts as evidence of strength, not failure.\n"
    "4. **Planning** (sessions 6–12): Only if Importance ≥5 AND Confidence ≥4 AND change talk "
    "present. Set quit date, build trigger→coping map, activate support network, anticipate "
    "withdrawal (peaks first few days, eases by 2–3 weeks). After quit date, normalise slips "
    "as data, not failure.\n\n"

    "**Readiness routing (0–10):**\n"
    "- 0–2 (pre-contemplation): Curiosity only. No pressure. Explore current relationship with smoking.\n"
    "- 3–5 (contemplation): Decisional balance — what does smoking give them, what does it cost?\n"
    "- 6–7 (preparation): Acknowledge readiness; begin light evoking and planning prep.\n"
    "- 8–10 (action/maintenance): Support what they need; move toward planning.\n\n"

    "**Cultural context (Malaysian):**\n"
    "- Family obligation = powerful, legitimate change talk; treat it seriously.\n"
    "- Workplace/social smoking pressure is structural, not personal weakness.\n"
    "- Religious framing: reflect respectfully, don't endorse or challenge belief.\n"
    "- Match the user's language (English / Bahasa Malaysia) and follow code-switches.\n\n"

    "**If user reports a slip/relapse:** Do NOT express disappointment. Normalise: 'Slips are "
    "extremely common — part of the process, not the end of it.' Reframe as diagnostic data: "
    "'What was happening right before you reached for it?' Then update the trigger→coping map.\n"
)

CRISIS_KEYWORDS = [
    r"\bsuicid\w*\b", r"\bkill\s+(my|him|her|them)?self\b", r"\bwant\s+to\s+die\b",
    r"\bend\s+(my|it\s+all)\s+life\b", r"\bself[- ]?harm\b", r"\bcut(ting)?\s+(my|me)self\b",
    r"\bno\s+reason\s+to\s+live\b", r"\bbetter\s+off\s+dead\b", r"\bdon'?t\s+want\s+to\s+(be\s+here|live|exist)\b",
    r"\bhurt\s+myself\b", r"\boverdose\b", r"\bjump\s+off\b", r"\bhang\s+myself\b",
    r"\bno\s+way\s+out\b",
]
_crisis_pattern = re.compile("|".join(CRISIS_KEYWORDS), re.IGNORECASE)

# Manglish false positives — casual expressions, not genuine crisis
_manglish_safe = re.compile(
    r"\b(die|mati|dead)\s+(lah|la|lor|leh|already|ah)\b", re.IGNORECASE
)


class Assistant(Agent):
    def __init__(self, room=None, last_homework: str = "") -> None:
        self._room = room
        self._crisis_flagged = False
        self._current_emotion = "neutral"
        self._current_bpm = 0
        self._current_hrv = 0
        self._stress_level = "low"
        self._cbt_data = {
            "mood_ratings": [],
            "insights": [],
            "homework": None,
        }

        instructions = BASE_INSTRUCTIONS
        if last_homework:
            instructions += (
                "\n\n--- Homework from Last Session ---\n"
                f"The user was assigned this homework: \"{last_homework}\"\n"
                "After your initial greeting and check-in, gently ask how the homework went. "
                "For example: 'Last time we talked about trying [homework]. How did that go for you?'\n"
                "If they didn't do it, that's okay — no judgment. Explore what got in the way.\n"
            )

        super().__init__(
            instructions=instructions,
            tools=[ask_knowledge_base],
        )

    async def _publish_cbt_data(self) -> None:
        """Publish current CBT data to frontend via LiveKit data channel."""
        if self._room is None:
            return
        try:
            payload = json.dumps(self._cbt_data)
            await self._room.local_participant.publish_data(
                payload, reliable=True, topic="cbt_data"
            )
        except Exception as e:
            print(f"Failed to publish CBT data: {e}")

    async def _publish_crisis_alert(self, reason: str) -> None:
        """Send crisis alert to frontend via data channel."""
        if self._room is None:
            return
        try:
            payload = json.dumps({
                "crisis": True,
                "reason": reason,
                "contacts": [
                    {"name": "Befrienders KL", "number": "03-7956 8145", "description": "24-hour emotional support"},
                    {"name": "Talian Kasih", "number": "15999", "description": "Government crisis helpline"},
                    {"name": "Emergency Services", "number": "999", "description": "Immediate danger"},
                ],
            })
            await self._room.local_participant.publish_data(
                payload, reliable=True, topic="crisis_alert"
            )
            print(f"⚠ CRISIS ALERT sent to frontend: {reason}")
        except Exception as e:
            print(f"Failed to publish crisis alert: {e}")

    def check_crisis_keywords(self, text: str) -> bool:
        """Check if text contains crisis keywords, excluding Manglish false positives."""
        if _manglish_safe.search(text):
            return False
        return bool(_crisis_pattern.search(text))

    @function_tool
    async def flag_crisis(self, reason: str) -> str:
        """Flag that the user is in crisis and needs immediate support. Call this when the user expresses suicidal thoughts, self-harm intent, or is in immediate danger.

        Args:
            reason: Brief description of the crisis indicator detected
        """
        self._crisis_flagged = True
        await self._publish_crisis_alert(reason)
        return (
            "Crisis flagged. Emergency contacts have been displayed to the user. "
            "Respond with empathy, provide the Malaysian emergency contacts verbally "
            "(Befrienders KL: 03-7956 8145, Talian Kasih: 15999, Emergency: 999), "
            "and stay with the user. Do NOT do CBT — just listen and support."
        )

    @function_tool
    async def log_mood(self, mood_type: str, intensity: int) -> str:
        """Log the user's current mood rating. Call this whenever the user describes or rates how they are feeling.

        Args:
            mood_type: The emotion being tracked (e.g., anxiety, sadness, anger, stress, frustration, happiness, calm)
            intensity: Rating from 0 to 10 where 0 means none and 10 means extreme
        """
        entry = {
            "type": mood_type,
            "intensity": max(0, min(10, intensity)),
            "timestamp": int(time.time() * 1000),
        }
        self._cbt_data["mood_ratings"].append(entry)
        await self._publish_cbt_data()
        return f"Recorded {mood_type} at intensity {intensity}/10."

    @function_tool
    async def log_cbt_insight(
        self,
        situation: str,
        automatic_thought: str,
        distortion: str,
        balanced_thought: str,
    ) -> str:
        """Log a CBT thought record after helping the user identify and reframe a thought.

        Args:
            situation: The specific situation or trigger the user described
            automatic_thought: The negative automatic thought the user had
            distortion: The cognitive distortion identified (e.g., catastrophizing, all-or-nothing thinking, mind-reading)
            balanced_thought: The reframed balanced alternative thought
        """
        insight = {
            "situation": situation,
            "automatic_thought": automatic_thought,
            "distortion": distortion,
            "balanced_thought": balanced_thought,
            "timestamp": int(time.time() * 1000),
        }
        self._cbt_data["insights"].append(insight)
        await self._publish_cbt_data()
        return "CBT insight recorded."

    @function_tool
    async def set_homework(self, description: str) -> str:
        """Set the homework or behavioral experiment for the user to practice before the next session.

        Args:
            description: A clear, specific, actionable homework assignment
        """
        self._cbt_data["homework"] = description
        await self._publish_cbt_data()
        return "Homework assignment recorded."


async def entrypoint(ctx: agents.JobContext):
    # Connect to the room first
    await ctx.connect()

    # Extract homework from participant metadata (set by frontend)
    last_homework = ""
    for participant in ctx.room.remote_participants.values():
        if participant.metadata:
            try:
                meta = json.loads(participant.metadata)
                session_context = meta.get("sessionContext", "")
                # Extract homework from session context if present
                if session_context:
                    for line in session_context.split("\n"):
                        if line.startswith("[HOMEWORK FROM LAST SESSION]:"):
                            last_homework = line.replace("[HOMEWORK FROM LAST SESSION]:", "").strip()
                            print(f"✓ Loaded homework: {last_homework[:80]}")
                            break
            except (json.JSONDecodeError, AttributeError):
                pass
            break

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(
            min_silence_duration=2.0,   # Wait 2 seconds of silence before responding
            min_speech_duration=0.1,    # Minimum speech to register as talking
            activation_threshold=0.45,  # Slightly more sensitive to catch softer speech
        ),
    )

    assistant = Assistant(room=ctx.room, last_homework=last_homework)

    # Start HeyGen LiveAvatar BEFORE session.start so it can take over audio
    # output cleanly. Set DISABLE_AVATAR=1 to skip entirely (useful when the
    # LiveAvatar API is flaky — the connection drops kill the TTS pipeline).
    avatar_loaded = False
    avatar_id = os.environ.get("LIVEAVATAR_AVATAR_ID", "b8be7fb8-8784-4e58-91d5-e8b4666a0e3f")
    avatar_state = {
        "identities": set(),  # identities seen as the avatar (it may rejoin under a new id)
        "restarts": 0,
        "last_restart": 0.0,
        "max_restarts": 3,
        "cooldown": 30.0,
    }

    async def _start_avatar_once(label: str) -> bool:
        try:
            print(f"Starting HeyGen LiveAvatar ({label}, avatar_id={avatar_id})...", flush=True)
            before = set(ctx.room.remote_participants.keys())
            new_avatar = liveavatar.AvatarSession(avatar_id=avatar_id)
            await asyncio.wait_for(new_avatar.start(session, room=ctx.room), timeout=4.0)
            # Give the avatar 2s to register as a remote participant, then capture
            # its identity so the supervisor can watch for THIS specific drop.
            for _ in range(20):
                await asyncio.sleep(0.1)
                added = set(ctx.room.remote_participants.keys()) - before
                if added:
                    avatar_state["identities"].update(added)
                    print(f"✓ HeyGen LiveAvatar started ({label}) identity={added}", flush=True)
                    return True
            print(f"✓ HeyGen LiveAvatar started ({label}) — identity not yet observed", flush=True)
            return True
        except asyncio.TimeoutError:
            print(f"⚠ HeyGen {label} timed out after 4s", flush=True)
        except Exception as e:
            print(f"⚠ HeyGen {label} failed: {e}", flush=True)
        return False

    if os.environ.get("DISABLE_AVATAR") == "1":
        print("DISABLE_AVATAR=1, skipping LiveAvatar — audio-only mode")
    else:
        for attempt in range(2):
            if await _start_avatar_once(f"attempt {attempt + 1}"):
                avatar_loaded = True
                break
        if not avatar_loaded:
            print("  Continuing in audio-only mode...")

    # Supervisor: if the LiveAvatar participant disappears mid-call (the
    # provider's WebSocket drops), try to bring it back. Capped restart count
    # with cooldown so a dead provider doesn't get hammered.
    if avatar_loaded:
        async def _supervise_avatar():
            # Allow some grace for initial registration on slow links.
            await asyncio.sleep(5)
            while True:
                await asyncio.sleep(6)
                if not avatar_state["identities"]:
                    # We never captured an identity — fall back to count: if no
                    # new participant has been added beyond the human, treat
                    # avatar as gone after 30s.
                    continue
                still_present = any(
                    ident in ctx.room.remote_participants for ident in avatar_state["identities"]
                )
                if still_present:
                    continue
                if avatar_state["restarts"] >= avatar_state["max_restarts"]:
                    print("⚠ Avatar gone; max restarts reached — staying audio-only", flush=True)
                    return
                now = time.time()
                if now - avatar_state["last_restart"] < avatar_state["cooldown"]:
                    continue
                avatar_state["restarts"] += 1
                avatar_state["last_restart"] = now
                print(
                    f"⚠ Avatar disconnected; restart "
                    f"{avatar_state['restarts']}/{avatar_state['max_restarts']}",
                    flush=True,
                )
                await _start_avatar_once(f"restart {avatar_state['restarts']}")

        asyncio.create_task(_supervise_avatar())

    await session.start(
        room=ctx.room,
        agent=assistant,
    )

    # Listen for emotion + vitals data from frontend
    @ctx.room.on("data_received")
    def on_data_received(data_packet):
        try:
            payload = data_packet.data.decode("utf-8") if isinstance(data_packet.data, bytes) else str(data_packet.data)
            if data_packet.topic == "emotion_visual":
                emotion_data = json.loads(payload)
                dominant = emotion_data.get("dominantEmotion", "neutral")
                assistant._current_emotion = dominant
                top_emotions = emotion_data.get("topEmotions", [])
                if top_emotions:
                    emotions_str = ", ".join(f"{e['name']}({e['score']})" for e in top_emotions)
                    print(f"🎭 Emotion detected: {dominant} [{emotions_str}]")
            elif data_packet.topic == "rppg_vitals":
                vitals = json.loads(payload)
                assistant._current_bpm = vitals.get("bpm", 0)
                assistant._current_hrv = vitals.get("hrv", 0)
                assistant._stress_level = vitals.get("stressLevel", "low")
                print(f"💓 Vitals: BPM={vitals.get('bpm')} HRV={vitals.get('hrv')}ms Stress={vitals.get('stressLevel')}")
        except Exception as e:
            print(f"Failed to parse data: {e}")

    # Backend crisis keyword detection as a safety net
    @session.on("user_input_transcribed")
    def on_user_speech(ev):
        if not assistant._crisis_flagged and assistant.check_crisis_keywords(ev.transcript):
            print(f"⚠ Crisis keyword detected in speech: {ev.transcript[:100]}")
            asyncio.create_task(assistant._publish_crisis_alert("Crisis keywords detected in user speech"))
            session.generate_reply(
                instructions=(
                    "URGENT: The user may be in crisis. Respond with empathy and warmth. "
                    "Call the flag_crisis tool, then provide the Malaysian emergency contacts: "
                    "Befrienders KL: 03-7956 8145, Talian Kasih: 15999, Emergency: 999. "
                    "Do NOT do CBT. Just listen and support."
                )
            )

    if last_homework:
        await session.generate_reply(
            instructions=(
                "Say a super casual, short greeting like a friend would — like 'Hey! Good to see you again.' or 'Hi! How's it going?' "
                "Keep it to ONE short sentence. Then ask how their homework went. "
                "Do NOT say 'How are you feeling today?' — that's too formal. Speak english."
            )
        )
    else:
        await session.generate_reply(
            instructions=(
                "Say a super casual, short greeting like a friend would — like 'Hey! What's up?' or 'Hi there! How's your day going?' "
                "Keep it to ONE short sentence, then let them talk. "
                "Do NOT say 'How are you feeling today? Is there anything specific on your mind?' — that's too formal and scripted. Speak english."
            )
        )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        initialize_process_timeout=30.0,
        num_idle_processes=1,
    ))
