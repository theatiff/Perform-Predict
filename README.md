# Perform_Predict

### Predict Performance. Discover Potential.

Perform_Predict is a machine learning-based web application that predicts student academic performance using student-related information.

The project includes two prediction systems: one for school students and another for college students. It uses trained machine learning models to generate predictions through a simple and user-friendly website.

## Features

* **School Student Prediction:** Predicts a student's Mathematics score using academic and personal information.
* **College Student Prediction:** Predicts a student's academic grade using college-related information.
* **Machine Learning Models:** Uses trained models built with Scikit-learn.
* **Interactive Dashboard:** Displays project information and model performance.
* **Simple Interface:** Easy-to-use forms for entering student information.
* **Responsive Design:** Designed to work on desktop, tablet, and mobile screens.

## Technologies Used

| Technology   | Purpose                           |
| ------------ | --------------------------------- |
| Python       | Backend programming               |
| Flask        | Web application framework         |
| Scikit-learn | Machine learning                  |
| Pandas       | Data processing                   |
| NumPy        | Numerical operations              |
| Joblib       | Saving and loading trained models |
| HTML         | Website structure                 |
| CSS          | Website styling                   |
| JavaScript   | Website interactions              |
| Chart.js     | Data visualization                |

## Project Structure

```text
Perform_Predict/
│
├── app.py
│
├── models/
│   ├── school_performance_model.pkl
│   └── college_student_model.pkl
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── school.html
│   └── college.html
│
└── static/
    ├── css/
    │   ├── style.css
    │   ├── dashboard.css
    │   ├── prediction.css
    │   └── responsive.css
    │
    ├── js/
    │   ├── main.js
    │   ├── dashboard.js
    │   └── prediction.js
    │
    └── images/
        ├── logo.png
        ├── home-background.png
        └── dashboard-background.png
```

## Machine Learning Models

### 1. School Student Performance Prediction

* Dataset: Students Performance Dataset.
* Model: Ridge Regression.
* Prediction: Mathematics score.
* Input features include gender, parental education, lunch type, test preparation, reading score, and writing score.
* Test R² Score: Approximately 0.8805.

### 2. College Student Performance Prediction

* Dataset: Higher Education Students Performance Evaluation.
* Model: Random Forest Classifier.
* Prediction: Student academic grade.
* Number of records: 145.
* Cross-validation accuracy: Approximately 35.86%.

**Note:** The college dataset is relatively small, and its prediction accuracy is limited. The results should be treated as experimental predictions rather than guaranteed academic outcomes.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Open the Project Folder

```bash
cd Perform_Predict
```

### 3. Install Required Packages

```bash
pip install flask pandas numpy scikit-learn joblib
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

## How It Works

1. Open the PerformPredict website.
2. Select School or College Prediction.
3. Enter the required student information.
4. Submit the form.
5. The trained machine learning model processes the information.
6. View the predicted result.

## Project Limitations

* Predictions depend on the datasets used during model training.
* The school model predicts Mathematics marks only.
* The college model has limited accuracy because of the small dataset.
* Predictions are estimates and should not be considered guaranteed results.
* The project does not store user accounts or prediction history.

## Future Improvements

* Collect larger and more diverse student datasets.
* Improve model accuracy through better training data.
* Add more academic performance prediction options.
* Improve data visualization and prediction reports.
* Support different grading systems.

---

**PerformPredict**

*Predict Performance. Discover Potential.*
