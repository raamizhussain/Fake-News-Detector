from dotenv import load_dotenv
import os
# from openai import OpenAI
import httpx


# Load .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

print("✅ Loaded API Key:", f"{api_key[:15]}...{api_key[-10:]}")

# Create OpenAI client for OpenRouter
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     default_headers={
#         "Authorization": f"Bearer {api_key}",
#         "HTTP-Referer": "http://localhost:8501",
#         "X-Title": "News Verifier"
#     }
# )

# def ask_llm(prompt):
#     # Try multiple models in order of preference
#     models_to_try = [
#         "mistralai/mistral-7b-instruct",
#         "mistralai/mistral-7b-instruct:free",
#         "microsoft/phi-3-mini-128k-instruct:free",
#         "meta-llama/llama-3.2-3b-instruct:free",
#         "google/gemma-7b-it:free"
#     ]
    
#     for model in models_to_try:
#         try:
#             print(f"🔄 Trying model: {model}")
#             response = client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant who verifies news based on search results and explains clearly."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=500
#             )
#             print(f"✅ Success with model: {model}")
#             return response.choices[0].message.content
#         except Exception as e:
#             print(f"❌ Failed with {model}: {e}")
#             continue
    
#     return "Error: Could not get response from any available AI model. Please check your API key and account status."
def ask_llm(prompt):
    models_to_try = [
        "mistralai/mistral-7b-instruct",
        "mistralai/mistral-7b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "google/gemma-7b-it:free"
    ]

    for model in models_to_try:
        try:
            print(f"🔄 Trying model: {model}")
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "News Verifier",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant who verifies news based on search results and explains clearly."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500
                },
                timeout=30.0
            )

            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                print(f"✅ Success with model: {model}")
                return content
            else:
                print(f"❌ Failed with {model}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception with {model}: {e}")
    
    return "Error: Could not get response from any available AI model. Please check your API key and account status."


# Test function
if __name__ == "__main__":
    test_prompt = "Hello! Please respond with a simple greeting."
    result = ask_llm(test_prompt)
    print(f"\n✅ Final result: {result}")
    
def format_search_results(results):
    formatted = []
    for r in results:
        try:
            # Try to split title, snippet, and link from existing format
            if " - " in r and "(" in r and r.endswith(")"):
                title_snippet, link = r.rsplit("(", 1)
                title, snippet = title_snippet.split(" - ", 1)
                link = link.rstrip(")")
                formatted.append(f"- **{title.strip()}**: {snippet.strip()} ({link.strip()})")
            else:
                formatted.append(f"- {r}")
        except:
            formatted.append(f"- {r}")
    return "\n".join(formatted)


def ask_llm_with_web(claim, search_results):
    formatted_results = format_search_results(search_results)

    prompt = f"""
    Your job is to verify if this claim is true based on the search results below.
    Please return output in this exact format:

    VERDICT: TRUE or FALSE
    EXPLANATION: Your reasoning here.

    Search Results:
    {formatted_results}

    Claim: '{claim}'
    """.strip()

    return ask_llm(prompt)
