"""PerformPredict - Flask app that serves two pre-trained scikit-learn pipelines."""

import os
import warnings
from collections import UserList

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

warnings.filterwarnings("ignore")
BASE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- loading

def _compat_patch():
    """Some scikit-learn versions renamed an internal class that old pickles
    refer to. Only used when needed. Best fix: use the scikit-learn version
    you trained with (see requirements.txt)."""
    import sklearn.compose._column_transformer as ct
    if not hasattr(ct, "_RemainderColsList"):
        class _RemainderColsList(UserList):
            def __init__(self, columns=(), *a, **k):
                super().__init__(columns)
        ct._RemainderColsList = _RemainderColsList


def load_model(name):
    path = os.path.join(BASE, "models", name)
    try:
        return joblib.load(path)
    except AttributeError:
        _compat_patch()
        return joblib.load(path)


school_model = load_model("school_performance_model.pkl")
college_model = load_model("college_student_model.pkl")

app = Flask(__name__)

# Set your real address (or the CONTACT_EMAIL environment variable) to show it
# in the footer. If empty, no email is shown.

CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "")


@app.context_processor
def inject_contact():
    return {"contact_email": CONTACT_EMAIL}

# ------------------------------------------------------------ school setup

SCHOOL_FEATURES = list(school_model.feature_names_in_)
_school_enc = school_model.named_steps["preprocessor"].named_transformers_["encoder"]
_school_cat_cols = ["gender", "race/ethnicity", "parental level of education",
                    "lunch", "test preparation course"]
SCHOOL_CHOICES = {c: [str(v) for v in cats]
                  for c, cats in zip(_school_cat_cols, _school_enc.categories_)}
SCHOOL_LABELS = {
    "gender": "Gender", "race/ethnicity": "Race / ethnicity",
    "parental level of education": "Parental level of education",
    "lunch": "Lunch", "test preparation course": "Test preparation course",
    "reading score": "Reading score", "writing score": "Writing score"}

# ----------------------------------------------------------- college setup

YN = {1: "Yes", 2: "No"}
FREQ3 = {1: "Never", 2: "Sometimes", 3: "Always"}
EDU = {1: "Primary school", 2: "Secondary school", 3: "High school",
       4: "University", 5: "MSc", 6: "PhD"}
GPA = {1: "Below 2.00", 2: "2.00 - 2.49", 3: "2.50 - 2.99", 4: "3.00 - 3.49", 5: "Above 3.49"}
COLLEGE_META = {
    "1": ("Age", {1: "18 - 21", 2: "22 - 25", 3: "26 or above"}),
    "2": ("Sex", {1: "Female", 2: "Male"}),
    "3": ("High school type", {1: "Private", 2: "State", 3: "Other"}),
    "4": ("Scholarship type", {1: "None", 2: "25%", 3: "50%", 4: "75%", 5: "Full"}),
    "5": ("Additional work", YN),
    "6": ("Regular artistic or sports activity", YN),
    "7": ("Has a partner", YN),
    "8": ("Total salary (if available)", {1: "USD 135 - 200", 2: "USD 201 - 270",
          3: "USD 271 - 340", 4: "USD 341 - 410", 5: "Above USD 410"}),
    "9": ("Transportation to the university", {1: "Bus", 2: "Private car / taxi", 3: "Bicycle", 4: "Other"}),
    "10": ("Accommodation type", {1: "Rental", 2: "Dormitory", 3: "With family", 4: "Other"}),
    "11": ("Mother's education", EDU),
    "12": ("Father's education", EDU),
    "13": ("Number of siblings", {1: "1", 2: "2", 3: "3", 4: "4", 5: "5 or more"}),
    "14": ("Parental status", {1: "Married", 2: "Divorced", 3: "One or both deceased"}),
    "15": ("Mother's occupation", {1: "Retired", 2: "Housewife", 3: "Government officer",
           4: "Private sector employee", 5: "Self-employed", 6: "Other"}),
    "16": ("Father's occupation", {1: "Retired", 2: "Government officer",
           3: "Private sector employee", 4: "Self-employed", 5: "Other"}),
    "17": ("Weekly study hours", {1: "None", 2: "Under 5 hours", 3: "6 - 10 hours",
           4: "11 - 20 hours", 5: "More than 20 hours"}),
    "18": ("Reading frequency (non-scientific books)", {1: "None", 2: "Sometimes", 3: "Often"}),
    "19": ("Reading frequency (scientific books)", {1: "None", 2: "Sometimes", 3: "Often"}),
    "20": ("Attends department seminars / conferences", YN),
    "21": ("Impact of projects / activities on success", {1: "Positive", 2: "Negative", 3: "Neutral"}),
    "22": ("Class attendance", {1: "Always", 2: "Sometimes", 3: "Never"}),
    "23": ("Midterm 1 preparation", {1: "Alone", 2: "With friends", 3: "Not applicable"}),
    "24": ("Midterm 2 preparation", {1: "Close to the exam date",
           2: "Regularly during the semester", 3: "Never"}),
    "25": ("Takes notes in class", FREQ3),
    "26": ("Listens in class", FREQ3),
    "27": ("Discussion improves interest and success", FREQ3),
    "28": ("Flipped classroom", {1: "Not useful", 2: "Useful", 3: "Not applicable"}),
    "29": ("Last semester GPA (out of 4.00)", GPA),
    "30": ("Expected GPA at graduation (out of 4.00)", GPA),
    # "COURSE ID": ("Subject", {}),
    
    # this for course id, we will use the course name instead of id 
    "COURSE ID": ("Course ID", {}),
}
# GRADES = {0: "Fail", 1: "DD", 2: "DC", 3: "CC", 4: "CB", 5: "BB", 6: "BA", 7: "AA"}

GRADES = {
    0: "F",
    1: "D",
    2: "C",
    3: "C+",
    4: "B",
    5: "B+",
    6: "A",
    7: "A+"
}

COLLEGE_FEATURES = list(college_model.feature_names_in_)
_college_enc = college_model.named_steps["preprocessor"].transformers_[0][1]
COLLEGE_FIELDS = []
for col, cats in zip(COLLEGE_FEATURES, _college_enc.categories_):
    label, names = COLLEGE_META[col]
    opts = [{"value": int(c), "label": names.get(int(c), f"Course {int(c)}" if col == "COURSE ID" else str(int(c)))}
            for c in cats]            # only values the model saw in training
    COLLEGE_FIELDS.append({"name": col, "label": label, "options": opts})

# ---------------------------------------------- dashboard data (from models)

def _school_coefficients():
    pre = school_model.named_steps["preprocessor"]
    names = [n.split("__", 1)[-1] for n in pre.get_feature_names_out()]
    coefs = school_model.steps[-1][1].coef_
    rows = sorted(zip(names, coefs), key=lambda r: abs(r[1]), reverse=True)[:10]
    return {"labels": [r[0].replace("_", ": ") for r in rows],
            "values": [round(float(r[1]), 3) for r in rows]}


def _college_importances():
    pre = college_model.named_steps["preprocessor"]
    names = [n.split("__", 1)[-1].rsplit("_", 1)[0] for n in pre.get_feature_names_out()]
    imp = pd.Series(college_model.steps[-1][1].feature_importances_).groupby(names).sum()
    imp = imp.sort_values(ascending=False).head(10)
    return {"labels": [f"{COLLEGE_META[k][0]}" for k in imp.index],
            "values": [round(float(v) * 100, 2) for v in imp.values]}


DASHBOARD = {
    "school_algo": type(school_model.steps[-1][1]).__name__,
    "college_algo": type(college_model.steps[-1][1]).__name__,
    "school_coef": _school_coefficients(),
    "college_imp": _college_importances(),
    # Figures supplied from the training notebooks (not recomputed here).

    "school_metrics": {"cv_r2": 0.8717, "test_r2": 0.8805, "test_mae": 4.21},
    "college_metrics": {"cv_acc": 35.86, "records": 145, "classes": 8},
}

# ------------------------------------------------------------------ routes

@app.route("/")
def home():
    return render_template("index.html", page="home")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", page="dashboard", d=DASHBOARD)


@app.route("/school")
def school():
    return render_template("school.html", page="school", choices=SCHOOL_CHOICES)


@app.route("/college")
def college():
    return render_template("college.html", page="college", fields=COLLEGE_FIELDS)


@app.post("/api/predict/school")
def predict_school():
    data = request.get_json(silent=True) or {}
    row, errors = {}, {}
    for col, allowed in SCHOOL_CHOICES.items():
        v = str(data.get(col, "")).strip()
        if not v:
            errors[col] = "This field is required."
        elif v not in allowed:
            errors[col] = "Choose one of the listed options."
        row[col] = v
    for col in ("reading score", "writing score"):
        try:
            v = float(data.get(col))
            if not 0 <= v <= 100:
                raise ValueError
            row[col] = v
        except (TypeError, ValueError):
            errors[col] = "Enter a number from 0 to 100."
    if errors:
        return jsonify(ok=False, errors=errors), 400
    X = pd.DataFrame([row])[SCHOOL_FEATURES]
    raw = float(school_model.predict(X)[0])
    return jsonify(ok=True, score=round(min(max(raw, 0), 100), 1))


@app.post("/api/predict/college")
def predict_college():
    data = request.get_json(silent=True) or {}
    row, errors = {}, {}
    for f in COLLEGE_FIELDS:
        allowed = {o["value"] for o in f["options"]}
        try:
            v = int(data.get(f["name"]))
            if v not in allowed:
                raise ValueError
            row[f["name"]] = v
        except (TypeError, ValueError):
            errors[f["name"]] = "Choose one of the listed options."
    if errors:
        return jsonify(ok=False, errors=errors), 400
    X = pd.DataFrame([row])[COLLEGE_FEATURES]
    grade = int(college_model.predict(X)[0])
    return jsonify(ok=True, grade=grade, category=GRADES[grade])


if __name__ == "__main__":
    app.run(debug=True)
