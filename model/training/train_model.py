import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report
)


# ==========================================
# 1. LOAD SYNTHETIC DATASET
# ==========================================

file_path = (
    "dataset/synthetic/"
    "synthetic_mental_wellbeing_dataset.csv"
)

df = pd.read_csv(file_path)

print("Dataset shape:", df.shape)


# ==========================================
# 2. SEPARATE FEATURES AND TARGET
# ==========================================

target_column = "Risk_Level"

X = df.drop(columns=[target_column])

y = df[target_column]


print("\nTarget distribution:")
print(y.value_counts())


# ==========================================
# 3. IDENTIFY COLUMN TYPES
# ==========================================

categorical_features = [
    "Gender",
    "Occupation"
]

numerical_features = [
    column
    for column in X.columns
    if column not in categorical_features
]


print("\nCategorical features:")
print(categorical_features)

print("\nNumerical features:")
print(numerical_features)


# ==========================================
# 4. CREATE PREPROCESSING PIPELINE
# ==========================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),

        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )

    ]
)


# ==========================================
# 5. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 6. CREATE MODELS
# ==========================================

models = {

    "Logistic Regression": Pipeline([

        (
            "preprocessing",
            preprocessor
        ),

        (
            "model",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )

    ]),


    "Random Forest": Pipeline([

        (
            "preprocessing",
            preprocessor
        ),

        (
            "model",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight="balanced"
            )
        )

    ]),


    "SVM": Pipeline([

        (
            "preprocessing",
            preprocessor
        ),

        (
            "model",
            SVC(
                class_weight="balanced"
            )
        )

    ])

}


# ==========================================
# 7. TRAIN AND EVALUATE
# ==========================================

results = {}

trained_models = {}


for name, model in models.items():

    print("\n" + "=" * 60)

    print(name)

    print("=" * 60)


    # Train
    model.fit(
        X_train,
        y_train
    )


    # Predict
    y_pred = model.predict(
        X_test
    )


    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )


    results[name] = accuracy

    trained_models[name] = model


    print("\nAccuracy:", accuracy)


    print("\nClassification Report:")

    print(

        classification_report(

            y_test,

            y_pred,

            zero_division=0

        )

    )


# ==========================================
# 8. FIND BEST MODEL
# ==========================================

best_model_name = max(
    results,
    key=results.get
)

best_model = trained_models[
    best_model_name
]


print("\n" + "=" * 60)

print(
    "BEST MODEL:",
    best_model_name
)

print(
    "BEST ACCURACY:",
    results[best_model_name]
)

print("=" * 60)


# ==========================================
# 9. SAVE COMPLETE PIPELINE
# ==========================================

os.makedirs(
    "model/saved_models",
    exist_ok=True
)


model_path = (
    "model/saved_models/"
    "wellbeing_model.pkl"
)


joblib.dump(
    best_model,
    model_path
)


print("\nBest model pipeline saved successfully!")

print(
    "Saved to:",
    model_path
)