# 🧠 Mental Health Assessment API

This project offers a simple backend API for assessing mental health using **PHQ-9** and **GAD-7** questionnaires. It combines traditional **ML models** with powerful **LLM-based insights** using Mistral-24B (via Groq API).

## 🚀 Features 

- ✅ Get PHQ-9 and GAD-7 questions
- ✅ Submit answers and receive confirmation
- ✅ Analyze answers using:
  - ML (RandomForest, XGBoost, LogisticRegression)
  - LLM (Mistral-24B via Groq)
- ✅ Ready to deploy (FastAPI + CORS)

---

## 📦 Setup Locally

```bash
# Clone this repo
git clone https://github.com/PRASANTH-1427/Mental-Health-QA-analysis-with-ML_LLM.git
cd mental-health-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key to a .env file
echo "API_KEY_GROQ=your_groq_api_key" > .env

# Run the app
uvicorn main:app --reload

---

🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/get-questions` | GET | Returns PHQ-9 and GAD-7 questions |
| `/submit-answers` | POST | Accepts answers and echoes back |
| `/analyze` | POST | Returns ML and LLM-based mental health insights |


📤 Deploying to Render
Push to GitHub

Go to Render

Create a new Web Service

Set:

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port 8000

Environment Variable: API_KEY_GROQ=your_api_key_here

🧠 Models Used

ML Models
Logistic Regression, XGBoost, Random Forest

Trained on vectorized PHQ-9 and GAD-7 answers

LLM
Mistral-24B via Groq

Provides reasoning, classification, tips, and recommendations

📬 Example Input to /analyze

{
  "PHQ_9": {
    "Little interest or pleasure in doing things": "Several days",
    "Feeling down, depressed, or hopeless": "Several days",
    "...": "..."
  },
  "GAD_7": {
    "Feeling nervous, anxious, or on edge": "Several days",
    "Not being able to stop or control worrying": "Several days",
    "...": "..."
  }
}

🙏 Credits
Developed using FastAPI, Groq API, and LangChain.

ML models trained offline using sklearn and joblib.