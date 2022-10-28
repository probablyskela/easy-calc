from flask import Flask
app = Flask(__name__)


from app.views import user

# import easy_calc.user
app.register_blueprint(user.blpr)

