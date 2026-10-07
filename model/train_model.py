
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "twitter_airline_sentiment.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 2. Load the existing CSV
df = pd.read_csv(DATA_PATH)

# 3. Select input and target
df = df.dropna(subset=["text", "airline_sentiment"])

X = df["text"].astype(str)
y = df["airline_sentiment"]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Build the ML pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=20000,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

# 6. Train the model
print("Training model...")
model.fit(X_train, y_train)

# 7. Evaluate on unseen test data
y_pred = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["negative", "neutral", "positive"]
))

# 8. Save the trained pipeline
model_path = MODEL_DIR / "sentiment_model.joblib"
joblib.dump(model, model_path)

print(f"\nModel saved to: {model_path}")

# 9. Test a new tweet
sample = ["The flight was amazing and the staff were very helpful"]
prediction = model.predict(sample)[0]

print("\nSample tweet:", sample[0])
print("Predicted sentiment:", prediction)
