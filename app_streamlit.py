import streamlit as st
import json
import os
import datetime
from src.ML_Model.load_ml_model import get_inference
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

def resolve_path_from_root(*relative_parts):
    """
    Resolves a path relative to the project root (the directory containing src).
    
    Example:
        resolve_path_from_root("saved_models", "PHQ-9_model.pkl")
    """
    # Get path to the current file (e.g., utils/paths.py)
    current_file = os.path.abspath(__file__)
    
    # Go up to project root — adjust levels if needed
    project_root = os.path.abspath(os.path.join(current_file, ".."))
    print("project_root:- ",project_root)
    return os.path.join(project_root, *relative_parts)

# Main app logic
def main():
    st.title("Mental Health Questionnaire")

    model_path = resolve_path_from_root("questions", "full_question_2type.json")
    if model_path:
        # print("model_path :-",model_path)
        questionnaire_data = load_questionnaire(model_path)
        questionnaire_keys = list(questionnaire_data.keys())
    else:
        print('it came to else in the file path finding')
        questionnaire_data = load_questionnaire(r"questions\full_question_2type.json")
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
            # if st.button("Submit"):
            #     st.success("Thank you for completing the questionnaires!")
            #     st.markdown("### Scores:")
            #     if "PHQ-9" in questionnaire_data:
            #         phq_score = calculate_score(st.session_state.user_answers, questionnaire_data["PHQ-9"])
            #         st.write(f"**PHQ-9 Score:** {phq_score}")
            #     if "GAD-7" in questionnaire_data:
            #         gad_score = calculate_score(st.session_state.user_answers, questionnaire_data["GAD-7"])
            #         st.write(f"**GAD-7 Score:** {gad_score}")
            #     # if "BDI-II" in questionnaire_data:
            #     #     bdi_score = calculate_bdi_ii_score(st.session_state.user_answers, questionnaire_data["BDI-II"])
            #     #     st.write(f"**BDI-II Score:** {bdi_score}")

            #     st.markdown("### Collected Answers:")
            #     structured_answers = collect_structured_answers(questionnaire_data, st.session_state.user_answers)
            #     st.json(structured_answers)

            #     # Ensure folder exists
            #     os.makedirs("collected_QAs", exist_ok=True)

            #     # Create a timestamped filename
            #     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            #     filename = f"submission_{timestamp}.json"
            #     filepath = os.path.join("collected_QAs", filename)

            #     # Save structured answers
            #     with open(filepath, "w", encoding="utf-8") as f:
            #         json.dump(structured_answers, f, ensure_ascii=False, indent=4)

            #     st.success(f"Responses saved to '{filepath}'")

            #     ml_result = load_models_and_predict(structured_answers)
            #     llm_result = model_call(structured_answers)

            ##----------------------updated version-------------------

            if st.button("Submit"):
                st.success("✅ Thank you for completing the questionnaires!")

                # Display raw scores
                st.markdown("### 🧮 Scores")
                score_col1, score_col2 = st.columns(2)
                with score_col1:
                    if "PHQ-9" in questionnaire_data:
                        phq_score = calculate_score(st.session_state.user_answers, questionnaire_data["PHQ-9"])
                        st.metric("PHQ-9 Score", phq_score)
                with score_col2:
                    if "GAD-7" in questionnaire_data:
                        gad_score = calculate_score(st.session_state.user_answers, questionnaire_data["GAD-7"])
                        st.metric("GAD-7 Score", gad_score)

                # Show collected answers
                # st.markdown("### 📝 Your Responses")
                structured_answers = collect_structured_answers(questionnaire_data, st.session_state.user_answers)
                # st.json(structured_answers)

                # ML Model Results (Safe)
                try:
                    ml_result = get_inference(structured_answers)
                    st.markdown("### 🤖 ML Model Predictions")
                    for section, model_results in ml_result.items():
                        with st.expander(f"{section} Predictions"):
                            for model_name, prediction in model_results.items():
                                st.write(f"**{model_name}:** {prediction}")
                except Exception as e:
                    st.error(f"⚠️ ML Prediction Error: {e}")

                # LLM Model Results (Safe)
                try:
                    llm_result = model_call(structured_answers)
                    if llm_result:
                        st.markdown("### 💡 LLM Insights")

                        # Classification
                        st.markdown("#### 🧠 Classification")
                        st.write(llm_result.get("classification", {}))

                        # Reasoning
                        st.markdown("#### 🧩 Reasoning")
                        reasoning = llm_result.get("reasoning", {})
                        for key, text in reasoning.items():
                            st.markdown(f"**{key}**")
                            st.write(text)

                        # Recommendation
                        st.markdown("#### 🩺 Recommendation")
                        st.info(llm_result.get("recommendation", "No recommendation provided."))

                        # Tips
                        st.markdown("#### 🌿 Tips for You")
                        for tip in llm_result.get("tips", []):
                            st.markdown(f"- {tip}")
                    else:
                        st.warning("⚠️ LLM model returned no result.")
                except Exception as e:
                    st.error(f"❌ LLM Processing Error: {e}")


    else:
        st.info("Please answer all the questions to proceed.")

if __name__ == "__main__":
    main()
