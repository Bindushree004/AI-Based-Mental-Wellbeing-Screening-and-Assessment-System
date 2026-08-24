import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

DATASET_PATH = (
    "dataset/synthetic/"
    "synthetic_mental_wellbeing_dataset.csv"
)

df = pd.read_csv(DATASET_PATH)


# ==========================================
# 2. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["Risk_Level"])

y = df["Risk_Level"]


# ==========================================
# 3. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. LOAD SAVED BEST MODEL
# ==========================================

MODEL_PATH = (
    "model/saved_models/"
    "wellbeing_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ==========================================
# 5. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 6. CALCULATE METRICS
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

print("\n" + "=" * 60)

print("MODEL EVALUATION")

print("=" * 60)

print("\nAccuracy:")
print(round(accuracy, 4))

print("\nPrecision:")
print(round(precision, 4))

print("\nRecall:")
print(round(recall, 4))

print("\nF1-Score:")
print(round(f1, 4))


# ==========================================
# 8. CLASSIFICATION REPORT
# ==========================================

print("\n" + "=" * 60)

print("CLASSIFICATION REPORT")

print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# 9. CONFUSION MATRIX
# ==========================================

print("\n" + "=" * 60)

print("CONFUSION MATRIX")

print("=" * 60)

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)