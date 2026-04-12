import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
from io import BytesIO
import base64
from database import create_table, insert_prediction, fetch_all

from util import load_data
from model import train_model, predict_scores
from decision import analyze_performance
from ai_module import generate_ai_analysis

# 🔑 API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- PAGE ----------
st.set_page_config(page_title="Student Performance AI", page_icon="🎓")

st.title("🎓 Student Performance AI App")
st.write("Predict student performance and get AI-powered insights")

if st.button("🧹 Clear All Data"):
    st.session_state.clear()
    st.rerun()
# ---------- LOAD DATA ----------
@st.cache_data
def get_data():
    return load_data()

df = get_data()

@st.cache_resource
def init_db():
    create_table()

init_db() 

@st.cache_resource
def get_model(data):
    return train_model(data)

model, mae, rmse, r2 = get_model(df)

if "saved" not in st.session_state:
    st.session_state.saved = False

# ---------- OPTIONAL ----------
if st.checkbox("📂 Show Data"):
    st.dataframe(df.head())

if st.checkbox("📊 Model Info"):
    st.write("Model: Random Forest")
    st.write(f"MAE: {mae:.2f}")
    st.write(f"RMSE: {rmse:.2f}")
    st.write(f"R2 Score: {r2:.2f}")
# ---------- INPUT ----------
st.header("📥 Enter Student Details")

with st.form("form"):

    math = st.number_input("Math Score", min_value=0, max_value=100, value=None, placeholder="Enter Math Score")
    reading = st.number_input("Reading Score", min_value=0, max_value=100, value=None, placeholder="Enter Reading Score")

    gender = st.selectbox("Gender", df["gender"].unique())
    race = st.selectbox("Race/Ethnicity", df["race/ethnicity"].unique())
    parental = st.selectbox("Parental Education", df["parental level of education"].unique())
    lunch = st.selectbox("Lunch Type", df["lunch"].unique())
    prep = st.selectbox("Test Preparation Course", df["test preparation course"].unique())

    submit = st.form_submit_button("🚀 Predict")
    
# ---------- PREDICTION ----------
if submit:
    st.session_state.saved = False

    if math is None or reading is None or math <= 0 or reading <= 0 :
        st.warning("⚠️ Please enter valid scores")
        st.stop()
    # Prepare input
    input_data = pd.DataFrame({
        "gender": [gender],
        "race/ethnicity": [race],
        "parental level of education": [parental],
        "lunch": [lunch],
        "test preparation course": [prep],
        "math score": [math],
        "reading score": [reading]
    })

    # Get predictions
    with st.spinner("Predicting..."):
        predicted_writing, final_score = predict_scores(model, input_data)

    st.toast("Prediction completed successfully 🎉")

    # ---------- OUTPUT ----------
    st.success(f"✍️ Predicted Writing Score: {predicted_writing:.2f}")
    st.success(f"📊 Final Score: {final_score:.2f}")
    st.divider()

    # ---------- CHART ----------
    chart_data = pd.DataFrame({
        "Subjects": ["Math", "Reading", "Writing (Pred)", "Final"],
        "Scores": [math, reading, predicted_writing, final_score]
    })

    st.subheader("📈 Subject-wise Scores")
    st.bar_chart(chart_data.set_index("Subjects"))
    # Create chart image for report
    fig, ax = plt.subplots()
    ax.bar(chart_data["Subjects"], chart_data["Scores"])
    ax.set_title("Student Performance")

    # Save image to memory
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    # Convert to base64
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    plt.close(fig)

    # ---------- WEAK SUBJECT ----------
    scores = {
        "Math": math,
        "Reading": reading,
        "Writing": predicted_writing
    }

    weak_subject = min(scores, key=scores.get)
    st.write(f"📉 Weakest Subject: **{weak_subject}**")
    st.divider()
    # ---------- PERFORMANCE LEVEL ----------
    level, risk, recommendation = analyze_performance(final_score, weak_subject)

    db_data = {
    "gender": gender,
    "race": race,
    "parental": parental,
    "lunch": lunch,
    "prep": prep,
    "math": math,
    "reading": reading,
    "writing": predicted_writing,
    "final_score": final_score,
    "level": level,
    "risk": risk,
    "weak_subject": weak_subject
    }

    if not st.session_state.saved:
        insert_prediction(db_data)
        st.session_state.saved = True

    st.subheader("📊 Decision Analysis")

    st.write(f"🏷️ Performance Level: **{level}**")
    st.write(f"⚠️ Risk Level: **{risk}**")
    st.write(f"💡 Recommendation: {recommendation}")

    
    # ---------- AI ANALYSIS WITH CACHE ----------
    
    st.subheader("🤖 AI Performance Analysis")

    # Create unique cache key
    cache_key = f"{gender}-{race}-{parental}-{lunch}-{prep}-{math}-{reading}-{final_score}"

    # Initialize session cache
    if "ai_cache" not in st.session_state:
        st.session_state.ai_cache = {}

    # Prepare AI input
    ai_data = {
        "gender": gender,
        "race": race,
        "parental": parental,
        "lunch": lunch,
        "prep": prep,
        "math": math,
        "reading": reading,
        "writing": round(predicted_writing, 2),
        "final_score": round(final_score, 2),
        "level": level,
        "risk": risk,
        "weak_subject": weak_subject
    }

    # ---------- CACHE CHECK ----------
    if cache_key in st.session_state.ai_cache:
        st.success("⚡ Loaded from cache (No API call)")
        ai_output = st.session_state.ai_cache[cache_key]
        st.write(ai_output)

    else:
        try:
            with st.spinner("Analyzing with AI..."):

                ai_output = generate_ai_analysis(ai_data)

                if ai_output:
                    # Save to cache
                    st.session_state.ai_cache[cache_key] = ai_output

                    st.success("✅ AI Analysis")
                    st.write(ai_output)

                else:
                    raise Exception("AI failed")

        except Exception:
            st.warning("⚠️ AI unavailable, showing fallback")

            # ---------- FALLBACK ----------
            if final_score >= 85:
                ai_output = "Excellent performance. Keep it up!"
            elif final_score >= 70:
                ai_output = "Good performance. Focus on improving weaker areas."
            elif final_score >= 50:
                ai_output = "Average performance. Regular practice is needed."
            else:
                ai_output = "Performance is below average. Focus on fundamentals."

            # Save fallback also in cache 
            st.session_state.ai_cache[cache_key] = ai_output

            st.write(ai_output)

    # ---------- DOWNLOAD REPORT ----------
    import markdown
    formatted_ai = markdown.markdown(ai_output)

    report = f"""
    <html>
    <head>
    <style>
    body {{
        font-family: Arial, sans-serif;
        padding: 20px;
    }}
    h2 {{
        color: #2c3e50;
    }}
    .section {{
        margin-bottom: 20px;
    }}
    .card {{
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
    }}
    </style>
    </head>
    
    <body>
    
    <h2>🎓 Student Performance Report</h2>
    
    <div class="section card">
    <h3>📊 Scores</h3>
    <ul>
    <li>Math: {math}</li>
    <li>Reading: {reading}</li>
    <li>Predicted Writing: {predicted_writing:.2f}</li>
    <li><b>Final Score: {final_score:.2f}</b></li>
    </ul>
    </div>
    
    <div class="section card">
    <h3>📊 Decision Analysis</h3>
    <ul>
    <li>Performance Level: {level}</li>
    <li>Risk Level: {risk}</li>
    <li>Recommendation: {recommendation}</li>
    </ul>
    </div>
    
    <div class="section card">
    <h3>📊 Performance Chart</h3>
    <img src="data:image/png;base64,{img_base64}" width="400"/>
    </div>
    
    <div class="section card">
    <h3>🤖 AI Analysis</h3>
    <p>{formatted_ai}</p>
    </div>
    
    <hr>
    <p style="text-align:center;">Generated by Student Performance AI</p>
    
    </body>
    </html>
    """

    st.download_button(
        "📥 Download Report",
        report,
        file_name="student_report.html",
        mime="text/html"
    )

    st.divider()

    # ---------- DASHBOARD ----------
st.markdown("---")
st.header("📊 Prediction History Dashboard")

if st.checkbox("📜 Show Prediction History"):

    data = fetch_all()

    if data:
        df_history = pd.DataFrame(data, columns=[
            "ID", "Gender", "Race", "Parental", "Lunch", "Prep",
            "Math", "Reading", "Writing", "Final Score",
            "Level", "Risk", "Weak Subject", "Timestamp"
        ])
        
        df_history["Timestamp"] = pd.to_datetime(df_history["Timestamp"])

        st.dataframe(df_history)
        st.subheader("📈 Performance Distribution")

        level_counts = df_history["Level"].value_counts().reset_index()
        level_counts.columns = ["Level", "Count"]
        st.bar_chart(level_counts.set_index("Level"))

        st.subheader("⚠️ Risk Distribution")

        risk_counts = df_history["Risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        st.bar_chart(risk_counts.set_index("Risk"))

        st.subheader("📊 Overall Stats")

        st.write(f"Average Final Score: {df_history['Final Score'].mean():.2f}")
        st.write(f"Highest Score: {df_history['Final Score'].max():.2f}")
        st.write(f"Lowest Score: {df_history['Final Score'].min():.2f}")

    else:
        st.info("No data available yet")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built using Streamlit + Machine Learning + Generative AI")
