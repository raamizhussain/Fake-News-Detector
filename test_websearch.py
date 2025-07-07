# test_websearch.py
from scripts.web_search import search_web

query = "Air India crash Ahmedabad 2025"
results = search_web(query)

print("\n".join(results))
