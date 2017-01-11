from flask import Blueprint

item_blueprint = Blueprint('items', __name__)

@item_blueprint.route('/item/<string:name')
def item_page(name):
    pass

@item_blueprint.route('/load')
def load_item():
    """
    Load an item's data using the store and return their json representation
    :return:
    """
