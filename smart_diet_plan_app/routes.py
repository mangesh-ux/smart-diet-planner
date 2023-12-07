## routes.py

from flask import render_template, url_for, flash, redirect, request
from smart_diet_plan_app import app, db
from smart_diet_plan_app.forms import RegistrationForm, LoginForm, DietPlanForm
from smart_diet_plan_app.models import User, DietPlan, UserSchema, DietPlanSchema
from smart_diet_plan_app.utils import generate_diet_plan, track_progress, suggest_meals
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, age=form.age.data, gender=form.gender.data, weight=form.weight.data, height=form.height.data, activity_level=form.activity_level.data, goal=form.goal.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dietplan", methods=['GET', 'POST'])
@login_required
def dietplan():
    form = DietPlanForm()
    if form.validate_on_submit():
        diet_plan = DietPlan(calories=form.calories.data, protein=form.protein.data, carbs=form.carbs.data, fats=form.fats.data)
        db.session.add(diet_plan)
        db.session.commit()
        flash('Your diet plan has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('dietplan.html', title='Diet Plan', form=form)

@app.route("/track", methods=['GET', 'POST'])
@login_required
def track():
    if request.method == 'POST':
        # Get food intake data from form
        food_intake_data = request.form
        # Track progress
        track_progress(current_user, food_intake_data)
        flash('Your progress has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template('track.html', title='Track')

@app.route("/suggest", methods=['GET', 'POST'])
@login_required
def suggest():
    if request.method == 'POST':
        # Get food preference data from form
        food_preference_data = request.form
        # Suggest meals
        meal_suggestions = suggest_meals(current_user, food_preference_data)
        flash('Meal suggestions have been generated!', 'success')
        return render_template('suggest.html', title='Suggest', meal_suggestions=meal_suggestions)
    return render_template('suggest.html', title='Suggest')

@app.route("/adjust", methods=['GET', 'POST'])
@login_required
def adjust():
    form = DietPlanForm()
    if form.validate_on_submit():
        # Adjust diet plan
        current_user.diet_plan.calories = form.calories.data
        current_user.diet_plan.protein = form.protein.data
        current_user.diet_plan.carbs = form.carbs.data
        current_user.diet_plan.fats = form.fats.data
        db.session.commit()
        flash('Your diet plan has been adjusted!', 'success')
        return redirect(url_for('home'))
    return render_template('adjust.html', title='Adjust', form=form)

@app.route("/progress", methods=['GET', 'POST'])
@login_required
def progress():
    # Get progress data
    progress_data = get_progress_data(current_user)
    return render_template('progress.html', title='Progress', progress_data=progress_data)
