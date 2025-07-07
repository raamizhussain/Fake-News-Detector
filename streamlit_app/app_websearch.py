import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.ask_llm import ask_llm
from scripts.web_search import search_web

st.set_page_config(page_title="AI News Verifier")

st.title("🔎 Web-Verified News Checker")
st.markdown("Check if a news claim is true using web search + AI explanation.")

# User input
user_input = st.text_area("📝 Enter your news claim", height=150)

if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter a news claim.")
    else:
        with st.spinner("Searching the web and verifying..."):
            # 🔁 TEMP: Hardcoded dummy search result
            search_results = search_web(user_input, max_results=5)

            search_summary = "\n".join(search_results)


            # 🧠 Build prompt for LLM
            prompt = f"""
            Your job is to verify if this claim is true based on the search results below.
            Please return output in this exact format:

            VERDICT: TRUE or FALSE
            EXPLANATION: Your reasoning here.

            Search Results:
            {search_summary}

            Claim: '{user_input}'
            """.strip()


            # 💬 Ask the LLM
            response = ask_llm(prompt)

            # Extract verdict + explanation
            verdict_line = next((line for line in response.splitlines() if "VERDICT:" in line), "")
            verdict = verdict_line.replace("VERDICT:", "").strip().upper()

            if not verdict:
                st.error("❌ Could not extract a clear verdict from the AI response.")
                st.code(response)  # Show raw response for debugging
                st.stop()

            
            explanation_lines = [
                line for line in response.splitlines()
                if "EXPLANATION:" in line or ("VERDICT:" not in line and "Search Results:" not in line)
            ]
            explanation = "\n".join(explanation_lines).replace("EXPLANATION:", "").strip()

            keywords = ["confirmed", "reported", "according to", "officials", "news", "says", "crash", "incident"]
            verified_count = sum(any(kw.lower() in r.lower() for kw in keywords) for r in search_results)
            total_results = len(search_results)
            
            match_ratio = verified_count / total_results if total_results else 0

            if match_ratio >= 0.8:
                color = "success"
            elif match_ratio >= 0.5:
                color = "warning"
            else:
                color = "error"

            
            # 🧾 Display
            # Show result
            st.markdown(f"""### {'✅' if verdict == 'TRUE' else '❌'} The claim that _\"{user_input.strip()}\"_ is **{verdict}**""")

            st.markdown(explanation)
            label = "High" if match_ratio >= 0.8 else "Medium" if match_ratio >= 0.5 else "Low"
            st.markdown(f"### 🧠 Verification Strength: **{label} ({verified_count}/{total_results} sources matched)**")

            st.markdown(f"### :{color}[{verified_count} out of {total_results} sources matched]")
            st.progress(match_ratio)


            # Optional: show sources
            with st.expander("📚 View sources used"):
                for r in search_results:
                    st.markdown(f"- {r}")

            # st.success(explanation)
