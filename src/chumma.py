# def map_predictions_to_labels(results):
#     phq9_mapping = {
#         0: "Minimal depression",
#         1: "Mild depression",
#         2: "Moderate depression",
#         3: "Moderately severe depression",
#         4: "Severe depression"
#     }

#     gad7_mapping = {
#         0: "Minimal anxiety",
#         1: "Mild anxiety",
#         2: "Moderate anxiety",
#         3: "Severe anxiety"
#     }

#     readable_results = {
#         "PHQ-9": {model: phq9_mapping.get(score, "Unknown") for model, score in results.get("PHQ-9", {}).items()},
#         "GAD-7": {model: gad7_mapping.get(score, "Unknown") for model, score in results.get("GAD-7", {}).items()},
#     }

#     return readable_results


# result= {'PHQ-9': {'RandomForest': 1, 'LogisticRegression': 1, 'XGBoost': 1}, 'GAD-7': {'RandomForest': 1, 'LogisticRegression': 0, 'XGBoost': 0}}
# a= map_predictions_to_labels(result)
# print("a:- ", a)




import streamlit as st
import json
import os
import datetime
from src.ML_Model.load_ml_model import load_models_and_predict
from src.LLM_Model.mistral_qroq import model_call

# Load questionnaire data from JSON file
def load_questionnaire(file_path):
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found.")
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Generic scoring for PHQ-9 and GAD-7
def calculate_score(answers, questionnaire):
    option_to_score = {opt: i for i, opt in enumerate(questionnaire["options"])}
    return sum(option_to_score.get(answers.get(q["key"], ""), 0) for q in questionnaire["questions"])

# Scoring for BDI-II
def calculate_bdi_ii_score(answers, questionnaire):
    score = 0
    for q in questionnaire["questions"]:
        selected = answers.get(q["key"], "")
        try:
            score += q["options"].index(selected)
        except ValueError:
            continue
    return score

# Render a single questionnaire
def render_questionnaire(questionnaire, answers):
    st.subheader(questionnaire["title"])
    for q in questionnaire["questions"]:
        key = q["key"]
        opts = q.get("options", questionnaire.get("options", []))
        answers[key] = st.radio(q["text"], opts, key=key, index=None)

# Check if all questions are answered
def all_answered(questionnaire, answers):
    return all(answers.get(q["key"], None) for q in questionnaire["questions"])

# Collect structured answers by questionnaire
def collect_structured_answers(questionnaire_data, user_answers):
    structured = {}
    for q_key, q_info in questionnaire_data.items():
        section_answers = {}
        for q in q_info["questions"]:
            question_text = q["text"]
            selected_answer = user_answers.get(q["key"], None)
            if selected_answer is not None:
                section_answers[question_text] = selected_answer
        structured[q_key] = section_answers
    return structured


# Main app logic
def main():
    st.title("Mental Health Questionnaire")

    questionnaire_data = load_questionnaire(r"C:\Users\CVHS\vsprograms\mental-health\mental-health-local\questions\full_question_2type.json")
    questionnaire_keys = list(questionnaire_data.keys())

    if not questionnaire_keys:
        st.warning("No questionnaires available to display.")
        return

    if "step" not in st.session_state:
        st.session_state.step = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Handle out-of-range index
    if st.session_state.step >= len(questionnaire_keys):
        st.session_state.step = 0

    current_form_key = questionnaire_keys[st.session_state.step]
    current_questionnaire = questionnaire_data[current_form_key]

    render_questionnaire(current_questionnaire, st.session_state.user_answers)

    if all_answered(current_questionnaire, st.session_state.user_answers):
        if st.session_state.step < len(questionnaire_keys) - 1:
            if st.button("Next"):
                st.session_state.step += 1
                st.rerun()  
        else:
            if st.button("Submit"):
                st.success("Thank you for completing the questionnaires!")
                st.markdown("### Scores:")
                if "PHQ-9" in questionnaire_data:
                    phq_score = calculate_score(st.session_state.user_answers, questionnaire_data["PHQ-9"])
                    st.write(f"**PHQ-9 Score:** {phq_score}")
                if "GAD-7" in questionnaire_data:
                    gad_score = calculate_score(st.session_state.user_answers, questionnaire_data["GAD-7"])
                    st.write(f"**GAD-7 Score:** {gad_score}")

                st.markdown("### Collected Answers:")
                structured_answers = collect_structured_answers(questionnaire_data, st.session_state.user_answers)
                st.json(structured_answers)

                ml_result = load_models_and_predict(structured_answers)
                llm_result = model_call(structured_answers)

    else:
        st.info("Please answer all the questions to proceed.")

if __name__ == "__main__":
    main()
