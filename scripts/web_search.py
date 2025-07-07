# scripts/web_search.py

from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

def search_web(query, max_results=5):
    api_key = os.getenv("SERPAPI_API_KEY")
    params = {
        "engine": "google",
        "q": query,
        "num": max_results,
        "api_key": api_key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []

    for result in results.get("organic_results", [])[:max_results]:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        snippets.append(f"{title} - {snippet} ({link})")

    return snippets
