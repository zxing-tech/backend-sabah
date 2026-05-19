#!/usr/bin/env python3
"""
Script to create a new Hedra avatar for real-time sessions
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEDRA_API_KEY = os.getenv("HEDRA_API_KEY")
HEDRA_API_BASE = "https://api.hedra.com/v1"

def create_avatar():
    """Create a new Hedra avatar for real-time sessions"""

    if not HEDRA_API_KEY:
        print("❌ Error: HEDRA_API_KEY not found in .env file")
        return None

    print("Creating new Hedra avatar...")
    print(f"API Key: {HEDRA_API_KEY[:20]}...")

    headers = {
        "X-API-KEY": HEDRA_API_KEY,
        "Content-Type": "application/json"
    }

    # Try to create a real-time avatar
    # This payload may need adjustment based on Hedra's actual API
    payload = {
        "type": "realtime",
        "name": "Theraverse Mental Health Support"
    }

    try:
        # First, let's list available avatars
        print("\n📋 Fetching existing avatars...")
        list_response = requests.get(
            f"{HEDRA_API_BASE}/avatars",
            headers=headers,
            timeout=30
        )

        print(f"Status: {list_response.status_code}")
        print(f"Response: {list_response.text}")

        if list_response.status_code == 200:
            avatars = list_response.json()
            print(f"\n✓ Found {len(avatars.get('avatars', []))} existing avatars")
            for avatar in avatars.get('avatars', []):
                print(f"  - ID: {avatar.get('id')}, Name: {avatar.get('name')}, Type: {avatar.get('type')}")

        # Now try to create a new avatar
        print("\n🎭 Creating new avatar...")
        create_response = requests.post(
            f"{HEDRA_API_BASE}/avatars",
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"Status: {create_response.status_code}")
        print(f"Response: {create_response.text}")

        if create_response.status_code in [200, 201]:
            avatar_data = create_response.json()
            avatar_id = avatar_data.get('id') or avatar_data.get('avatar_id')
            print(f"\n✅ Avatar created successfully!")
            print(f"Avatar ID: {avatar_id}")
            return avatar_id
        else:
            print(f"\n⚠️  Failed to create avatar: {create_response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API request failed: {e}")
        return None

if __name__ == "__main__":
    avatar_id = create_avatar()

    if avatar_id:
        print(f"\n🎉 Success! Use this avatar ID in your agent.py:")
        print(f'   avatar_id="{avatar_id}"')
    else:
        print("\n💡 Tip: You may need to create avatars through the Hedra dashboard first")
        print("   Visit: https://app.hedra.com")
