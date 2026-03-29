import streamlit as st
import numpy as np
import pandas as pd
import time
from google import genai

# ✅ Import from your modules
from util import load_data
from model import train_model

# 🔑 Add your API Key
client = genai.Client(api_key="ENTER_YOUR_API_KEY_HERE")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student Performance AI", page_icon="🎓")

# ---------- TITLE ----------
st.title("🎓 Student Performance AI App")
st.write("Predict student performance and get AI-powered insights")

# ---------- LOAD DATA (CACHED) ----------
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ---------- TRAIN MODEL (CACHED) ----------
@st.cache_resource
def get_model(data):
    return train_model(data)

model, mae = get_model(df)

# ---------- OPTIONAL UI ----------
if st.checkbox("📂 Show Dataset Preview"):
    st.dataframe(df.head())

if st.checkbox("📊 Show Model Info"):
    st.write("Model: Linear Regression")
    

# ---------- INPUT FORM ----------
st.header("📥 Enter Student Scores")

with st.form("input_form"):

    math = st.number_input(
        "Math Score", min_value=0, max_value=100,
        value=None, placeholder="Enter Math Score"
    )
    reading = st.number_input(
        "Reading Score", min_value=0, max_value=100,
        value=None, placeholder="Enter Reading Score"
    )
    writing = st.number_input(
        "Writing Score", min_value=0, max_value=100,
        value=None, placeholder="Enter Writing Score"
    )

    submit = st.form_submit_button("🚀 Predict Performance")

# ---------- PREDICTION ----------
if submit:

    # ✅ Validation
    if math is None or reading is None or writing is None:
        st.warning("⚠️ Please enter all scores")
        st.stop()

    # ---------- DATASET INSIGHTS ----------
    st.subheader("📊 Dataset Insights")

    avg_score = df["average_score"].mean()

    st.write(f"Average Score: {avg_score:.2f}")
    st.write(f"Highest Score: {df['average_score'].max():.2f}")
    st.write(f"Lowest Score: {df['average_score'].min():.2f}")

    st.write(f"📉 Model MAE: {mae:.2f}")
    st.caption("MAE shows average prediction error (lower is better)")

    # ---------- PREDICTION ----------
    input_data = np.array([[math, reading, writing]])
    prediction = model.predict(input_data)[0]

    st.success(f"📊 Predicted Score: {prediction:.2f}")

    # ---------- PERFORMANCE LEVEL ----------
    if prediction >= 85:
        level = "Excellent"
    elif prediction >= 70:
        level = "Good"
    elif prediction >= 50:
        level = "Average"
    else:
        level = "Poor"

    st.write(f"🏷️ Performance Level: **{level}**")

    # ---------- CHART ----------
    st.subheader("📈 Subject-wise Scores")

    chart_data = pd.DataFrame({
        "Subjects": ["Math", "Reading", "Writing", "Average"],
        "Scores": [math, reading, writing, prediction]
    })

    st.bar_chart(chart_data.set_index("Subjects"))

    # ---------- WEAK SUBJECT ----------
    scores = {"Math": math, "Reading": reading, "Writing": writing}
    weak_subject = min(scores, key=scores.get)

    st.write(f"📉 Weakest Subject: **{weak_subject}**")

    # ---------- AI ANALYSIS (CACHED) ----------
    st.subheader("🤖 AI Performance Analysis")

    cache_key = f"{math}-{reading}-{writing}"

    if "ai_cache" not in st.session_state:
        st.session_state.ai_cache = {}

    # ✅ Use cache (no API call)
    if cache_key in st.session_state.ai_cache:
        st.success("⚡ Loaded from cache (no API used)")
        st.write(st.session_state.ai_cache[cache_key])

    else:
        prompt = f"""
        Student Scores:
        Math: {math}, Reading: {reading}, Writing: {writing}
        Predicted Score: {prediction:.2f}

        Explain performance in simple terms.
        Suggest 2-3 improvements.
        """

        try:
            with st.spinner("Analyzing with AI..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )

                ai_text = response.text

                # Save response
                st.session_state.ai_cache[cache_key] = ai_text

                st.success("✅ AI Response")
                st.write(ai_text)

        except Exception:
            st.info("ℹ️ AI temporarily unavailable. Showing basic analysis.")

            if prediction >= 85:
                fallback = "Excellent performance. Keep it up!"
            elif prediction >= 70:
                fallback = "Good performance. Practice more."
            elif prediction >= 50:
                fallback = "Average performance. Focus on weak areas."
            else:
                fallback = "Needs improvement. Work on basics."

            st.write(fallback)

    # ---------- DOWNLOAD REPORT ----------
    report = f"""
Student Performance Report

Math: {math}
Reading: {reading}
Writing: {writing}

Predicted Score: {prediction:.2f}
Performance Level: {level}
Weakest Subject: {weak_subject}
"""

    st.download_button("📥 Download Report", report)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built using Streamlit + Machine Learning + Generative AI")