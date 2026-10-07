from pathlib import Path
import joblib


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "policy_stance_model.joblib"


# --------------------------------------------------
# 2. Load trained model
# --------------------------------------------------

model = joblib.load(MODEL_PATH)

print("PolicyPulse stance model loaded successfully.")


# --------------------------------------------------
# 3. Prediction loop
# --------------------------------------------------

while True:

    text = input("\nEnter a policy discussion (or 'exit' to quit): ")

    if text.strip().lower() == "exit":
        print("Exiting...")
        break

    if not text.strip():
        print("Please enter some text.")
        continue

    # Predict stance
    prediction = model.predict([text])[0]

    # Get probabilities
    probabilities = model.predict_proba([text])[0]

    classes = model.classes_

    print("\n-----------------------------")
    print("Discussion:")
    print(text)

    print("\nPredicted stance:", prediction)

    print("\nClass probabilities:")

    for label, probability in zip(classes, probabilities):
        print(f"{label}: {probability:.2%}")

    print("-----------------------------")