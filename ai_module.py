
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_analysis(data):
    """
    Returns AI analysis text OR None if failed
    """

    prompt = f"""
    You are an academic performance analyst.

    Student Profile:
    - Gender: {data['gender']}
    - Background: {data['race']}
    - Parental Education: {data['parental']}
    - Lunch: {data['lunch']}
    - Test Prep: {data['prep']}

    Scores:
    - Math: {data['math']}
    - Reading: {data['reading']}
    - Writing (Predicted): {data['writing']}

    Final Score: {data['final_score']}

    Decision Insights:
    - Performance Level: {data['level']}
    - Risk Level: {data['risk']}
    - Weak Subject: {data['weak_subject']}

    Provide:
    1. Performance explanation
    2. Key weakness
    3. 3 improvement actions
    4. Motivation tip
    """

    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return None