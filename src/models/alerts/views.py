from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
from src.models.users import decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)

# @alert_blueprint.route('/')
# def index():
#     return "This is the alerts index"

@alert_blueprint.route('/new', methods=['GET', 'POST']) ## you can directly access this url http://127.0.0.1:4490/alerts/new without login
@user_decorators.requires_login ##makes sure only sessions allow creation of alerts
def create_alert():
    if request.method == 'POST':
        item_name = request.form['name']
        item_url = request.form['url']
        price_limit = float(request.form['price_limit'])
        #price_limit = float(request.form['price_limit'])

        item = Item(name=item_name, url=item_url)
        item.save_to_db() ## this always creates a new item in the items database
        alert = Alert(user_email=session['email'],price_limit=price_limit,item_id=item._id)
        alert.load_item_price()

    return render_template('alerts/create_alert.html')

@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_alert_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_alert_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_alert_by_id(alert_id)
    #print alert
    return render_template("alerts/alert.html", alert=alert)

@alert_blueprint.route('/refresh/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price(alert_id):
    Alert.find_alert_by_id(alert_id).load_item_price()
    return  redirect(url_for('.get_alert_page', alert_id=alert_id))

@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_alert_by_id(alert_id).delete_alert()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_alert_by_id(alert_id)
    if request.method == "POST":
        alert.price_limit =float(request.form['price_limit'])
        alert.save_to_mongo()
        return redirect(url_for('users.user_alerts'))
    return render_template('/alerts/edit_alert.html', alert=alert)

@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass

