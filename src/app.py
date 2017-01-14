from flask import Flask
from flask import render_template

from src.common.database import Database




app = Flask(__name__)
app.config.from_object('src.config') #config class i imported as attributes to the app class here.
app.secret_key= "password"

@app.before_first_request
def init_db():
    Database.initialize()

# @app.route('/')
# def hello_world():
#     return "hello, how is it going?"

@app.route('/')
def home():
    return render_template('home.html')

from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")



