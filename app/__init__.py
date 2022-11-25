from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['DATABASE'] = open("config.txt", "r").read().strip()
from app.views import user, calculator, review


app.register_blueprint(user.user_blueprint)
app.register_blueprint(calculator.calculator_blpr)
app.register_blueprint(calculator.calculators_blpr)
app.register_blueprint(review.reviews_blpr)

