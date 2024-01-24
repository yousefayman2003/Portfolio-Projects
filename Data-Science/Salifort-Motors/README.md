<h1 align=center> Data-Driven Employee Retention System </h1>

# Table of Contents

- [Introduction](#introduction)
- [Project Scenario](#project_scenario)
- [Dataset Overview](#dataset_overview)
- [Project Stages](#project_stages)
- [Conclusion](#conclusion)

<a id="introduction"></a>

# Introduction

The Data-Driven Employee Retention System is designed to provide data-driven suggestions for HR professionals to improve employee satisfaction levels and reduce turnover. The system analyzes a dataset collected by the HR department at Salifort Motors, focusing on factors that influence employee retention. The primary goal is to build a predictive model that can identify employees likely to leave the company, allowing proactive measures to be taken to retain valuable talent.

<a id="project_scenario"></a>

# Project Scenario

The HR department at Salifort Motors has gathered data from employees but is uncertain about how to leverage it effectively. They seek data-driven suggestions to address the following question: "What's likely to make an employee leave the company?" By understanding the factors contributing to employee turnover, the company aims to implement initiatives that improve job satisfaction and increase retention.

<a id="dataset_overview"></a>

# Dataset Overview

The dataset contains 14,999 rows and 10 columns with the following variables:

`satisfaction_level`: Employee-reported job satisfaction level [0–1]

`last_evaluation`: Score of the employee's last performance review [0–1]

`number_project`: Number of projects the employee contributes to

`average_monthly_hours`: Average number of hours the employee worked per month

`tenure`: How long the employee has been with the company (in years)

`work_accident`: Whether or not the employee experienced an accident while at work

`left`: Whether or not the employee left the company (target variable)

`promotion_last_5years`: Whether or not the employee was promoted in the last 5 years

`department`: The employee's department

`salary`: The employee's salary (U.S. dollars)

# Project Stages

<a id="project_stages"></a>

## Step 1: Data Exploration and Cleaning

- Gather basic information about the data
- Check for missing values and duplicates
- Handle outliers in the tenure column
- Explore relationships between variables through visualizations
- Rename columns for consistency

## Step 2: Feature Engineering

- Encode categorical variables (salary, department)
- Create a binary feature (overworked) to identify employees working more than 175 hours/month
- Drop unnecessary features

### Step 3: Model Building & Evaluation

- Approach A: Logistic Regression Model
  - Train a logistic regression model
  - Evaluate the model's performance on the test set
  - Visualize confusion matrix and classification report
- Approach B: Tree-Based Model
  - Random Forest Classifier
    - Train a random forest model using hyperparameter tuning
    - Evaluate the model's performance on the test set
    - Visualize confusion matrix and feature importances
  - Gradient Boosting Classifier
    - Train a gradient boosting model using hyperparameter tuning
    - Evaluate the model's performance on the test set
    - Visualize confusion matrix and feature importances

<a id="conclusion"></a>

# Conclusion

The Data-Driven Employee Retention System leverages machine learning models to predict and address employee turnover. By applying data-driven insights, the HR department can proactively implement measures to retain valuable talent and create a more satisfying work environment.
