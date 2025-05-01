# import requests
# import time
# from dotenv import load_dotenv 
# import os
# from groq import Groq

# load_dotenv()  # take environment variables

# # Replace with your Groq API key
# groq_key = os.getenv("API_KEY_GROQ")

# def model_call(user_query):

#     start_time = time.time()  # Start Time Logging

#     try:
#         client = Groq(
#         # This is the default and can be omitted
#         api_key=groq_key,
#     )

#         prompt = f"""
#         You are a mental health assistant. The user will provide answers to two standard clinical assessments: **PHQ-9 (for depression)** and **GAD-7 (for anxiety)** in JSON format. Your job is to carefully read and interpret the responses, not just count scores.

#         Your response must contain:

#             1. **Classification** — For both PHQ-9 and GAD-7, classify the severity:
#             - PHQ-9: Minimal (0–4), Mild (5–9), Moderate (10–14), Moderately severe (15–19), Severe (20–27)
#             - GAD-7: Minimal (0–4), Mild (5–9), Moderate (10–14), Severe (15–21)

#             2. **Reasoning** — Explain your classification in detail. Analyze each question's meaning and the user’s answer. Identify any red flags, even if the total score is low. Pay special attention to questions about suicidal thoughts or excessive anxiety.

#             3. **Recommendation** — Suggest appropriate next steps based on the severity. Be cautious and responsible, especially if suicidal ideation or severe symptoms are present.

#             4. **Tips** — Give a few gentle, practical suggestions that can help the person feel supported. These may include lifestyle tips, stress relief techniques, or reminders to seek help.

#             Your tone should be **clinical but supportive** — kind, clear, and grounded in mental health best practices.

#         Here is the user’s response:

#         ```json
#         {user_query}

#         """

#         chat_completion = client.chat.completions.create(
#         messages=[
#                 {
#                     "role": "system",
#                     "content": prompt
#                 },

#             ],
#             # model="llama-3.3-70b-versatile",
#             model="mistral-saba-24b"
#         )

#         response = chat_completion.choices[0].message.content
#         print('raw response:- ',response)

#         end_time = time.time()  # End Time Logging
#         print(f"✅ Answered in {end_time - start_time:.2f} seconds.")

#         return response

#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error in Groq API Call: {e}")
#         return []
#     except Exception as e:
#         print(f"❌ Unexpected Error: {e}")
#         return []


##-----------------Json output parser----------------------

import requests
import time
from dotenv import load_dotenv
import os
from groq import Groq
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json

# Load environment variables
load_dotenv()
groq_key = os.getenv("API_KEY_GROQ")


# 1. Define expected structured output using Pydantic
class AssessmentOutput(BaseModel):
    classification: dict = Field(..., description="Severity classification for PHQ-9 and GAD-7")
    reasoning: dict = Field(..., description="Detailed reasoning behind the classification")
    recommendation: str = Field(..., description="Actionable advice based on the user's responses")
    tips: list[str] = Field(..., description="A few supportive or helpful tips for the user")


# 2. Initialize the parser
parser = PydanticOutputParser(pydantic_object=AssessmentOutput)


# 3. Function to make the model call
def model_call(user_query):
    start_time = time.time()

    try:
        client = Groq(api_key=groq_key)

        # Get format instructions from parser
        format_instructions = parser.get_format_instructions()

        # Prompt with format instructions
#         prompt = f"""
# You are a mental health assistant. The user will provide answers to two standard clinical assessments: **PHQ-9 (for depression)** and **GAD-7 (for anxiety)** in JSON format. Your job is to carefully read and interpret the responses, not just count scores.

# Your response must contain:

#     1. classification — a dictionary of severity levels for PHQ-9 and GAD-7.
#     2. reasoning — explanation of classification using detailed analysis of each response.
#     3. recommendation — clinical guidance on what action should be taken.
#     4. tips — a short list of kind and helpful advice for the person.

#     Your tone should be **clinical but supportive** — kind, clear, and grounded in mental health best practices.

# You must format your response as JSON like this:
#     {format_instructions}

# Here is the user’s response:

# {user_query}

# """
        prompt = f"""
You are a mental health assistant. The user will provide answers to two standard clinical assessments: **PHQ-9 (for depression)** and **GAD-7 (for anxiety)** in JSON format.

Your job is to carefully read and interpret the responses, not just count scores.

Speak directly to the person by using **"you" instead of "the user"** when referring to their responses or mental health condition.

Your response must contain:

1. **Classification** — For both PHQ-9 and GAD-7, classify the severity:
- PHQ-9: Minimal (0–4), Mild (5–9), Moderate (10–14), Moderately severe (15–19), Severe (20–27)
- GAD-7: Minimal (0–4), Mild (5–9), Moderate (10–14), Severe (15–21)

2. **Reasoning** — Explain your classification in detail. Analyze each question's meaning and the user’s answer. Identify any red flags, even if the total score is low. Pay special attention to questions about suicidal thoughts or excessive anxiety.

3. **Recommendation** — Suggest appropriate next steps based on the severity. Be cautious and responsible, especially if suicidal ideation or severe symptoms are present.

4. **Tips** — Give a few gentle, practical suggestions that can help the person feel supported. These may include lifestyle tips, stress relief techniques, or reminders to seek help.

Your tone should be **clinical but supportive** — kind, clear, and grounded in mental health best practices.


You must format your response as JSON like this:
    {format_instructions}

Here is the user’s response:

{user_query}

"""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt}
            ],
            model="mistral-saba-24b"  # or your preferred model
        )

        raw_response = chat_completion.choices[0].message.content
        print("Raw response:\n", raw_response)

        # 4. Parse output using LangChain's structured output parser
        parsed_output = parser.parse(raw_response)
        end_time = time.time()
        print(f"\n✅ Answered in {end_time - start_time:.2f} seconds.\n")

        # Print nicely formatted JSON
        print("Parsed Output:\n", json.dumps(parsed_output.dict(), indent=2))
        final_result = parsed_output.dict()
        return final_result

    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")




## Example Usage
if __name__ == "__main__":
    user_input ={
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
    result = model_call(user_query=json.dumps(user_input))
    print('result:- ',result)
    print('result type:-', type(result))


