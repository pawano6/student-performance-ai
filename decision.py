def analyze_performance(final_score, weak_subject):

    # -----------------------------
    # Performance Level + Risk
    # -----------------------------
    if final_score >= 85:
        level = "Excellent"
        risk = "Low"

    elif final_score >= 70:
        level = "Good"
        risk = "Medium"

    elif final_score >= 50:
        level = "Average"
        risk = "High"

    else:
        level = "Poor"
        risk = "Very High"

    # -----------------------------
    # Weakness-Based Suggestion
    # -----------------------------
    if weak_subject == "Math":
        suggestion = "Focus on problem-solving practice and formulas."

    elif weak_subject == "Reading":
        suggestion = "Improve reading comprehension and speed."

    else:
        suggestion = "Work on writing structure and grammar."

    # -----------------------------
    # Final Recommendation
    # -----------------------------
    recommendation = f"{suggestion} Maintain consistent study habits."

    return level, risk, recommendation