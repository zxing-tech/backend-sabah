"""Test script to verify all agent components can initialize without timing out."""

import asyncio
import os
from dotenv import load_dotenv
from livekit.plugins import google, cartesia, deepgram, silero, noise_cancellation

load_dotenv()

async def test_components():
    print("Testing component initialization...")

    try:
        print("  1. Testing Deepgram STT...")
        stt = deepgram.STT(model="nova-3", language="multi")
        print("     ✓ Deepgram STT initialized")
    except Exception as e:
        print(f"     ✗ Deepgram STT failed: {e}")
        return False

    try:
        print("  2. Testing Google LLM...")
        llm = google.LLM(model="gemini-1.5-flash")
        print("     ✓ Google LLM initialized")
    except Exception as e:
        print(f"     ✗ Google LLM failed: {e}")
        return False

    try:
        print("  3. Testing Cartesia TTS...")
        tts = cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02")
        print("     ✓ Cartesia TTS initialized")
    except Exception as e:
        print(f"     ✗ Cartesia TTS failed: {e}")
        return False

    try:
        print("  4. Testing Silero VAD...")
        vad = silero.VAD.load()
        print("     ✓ Silero VAD loaded")
    except Exception as e:
        print(f"     ✗ Silero VAD failed: {e}")
        return False

    try:
        print("  5. Testing BVC Noise Cancellation...")
        nc = noise_cancellation.BVC()
        print("     ✓ BVC Noise Cancellation initialized")
    except Exception as e:
        print(f"     ✗ BVC Noise Cancellation failed: {e}")
        return False

    print("\n✓ All components initialized successfully!")
    return True

if __name__ == "__main__":
    result = asyncio.run(test_components())
    exit(0 if result else 1)
