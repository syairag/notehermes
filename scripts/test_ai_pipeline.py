import httpx
import json
import os
from dotenv import load_dotenv

# Load the real key
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
API_KEY = os.getenv("DASHSCOPE_API_KEY").strip()

# Use the working coding endpoint
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

# Test Data
TEST_EMAIL = """
From: Toby <toby@company.com>
Subject: Urgent Tasks for Next Week

Hi Tony,

Please finish the PRD for NoteHermes by Monday, April 27th. 
Also, tell the frontend team to start working on the login page immediately.
Don't forget to check the M365 connection issues reported by QA.
"""

SYSTEM_PROMPT = "You are an expert executive assistant. Extract actionable tasks from the email."
USER_PROMPT = f"""
Extract tasks from this email. Return ONLY a JSON list of objects with keys: title, due_date (YYYY-MM-DD), priority (high/medium/low), assignee.

Email Content:
{TEST_EMAIL}
"""

print("🚀 Running Full AI Pipeline Test...")
print("📡 Connecting to DashScope (coding endpoint)...")

try:
    with httpx.Client(base_url=BASE_URL, timeout=60.0) as client:
        resp = client.post(
            "/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "qwen3-coder-plus",  # Coding model
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT}
                ],
                "temperature": 0.1
            }
        )
        
        if resp.status_code == 200:
            data = resp.json()
            content = data['choices'][0]['message']['content']
            
            print("✅ AI Extraction Success!")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Parse JSON
            clean = content.replace("```json", "").replace("```", "").strip()
            tasks = json.loads(clean)
            
            print(f"\n🎉 Extracted {len(tasks)} Tasks:")
            for i, t in enumerate(tasks, 1):
                print(f"{i}. [📌 {t.get('priority')}] {t.get('title')} (To: {t.get('assignee')})")
                if t.get('due_date'): print(f"   📅 Due: {t.get('due_date')}")
                
        else:
            print(f"❌ API Error: {resp.status_code}")
            print(resp.text)
            
except Exception as e:
    print(f"❌ Request Failed: {e}")
