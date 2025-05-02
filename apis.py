from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from src.ML_Model.load_ml_model import phq9_questions, gad7_questions, get_inference
from src.LLM_Model.mistral_qroq import model_call

app = FastAPI()

# ✅ Add this route
@app.get("/")
def root():
    return {"message": "API is live and running on Render!"}


# Allow frontend (like Streamlit) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format for answers
class QARequest(BaseModel):
    PHQ_9: Dict[str, str]
    GAD_7: Dict[str, str]

# ========== API 1: Get Questions ==========
@app.get("/get-questions")
def get_questions():
    return {
        "PHQ-9": phq9_questions,
        "GAD-7": gad7_questions
    }

# ========== API 2: Submit Answers ==========
@app.post("/submit-answers")
def submit_answers(payload: QARequest):
    try:
        user_data = {
            "PHQ-9": payload.PHQ_9,
            "GAD-7": payload.GAD_7
        }
        return {
            "questions": user_data,
            "message": "Answers received. You can now analyze using ML or LLM."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing answers: {str(e)}")

# ========== API 3: Get Full Analysis ==========
@app.post("/analyze")
def analyze_answers(payload: QARequest):
    try:
        user_data = {
            "PHQ-9": payload.PHQ_9,
            "GAD-7": payload.GAD_7
        }

        ml_results = get_inference(user_data)
        llm_results = model_call(user_data)

        return {
            "ML_Results": ml_results,
            "LLM_Insights": llm_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apis:app", host="0.0.0.0", port=8000, reload=True)