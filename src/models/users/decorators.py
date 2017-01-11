from functools import wraps
from src.app import app

from flask import request
from flask import session
from flask import url_for, redirect



def requires_login(func):
    #func()  # this makes sure you can only run this method inside the context of decorator
    @wraps(func) # this allows you to invoke the function outside the context of decorator
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect((url_for('users.login_user', next=request.path)))# next arguement makes sure user gets redirected to http://127.0.0.1:4490/alerts/new after succesful login
        return func(*args, **kwargs) ## after login when next parameter above is executed this method gets invoked
    return decorated_function # this statement fires up the decorated function when ever the wrapped function is invoked

# the block below was just for demonstrating the decorated function
# @requires_login ## this decorator translates for python that it will take an arguement
# def my_function(x, y): ##this function exists in the context of the requires_login(). ie. you cannot call this function outside the requires_login()
#     print "decorated"
#     return x+y
#
#
# print my_function(5,6) ## when you put the function in the wraps/decorated and then return the wrap/decorated function you get to call the method this way



def requires_admin_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function
