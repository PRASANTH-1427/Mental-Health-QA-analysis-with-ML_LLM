##------------------------data_set_creation for PHQ-9----------------------------------

import pandas as pd
import numpy as np

def generate_dummy_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        answers = np.random.randint(0, 4, size=9)  # PHQ-9 answers: 0–3
        total_score = sum(answers)

        # Map total score to PHQ-9 depression categories
        if total_score <= 4:
            label = 0
        elif total_score <= 9:
            label = 1
        elif total_score <= 14:
            label = 2
        elif total_score <= 19:
            label = 3
        else:
            label = 4

        data.append(list(answers) + [label])

    # Create DataFrame
    df = pd.DataFrame(data, columns=[f"Q{i+1}" for i in range(9)] + ["label"])
    return df

# if __name__ == "__main__":
#     df = generate_dummy_data()
#     df.to_csv("phq9_dataset.csv", index=False)
#     print("✅ Dataset saved as phq9_dataset.csv")

##------------------------data_set_creation for GAD-7----------------------------------

import pandas as pd
import numpy as np

def generate_gad7_dummy_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        answers = np.random.randint(0, 4, size=7)  # GAD-7 answers: 0–3
        total_score = sum(answers)

        # Map total score to GAD-7 anxiety categories
        if total_score <= 4:
            label = 0  # Minimal anxiety
        elif total_score <= 9:
            label = 1  # Mild anxiety
        elif total_score <= 14:
            label = 2  # Moderate anxiety
        else:
            label = 3  # Severe anxiety

        data.append(list(answers) + [label])

    # Create DataFrame
    df = pd.DataFrame(data, columns=[f"Q{i+1}" for i in range(7)] + ["label"])
    return df

# if __name__ == "__main__":
#     df = generate_gad7_dummy_data()
#     df.to_csv("gad7_dataset.csv", index=False)
#     print("✅ Dataset saved as gad7_dataset.csv")


# # import pandas as pd

# # df= pd.read_csv(r"C:\Users\CVHS\vsprograms\mental-health\mental-health-local\src\dataset\phq9_dataset.csv")
# # print(df.head())