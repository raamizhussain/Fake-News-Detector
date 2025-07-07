import streamlit as st
import pickle

# Load model and vectorizer
with open(r"G:\Learning\fake_news_detector\models\model_text.pkl", "rb") as f:
    model = pickle.load(f)

with open(r"G:\Learning\fake_news_detector\models\vectorizer_text.pkl", "rb") as f:
    vectorizer = pickle.load(f)
# Streamlit UI
st.title("🧠 Fake News Detector (Text Only)")
st.markdown("Enter a news headline or paragraph and check if it's real or fake.")

# Input
user_input = st.text_area("📝 Your News Text", height=200)

# Predict
if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)[0]

        if prediction == 0:
            st.error("🟥 This news is likely **FAKE** ❌")
        else:
            st.success("🟩 This news is likely **REAL** ✅")
