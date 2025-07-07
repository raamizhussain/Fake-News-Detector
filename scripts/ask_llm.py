from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env file
load_dotenv()
print("✅ API Key:", os.getenv("OPENAI_API_KEY"))

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 👈 This must match your .env variable
    base_url="https://openrouter.ai/api/v1"
)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who verifies news based on search results and explains clearly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
