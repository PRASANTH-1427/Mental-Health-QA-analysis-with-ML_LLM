import os
import joblib
import numpy as np
import time

# Answer-to-score mapping
score_map = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

# PHQ-9 question order
phq9_questions = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself—or that you are a failure or have let yourself or your family down",
    "Trouble concentrating on things, such as reading the newspaper or watching television",
    "Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you have been moving around a lot more than usual",
    "Thoughts that you would be better off dead or of hurting yourself in some way"
]

# GAD-7 question order
gad7_questions = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it's hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen"
]

phq9_score_mapping = {
    0: "Minimal depression",
    1: "Mild depression",
    2: "Moderate depression",
    3: "Moderately severe depression",
    4: "Severe depression"
}

gad7_score_mapping = {
    0: "Minimal anxiety",
    1: "Mild anxiety",
    2: "Moderate anxiety",
    3: "Severe anxiety"
}

def preprocess_section(data, section):
    try:
        question_list = phq9_questions if section == "PHQ-9" else gad7_questions
        scores = [score_map.get(data.get(q, "Not at all"), 0) for q in question_list]
        return np.array(scores).reshape(1, -1)
    except Exception as e:
        print(f"Preprocessing error in section '{section}': {str(e)}")
        return np.zeros((1, len(phq9_questions) if section == "PHQ-9" else len(gad7_questions)))

def resolve_path_from_root(*relative_parts):
    """
    Resolves a path relative to the project root (the directory containing src).
    
    Example:
        resolve_path_from_root("saved_models", "PHQ-9_model.pkl")
    """
    # Get path to the current file (e.g., utils/paths.py)
    current_file = os.path.abspath(__file__)
    
    # Go up to project root — adjust levels if needed
    project_root = os.path.abspath(os.path.join(current_file, "..", ".."))
    print("project_root:- ",project_root)
    return os.path.join(project_root, *relative_parts)

def load_models_and_predict(model_prefix, features):
    models = ["RandomForest", "LogisticRegression", "XGBoost"]
    results = {}

    for model_name in models:
        start_time = time.time()
        model_path = resolve_path_from_root("saved_models", f"{model_prefix}_{model_name}_model.pkl")
        try:
            print("model_path :-",model_path)
            model = joblib.load(model_path)
            pred = model.predict(features)[0]
            print(f"{model_prefix} - {model_name} prediction: {int(pred)} | Time: {round(time.time() - start_time, 4)} sec")
            results[model_name] = int(pred)
        except Exception as e:
            print(f"Error with {model_prefix} - {model_name}: {str(e)} | Time: {round(time.time() - start_time, 4)} sec")
            results[model_name] = None

    return results

def get_inference(user_input):
    total_start = time.time()
    final_results = {}

    for section in ["PHQ-9", "GAD-7"]:
        if section in user_input:
            try:
                print(f"\n--- Starting inference for {section} ---")
                features = preprocess_section(user_input[section], section)
                model_results = load_models_and_predict(section, features)
                final_results[section] = model_results
            except Exception as e:
                print(f"Error in section {section}: {str(e)}")

    print('Raw results from model:- ',final_results)    

    readable_results = {
        "PHQ-9": {model: phq9_score_mapping.get(score, "Unknown") for model, score in final_results.get("PHQ-9", {}).items()},
        "GAD-7": {model: gad7_score_mapping.get(score, "Unknown") for model, score in final_results.get("GAD-7", {}).items()},
    }

    print(f"\nTotal inference time: {round(time.time() - total_start, 4)} sec")
    return readable_results


##---------Example usage------------------
if __name__ == "__main__":
    user_input = {
        "PHQ-9": {
            "Little interest or pleasure in doing things": "Not at all",
            "Feeling down, depressed, or hopeless": "Not at all",
            "Trouble falling or staying asleep, or sleeping too much": "Not at all",
            "Feeling tired or having little energy": "Not at all",
            "Poor appetite or overeating": "Not at all",
            "Feeling bad about yourself—or that you are a failure or have let yourself or your family down": "Not at all",
            "Trouble concentrating on things, such as reading the newspaper or watching television": "Not at all",
            "Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you have been moving around a lot more than usual": "Not at all",
            "Thoughts that you would be better off dead or of hurting yourself in some way": "Nearly every day"
        },
        "GAD-7": {
            "Feeling nervous, anxious, or on edge": "Nearly every day",
            "Not being able to stop or control worrying": "Not at all",
            "Worrying too much about different things": "Not at all",
            "Trouble relaxing": "Not at all",
            "Being so restless that it's hard to sit still": "Not at all",
            "Becoming easily annoyed or irritable": "Not at all",
            "Feeling afraid as if something awful might happen": "Not at all"
        }
    }
    results = get_inference(user_input)
    print('results:- ',results)
    print('type of the results:- ',type(results))