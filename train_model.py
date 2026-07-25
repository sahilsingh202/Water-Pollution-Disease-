from pathlib import Path
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "water_pollution_disease.csv"
MODEL_PATH = BASE_DIR / "water_disease_model.pkl"

if not CSV_PATH.exists():
    raise FileNotFoundError(
        "water_pollution_disease.csv was not found. Put the dataset in the same folder as train_model.py."
    )

df = pd.read_csv(CSV_PATH)

# Same target logic used in the project notebook.
bins = [-1, 150, 300, 501]
labels = ["Low", "Medium", "High"]
df["Diarrheal_Risk_Category"] = pd.cut(
    df["Diarrheal Cases per 100,000 people"],
    bins=bins,
    labels=labels,
    right=False,
)

# Remove rows outside the chosen bins, if any.
df = df.dropna(subset=["Diarrheal_Risk_Category"]).copy()

target = "Diarrheal_Risk_Category"
X = df.drop(columns=["Diarrheal Cases per 100,000 people", target])
y = df[target].astype(str)

categorical_columns = X.select_dtypes(include=["object", "category"]).columns.tolist()
numeric_columns = [c for c in X.columns if c not in categorical_columns]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_columns),
    ("categorical", categorical_pipeline, categorical_columns),
])

# Decision Tree is used because the notebook's final explanation selects it as the final model.
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", DecisionTreeClassifier(random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Test Accuracy:", round(accuracy_score(y_test, pred), 4))
print(classification_report(y_test, pred))

categorical_options = {}
for col in categorical_columns:
    values = X[col].dropna().astype(str).unique().tolist()
    categorical_options[col] = sorted(values)

joblib.dump(
    {
        "model": model,
        "feature_columns": X.columns.tolist(),
        "categorical_options": categorical_options,
    },
    MODEL_PATH,
)

print(f"Saved model to: {MODEL_PATH}")
