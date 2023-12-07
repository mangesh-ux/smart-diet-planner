## models.py

from main import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(50), nullable=False)
    diet_plan_id = db.Column(db.Integer, db.ForeignKey('diet_plan.id'))

    def __init__(self, username: str, password: str, age: int, gender: str, weight: float, height: float, activity_level: str, goal: str):
        self.username = username
        self.password = password
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.goal = goal

class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='diet_plan', uselist=False)

    def __init__(self, calories: int, protein: int, carbs: int, fats: int):
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class DietPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DietPlan
        load_instance = True
