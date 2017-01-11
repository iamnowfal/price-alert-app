from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.models.users.errors import UserNotExistsError, IncorrectPasswordError, UserError
from src.models.users.user import User
from src.models.users import decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST']) # when the blueprint gets registered with the app, the rule looks like /login (HEAD, OPTIONS, GET)->users.show
def login_user():
    if request.method == 'GET':
        return render_template('/users/login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        # except:
        #     return "Your credentials are wrong, Sorry!"

        # except UserNotExistsError as e:
        #     return e.message
        # except IncorrectPasswordError as e:
        #     return e.message

        except UserError as e:
            return e.message
        return render_template('/users/login.html') # this is executed when the password is invalid

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('/users/register.html')
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserError as e:
            return e.message
        return render_template('/users/register.html')

@user_blueprint.route('/alerts')
#@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email']) # the decorator above makes sure that this line will not throw any errors when trying to access alerts with out session
    print user.email
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts) ##this send the user specific alert page
    #return "This is the alerts page"

@user_blueprint.route('/logout')
def  logout_user():
    session['email'] = None
    return redirect(url_for('home')) ## this method is the under the root endpoint in the app.py file

@user_blueprint.route('/check_alerts/<string:user_id>')
@user_decorators.requires_login
def check_user_alerts(user_id):
    pass
