# 🎓 Student Performance AI App

An interactive Machine Learning + AI-powered web application that predicts student performance and provides intelligent insights.

---

## 🚀 Features

- 📊 Predicts student average score using ML model
- 📈 Displays subject-wise performance visualization
- 📉 Identifies weakest subject
- 🧠 Provides performance level (Excellent / Good / Average / Poor)
- 🤖 AI-generated insights (using Generative AI)
- ⚡ Optimized with caching (fast execution)
- 🛡️ Fallback system when AI is unavailable
- 📥 Downloadable performance report

---

## 🧠 Tech Stack

- Python
- Streamlit (UI)
- Pandas & NumPy (Data Processing)
- Scikit-learn (Machine Learning)
- Google Generative AI (AI insights)

---

## 📂 Project Structure
Student_Performance_Analysis/
│
├── app.py # Main Streamlit App
├── model.py # ML model logic
├── util.py # Data processing
├── requirements.txt
├── data/
│ └── StudentsPerformance.csv


---

## 📊 Dataset

- Dataset: Students Performance Dataset
- Features:
  - Math Score
  - Reading Score
  - Writing Score
- Target:
  - Average Score (calculated)

---

## 🤖 Machine Learning Model

- Model Used: Linear Regression
- Input: Math, Reading, Writing scores
- Output: Predicted average score
- Evaluation Metric: MAE (Mean Absolute Error)

---

## ⚡ Optimization Techniques

- Used Streamlit caching:
  - `@st.cache_data` → for dataset
  - `@st.cache_resource` → for model
- AI response caching to avoid repeated API calls
- Reduced unnecessary computations

---

## 🛡️ Error Handling

- Retry mechanism for AI API
- Fallback logic when AI is unavailable
- Input validation for user entries

---

## ▶️ How to Run

1. Clone the repository:
git clone https://github.com/pawano6/student-performance-ai.git


2. Navigate to folder:

cd student-performance-ai


3. Install dependencies:

pip install -r requirements.txt


4. Run the app:

streamlit run app.py


---

## 🚀 Future Improvements

- Add more features (gender, parental education, etc.)
- Use advanced ML models (Random Forest, XGBoost)
- Deploy on cloud (Streamlit Cloud)
- Replace API with local AI model

---

## 💡 Author

Pawan Singh

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!