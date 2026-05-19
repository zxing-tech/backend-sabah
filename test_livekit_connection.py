#!/usr/bin/env python3
"""Test LiveKit connection and agent dispatch configuration"""
import os
import asyncio
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def test_livekit_connection():
    """Test if we can connect to LiveKit and check agent dispatch"""

    livekit_url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    print(f"LiveKit URL: {livekit_url}")
    print(f"API Key: {api_key}")

    # Create LiveKit API client
    lk_api = api.LiveKitAPI(
        url=livekit_url,
        api_key=api_key,
        api_secret=api_secret,
    )

    try:
        # List active rooms
        print("\n📋 Listing active rooms...")
        rooms = await lk_api.room.list_rooms()
        print(f"Found {len(rooms)} active rooms:")
        for room in rooms:
            print(f"  - {room.name} (participants: {room.num_participants})")

        # List agent dispatches (if available)
        print("\n🤖 Checking agent dispatch configuration...")
        try:
            # This may not be available in all LiveKit plans
            dispatches = await lk_api.agent_dispatch.list_dispatch()
            print(f"Found {len(dispatches)} dispatch rules")
        except Exception as e:
            print(f"⚠️  Cannot access agent dispatch configuration: {e}")
            print("   You may need to configure this in the LiveKit Cloud dashboard")

        print("\n✅ LiveKit connection successful!")

    except Exception as e:
        print(f"\n❌ Error connecting to LiveKit: {e}")

    finally:
        await lk_api.aclose()

if __name__ == "__main__":
    asyncio.run(test_livekit_connection())
