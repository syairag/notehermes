import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("DASHSCOPE_API_KEY").strip()

# Test Data
TEST_EMAIL = "From: Toby\nSubject: Urgent\nFinish PRD by Monday."

# Try Coding Endpoint
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

print(f"🧪 Testing with Key: {API_KEY[:10]}...")
print(f"🌐 URL: {BASE_URL}/chat/completions")

try:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        resp = client.post(
            "/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "glm-5",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        print(f"Status: {resp.status_code}")
        print(resp.text[:500])
except Exception as e:
    print(f"Error: {e}")
