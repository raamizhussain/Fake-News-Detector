import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print("🔍 Testing OpenRouter API key directly...")
print(f"🔑 Using key: {api_key[:15]}...{api_key[-10:]}")

# Test 1: Check if key is valid by calling OpenRouter's models endpoint
print("\n📋 Test 1: Checking available models...")
try:
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json()
        print(f"✅ Found {len(models.get('data', []))} models")
        # Check if our target model exists
        model_ids = [model['id'] for model in models.get('data', [])]
        if 'mistralai/mistral-7b-instruct' in model_ids:
            print("✅ Target model 'mistralai/mistral-7b-instruct' is available")
        else:
            print("⚠️  Target model 'mistralai/mistral-7b-instruct' not found")
            print("📝 Available Mistral models:")
            mistral_models = [m for m in model_ids if 'mistral' in m.lower()]
            for model in mistral_models[:5]:  # Show first 5
                print(f"   - {model}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"❌ Response: {response.text}")
except Exception as e:
    print(f"❌ Request failed: {e}")

# Test 2: Try a simple chat completion
print("\n💬 Test 2: Testing chat completion...")
try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "News Verifier Test"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": "Hello! Just testing the connection."}
            ],
            "max_tokens": 50
        }
    )
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content']
        print(f"✅ Response: {message}")
        print("🎉 API key is working!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"❌ Response: {response.text}")
except Exception as e:
    print(f"❌ Request failed: {e}")

# Test 3: Check account info
print("\n👤 Test 3: Checking account info...")
try:
    response = requests.get(
        "https://openrouter.ai/api/v1/auth/key",
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        info = response.json()
        print(f"✅ Account info: {info}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"❌ Response: {response.text}")
except Exception as e:
    print(f"❌ Request failed: {e}")

print("\n🔧 Troubleshooting tips:")
print("1. Check your OpenRouter dashboard: https://openrouter.ai/keys")
print("2. Make sure you have credits/usage remaining")
print("3. Verify the key hasn't expired")
print("4. Try regenerating the API key if needed")