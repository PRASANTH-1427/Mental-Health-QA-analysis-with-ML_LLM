import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import time
import traceback

def train_model():
    try:
        start_time = time.time()
        print("🚀 Starting model training...")

        # Load data
        # df = pd.read_csv(r"C:\Users\CVHS\vsprograms\mental-health\mental-health-local\src\dataset\phq9_dataset.csv")
        df = pd.read_csv(r"C:\Users\CVHS\vsprograms\mental-health\mental-health-local\src\dataset\gad7_dataset.csv")
        X = df[[f"Q{i+1}" for i in range(7)]]
        y = df["label"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Models to train
        models = {
            "RandomForest": RandomForestClassifier(),
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
        }

        for name, model in models.items():
            print(f"\n🔍 Training {name}...")
            model_start_time = time.time()
            try:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                print(f"📊 {name} Classification Report:\n", classification_report(y_test, y_pred))

                # Save model
                joblib.dump(model, f"GAD-7_{name}_model.pkl")
                print(f"✅ {name} model saved as GAD-7_{name}_model.pkl")

                model_end_time = time.time()
                print(f"⏱️ {name} training time: {model_end_time - model_start_time:.2f} seconds")
            except Exception as e:
                print(f"❌ Error training {name}: {str(e)}")
                traceback.print_exc()

        total_time = time.time() - start_time
        print(f"\n✅ All model training complete. 🕒 Total time: {total_time:.2f} seconds")

    except Exception as e:
        print("❌ An unexpected error occurred during training:")
        traceback.print_exc()

if __name__ == "__main__":
    train_model()



