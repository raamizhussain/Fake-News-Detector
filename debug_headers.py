import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print("🔍 Debugging OpenRouter API headers...")
print(f"🔑 Using key: {api_key[:15]}...{api_key[-10:]}")

# Test different header combinations
test_cases = [
    {
        "name": "Basic Authorization",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    },
    {
        "name": "With HTTP-Referer",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501"
        }
    },
    {
        "name": "With X-Title",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "News Verifier"
        }
    },
    {
        "name": "With both HTTP-Referer and X-Title",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "News Verifier"
        }
    },
    {
        "name": "OpenRouter specific headers",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "News Verifier",
            "User-Agent": "News Verifier/1.0"
        }
    }
]

payload = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "user", "content": "Hello! Just testing."}
    ],
    "max_tokens": 50
}

for i, test_case in enumerate(test_cases):
    print(f"\n🧪 Test {i+1}: {test_case['name']}")
    print(f"📋 Headers: {json.dumps(test_case['headers'], indent=2)}")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=test_case['headers'],
            json=payload,
            timeout=30
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ SUCCESS! Response: {message}")
            print("🎉 This header combination works!")
            break
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Request failed: {e}")

# Additional test: Try a free model
print(f"\n🆓 Testing with a free model...")
free_payload = {
    "model": "microsoft/phi-3-mini-128k-instruct:free",
    "messages": [
        {"role": "user", "content": "Hello! Just testing."}
    ],
    "max_tokens": 50
}

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "News Verifier"
        },
        json=free_payload,
        timeout=30
    )
    
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content']
        print(f"✅ FREE MODEL SUCCESS! Response: {message}")
    else:
        print(f"❌ Free model also failed: {response.status_code}")
        print(f"❌ Response: {response.text}")
        
except Exception as e:
    print(f"❌ Free model test failed: {e}")

print("\n🔧 Next steps:")
print("1. If none of the tests work, your API key might need credits")
print("2. Check your OpenRouter dashboard for usage limits")
print("3. Try regenerating your API key")
print("4. Some models might require payment even with valid keys")