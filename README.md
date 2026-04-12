# 🎓 Student Performance AI System

A full-stack AI-powered web application that predicts student performance, provides intelligent insights, and stores real-world prediction data.

---

## 🚀 Features

- 📊 Predicts student performance using Machine Learning
- 📈 Visualizes subject-wise scores (bar chart)
- 📉 Identifies weakest subject
- 🧠 Decision Analysis (Performance Level + Risk + Recommendation)
- 🤖 AI-generated insights using Generative AI
- ⚡ Smart caching (fast performance, reduced API cost)
- 🛡️ Fallback system if AI fails
- 📥 Downloadable HTML performance report
- 🗄️ Stores prediction data in cloud database (Railway MySQL)
- 📊 Dashboard to view historical predictions
- 🔌 FastAPI backend for API access

---

## 🧠 Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### Machine Learning
- Scikit-learn (Random Forest / Regression)

### Data Processing
- Pandas, NumPy

### Visualization
- Matplotlib

### AI Integration
- Google Generative AI (Gemini)

### Database
- MySQL (Railway Cloud DB)

---


## 📂 Project Structure

Student_Performance_Analysis/

│

├── app.py # Streamlit frontend

├── api.py # FastAPI backend

├── model.py # ML model logic

├── util.py # Data processing

├── decision.py # Performance logic

├── ai_module.py # AI integration

├── database.py # DB operations

├── requirements.txt

├── .env # Environment variables (not pushed)



---


## 📊 How It Works

1. User enters student details
2. ML model predicts writing & final score
3. Decision engine determines:
   - Performance Level
   - Risk Level
4. AI generates insights
5. Data is stored in MySQL database
6. Dashboard shows historical analytics

---


## 🛡️ Error Handling & Optimization

- Input validation
- AI fallback system
- Session-based caching
- Streamlit caching for model & data

---


## ▶️ Run Locally

bash

git clone https://github.com/pawano6/student-performance-ai.git

cd student-performance-ai

pip install -r requirements.txt

streamlit run app.py



🔌 Run API

python -m uvicorn api:app --reload

Open:

👉 http://127.0.0.1:8000/docs


🌐 Environment Variables (.env)

MYSQLHOST=your_host

MYSQLUSER=your_user

MYSQLPASSWORD=your_password

MYSQLDATABASE=your_db

MYSQLPORT=your_port

GEMINI_API_KEY=your_api_key


🚀 Future Improvements

Deploy full system (frontend + backend)

Add authentication (login system)

Add more ML features

Use advanced models (XGBoost, Deep Learning)

Add real-time analytics dashboard


👨‍💻 Author

Pawan Singh


⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
