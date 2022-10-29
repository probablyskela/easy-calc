from flask import Flask
app = Flask(__name__)


from app.views import user
from app.views import calculator

app.register_blueprint(user.user_blueprint)
app.register_blueprint(calculator.calculator_blpr)
app.register_blueprint(calculator.calculators_blpr)

