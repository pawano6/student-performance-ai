
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_analysis(data):
    """
    Returns AI analysis text OR None if failed
    """

    prompt = f"""
    Analyze the student's academic performance.
    
    Student Details:
    - Gender: {data['gender']}
    - Background: {data['race']}
    - Parental Education: {data['parental']}
    - Lunch: {data['lunch']}
    - Test Preparation: {data['prep']}
    
    Scores:
    - Math: {data['math']}
    - Reading: {data['reading']}
    - Writing: {data['writing']}
    - Final Score: {data['final_score']}
    
    Insights:
    - Performance Level: {data['level']}
    - Risk Level: {data['risk']}
    - Weak Subject: {data['weak_subject']}
    
    Provide response STRICTLY in this format:
    
    ### 1. Performance Explanation
    ### 2. Key Weakness
    ### 3. Improvement Actions (3 points)
    ### 4. Motivation Tip
    
    Do NOT include:
    - Analyst name
    - Labels like "Status"
    - Any extra headings
    """

    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return None
