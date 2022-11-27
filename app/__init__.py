from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['DATABASE'] = 'postgresql+pg8000://postgres:123@localhost:5432/postgres'
from app.views import user, calculator, review


app.register_blueprint(user.user_blueprint)
app.register_blueprint(calculator.calculators_blpr)
app.register_blueprint(review.reviews_blpr)

