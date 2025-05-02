
import time
import streamlit as st
import requests

# backend_url = "https://mental-health-qa-analysis-with-ml-llm.onrender.com"
backend_url = "http://localhost:8000"

# # Fetch questions from FastAPI
# @st.cache_data
# def get_questions():
#     try:
#         response = requests.get(f"{backend_url}/get-questions")
#         if response.status_code == 200:
#             return response.json()
#     except Exception as e:
#         st.error(f"❌ Error fetching questions: {e}")
#     return {}

@st.cache_data
def get_questions():
    retries = 5
    for attempt in range(retries):
        try:
            response = requests.get(f"{backend_url}/get-questions")
            if response.status_code == 200 and response.json():
                return response.json()
            else:
                time.sleep(2)  # Wait and retry
        except Exception as e:
            time.sleep(2)
    st.error("❌ Failed to fetch questions after multiple attempts.")
    return {}

questions = get_questions()

print("the questions:- ",questions)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

questionnaire_keys = list(questions.keys())

# Render questionnaire page-by-page
def render_questionnaire(section_key):
    st.subheader(section_key)
    section_questions = questions[section_key]
    for q in section_questions:
        st.session_state.answers[q] = st.radio(
            q,
            ["Not at all", "Several days", "More than half the days", "Nearly every day"],
            key=q,
            index=None
        )

def all_answered(section_key):
    return all(st.session_state.answers.get(q) for q in questions[section_key])

# App title
st.title("🧠 Mental Health Questionnaire")

# st.write("📦 Raw questions data:", questions)

# Step control
if not questionnaire_keys:
    st.warning("⚠️ No questionnaires available.")
else:
    current_key = questionnaire_keys[st.session_state.step]
    render_questionnaire(current_key)

    if all_answered(current_key):
        if st.session_state.step < len(questionnaire_keys) - 1:
            if st.button("Next"):
                st.session_state.step += 1
                st.rerun()
        else:
            if st.button("Submit"):
                st.success("✅ Thank you for completing the questionnaires!")

                # Group answers by questionnaire
                grouped_answers = {key: {q: st.session_state.answers[q] for q in questions[key]} for key in questionnaire_keys}
                print("grouped_answers:- ",grouped_answers)

                # Score calculation (frontend)
                def answer_to_score(ans):
                    mapping = {
                        "Not at all": 0,
                        "Several days": 1,
                        "More than half the days": 2,
                        "Nearly every day": 3
                    }
                    return mapping.get(ans, 0)

                scores = {
                    "PHQ-9": sum(answer_to_score(ans) for ans in grouped_answers.get("PHQ-9", {}).values()),
                    "GAD-7": sum(answer_to_score(ans) for ans in grouped_answers.get("GAD-7", {}).values())
                }

                # Analyze responses
                try:
                    analyze_resp = requests.post(f"{backend_url}/analyze", json=grouped_answers)
                    if analyze_resp.status_code == 200:
                        result = analyze_resp.json()

                        # Score Display
                        st.markdown("### 🧮 Scores")
                        col1, col2 = st.columns(2)
                        with col1:
                            phq_score = scores.get("PHQ-9", "N/A")
                            st.metric("PHQ-9 Score", phq_score)
                        with col2:
                            gad_score = scores.get("GAD-7", "N/A")
                            st.metric("GAD-7 Score", gad_score)

                        # ML Results
                        ml_results = result.get("ML_Results", {})
                        if ml_results:
                            st.markdown("### 🤖 ML Model Predictions")
                            for section, models in ml_results.items():
                                with st.expander(f"{section} Predictions"):
                                    for model, pred in models.items():
                                        st.write(f"**{model}:** {pred}")
                        else:
                            st.info("No ML results available.")

                        # LLM Insights
                        llm = result.get("LLM_Insights", {})
                        if llm:
                            st.markdown("### 💡 LLM Insights")

                            st.markdown("#### 🧠 Classification")
                            st.json(llm.get("classification", {}))

                            st.markdown("#### 🧩 Reasoning")
                            for key, text in llm.get("reasoning", {}).items():
                                st.markdown(f"**{key}**")
                                st.write(text)

                            st.markdown("#### 🩺 Recommendation")
                            st.info(llm.get("recommendation", "No recommendation provided."))

                            st.markdown("#### 🌿 Tips for You")
                            for tip in llm.get("tips", []):
                                st.markdown(f"- {tip}")
                        else:
                            st.warning("⚠️ No LLM insights available.")
                    else:
                        st.error("❌ Failed to analyze responses.")
                except Exception as e:
                    st.error(f"❌ Analysis error: {e}")
    else:
        st.info("Please answer all the questions to proceed.")
