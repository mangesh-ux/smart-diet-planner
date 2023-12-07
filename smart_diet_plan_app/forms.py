## forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=1)])
    height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=1)])
    activity_level = SelectField('Activity Level', choices=[('sedentary', 'Sedentary'), ('light', 'Light'), ('moderate', 'Moderate'), ('active', 'Active'), ('very active', 'Very Active')], validators=[DataRequired()])
    goal = SelectField('Goal', choices=[('lose weight', 'Lose Weight'), ('maintain weight', 'Maintain Weight'), ('gain weight', 'Gain Weight')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DietPlanForm(FlaskForm):
    calories = IntegerField('Calories', validators=[DataRequired(), NumberRange(min=1)])
    protein = IntegerField('Protein (g)', validators=[DataRequired(), NumberRange(min=1)])
    carbs = IntegerField('Carbs (g)', validators=[DataRequired(), NumberRange(min=1)])
    fats = IntegerField('Fats (g)', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Generate Diet Plan')
