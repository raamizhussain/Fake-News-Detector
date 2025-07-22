from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "Authorization": "Bearer sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
)

response = client.models.list()
print("✅ Available models:", [m.id for m in response.data])