## utils.py

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from models import User, DietPlan

def generate_diet_plan(user: 'User', nutritional_data: pd.DataFrame) -> 'DietPlan':
    """
    This function generates a diet plan for a user based on their personal details and a machine learning model trained on nutritional data.
    """

    # Encode categorical variables
    le = LabelEncoder()
    nutritional_data['activity_level'] = le.fit_transform(nutritional_data['activity_level'])
    nutritional_data['goal'] = le.fit_transform(nutritional_data['goal'])

    # Prepare data
    X = nutritional_data.drop('calories', axis=1)
    y = nutritional_data['calories']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict calories
    calories = model.predict(np.array([user.age, user.weight, user.height, le.transform([user.activity_level])[0], le.transform([user.goal])[0]]).reshape(1, -1))[0]

    # Calculate macronutrients based on calories and user's goal
    if user.goal == 'lose weight':
        protein = 0.4 * calories
        carbs = 0.3 * calories
        fats = 0.3 * calories
    elif user.goal == 'maintain weight':
        protein = 0.3 * calories
        carbs = 0.4 * calories
        fats = 0.3 * calories
    else:  # gain weight
        protein = 0.2 * calories
        carbs = 0.5 * calories
        fats = 0.3 * calories

    # Create diet plan
    diet_plan = DietPlan(calories, protein, carbs, fats)

    return diet_plan

def track_progress(user: 'User', progress_data: pd.DataFrame):
    """
    This function tracks the user's progress based on their food intake and diet plan.
    """

    # Calculate total intake
    total_intake = progress_data.sum()

    # Calculate remaining intake
    remaining_intake = user.diet_plan - total_intake

    # Plot progress
    plt.figure(figsize=(10, 5))
    sns.barplot(x=['Calories', 'Protein', 'Carbs', 'Fats'], y=[total_intake['calories'], total_intake['protein'], total_intake['carbs'], total_intake['fats']])
    plt.title('Total Intake')
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=['Calories', 'Protein', 'Carbs', 'Fats'], y=[remaining_intake['calories'], remaining_intake['protein'], remaining_intake['carbs'], remaining_intake['fats']])
    plt.title('Remaining Intake')
    plt.show()
