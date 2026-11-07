# PerformPredict
### Predict Performance. Discover Potential.

PerformPredict is a machine learning-based web application designed to predict the academic performance of school and college students. It uses student-related information and trained machine learning models to generate predictions through a simple and user-friendly interface.

## About the Project

The project provides two prediction systems:

1. **School Student Performance Prediction:** Estimates a student's Mathematics score based on information such as gender, parental education, lunch type, test preparation, reading score, and writing score.

2. **College Student Performance Prediction:** Predicts a student's academic grade using college-related information, including study habits, class attendance, previous academic performance, and other student details.

## Features

- Separate prediction systems for school and college students.
- Machine learning models trained on academic datasets.
- Interactive prediction forms.
- User-friendly dashboard.
- Visual representation of model performance.
- Responsive website design.
- No login or registration required.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Scikit-learn | Machine learning models |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Joblib | Model saving and loading |
| HTML | Website structure |
| CSS | Website styling |
| JavaScript | Interactive functionality |
| Chart.js | Data visualization |

## Machine Learning Models

| Prediction System | Algorithm | Output |
|---|---|---|
| School Students | Ridge Regression | Mathematics Score |
| College Students | Random Forest Classifier | Academic Grade |

### School Model
- Dataset: Students Performance Dataset.
- Selected model: Ridge Regression.
- Test R² Score: Approximately 0.8805.
- Predicts Mathematics marks based on student information and reading and writing scores.

### College Model
- Dataset: Higher Education Students Performance Evaluation.
- Selected model: Random Forest Classifier.
- Dataset size: 145 records.
- Cross-validation accuracy: Approximately 35.86%.
- Predicts academic grade categories.

**Note:** The college model has limited accuracy because of the small dataset. Its predictions should be treated as estimates, not guaranteed academic results.

## How It Works

1. Visit the PerformPredict website.
2. Choose School or College Prediction.
3. Enter the required student details.
4. Submit the information.
5. The trained machine learning model processes the inputs.
6. View the predicted academic result.

## Project Goal

The goal of PerformPredict is to explore how machine learning can be used in education to understand student performance and provide data-based academic predictions.

## Limitations

- Predictions depend on the quality and size of the training datasets.
- The school model currently predicts Mathematics marks only.
- The college model uses a relatively small dataset.
- Results are estimates and should not replace actual academic assessments.

## Future Improvements

- Use larger and more diverse datasets.
- Improve prediction accuracy.
- Add more academic prediction options.
- Include additional data visualization features.
- Support more grading systems.

## License

This project is licensed under the Apache License 2.0. You are free to use, modify, and distribute this project according to the license terms.

See the [LICENSE](LICENSE) and [NOTICE](NOTICE) files for details.

## Author

**Atif Khan**
Specialization in Artificial Intelligence and Machine Learning

## Find Me Online
For questions, suggestions, or feedback, feel free to connect with me.

* **Portfolio:** [Webspace](https://theatif.netlify.app/)
* **GitHub:** [Atif Khan](https://github.com/theatiff/)

## Disclaimer

This Project is developed for educational and learning purposes. The predictions are estimates and should not be treated as guaranteed student results.

---

**PerformPredict**  
*Predict Performance. Discover Potential.*
