from flask import Blueprint
from flask import json
from flask import render_template
from flask import request
from flask import url_for, redirect

from src.models.stores.store import Store
from src.models.users import decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')

def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def get_store_page(store_id):
    return render_template("/stores/store.html", store=Store.get_by_store_id(store_id))

@store_blueprint.route('/edit_store/<string:store_id>', methods=['GET','POST'])
@user_decorators.requires_admin_permission
def edit_store(store_id):
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        # query = request.form['query'] # this statement returns a string and BeautifulSoup expects a python dictionary
        query = json.loads(request.form['query'])  # this statement converts the string into a format identifiable for bs4
        #store = Store(name, url_prefix, tag_name, query, store_id) there is a chance that you may create a new store instead of updating the existin store if we fail to pass the store_id as parameter
        store = Store.get_by_store_id(store_id)
        store.name=name
        store.url_prefix =url_prefix
        store.tag_name = tag_name
        store.query = query
        store.save_to_mongo()
        return redirect(url_for('stores.get_store_page', store_id=store_id))

    return render_template('/stores/edit_store.html', store=Store.get_by_store_id(store_id))

@store_blueprint.route('/delete_store/<string:store_id>')
@user_decorators.requires_admin_permission
def delete_store(store_id):
    Store.get_by_store_id(store_id).delete_store()
    return redirect(url_for('.index'))
    #return "This is how you delete the store"

@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permission
def create_store():
    if request.method == 'POST':
        name=request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        #query = request.form['query'] # this statement returns a string and BeautifulSoup expects a python dictionary
        query = json.loads(request.form['query']) # this statement converts the string into a format identifiable for bs4
        store = Store(name,url_prefix,tag_name,query)
        store.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('/stores/create_store.html')