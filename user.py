from flask import Blueprint
from bson.json_util import dumps
from db import db


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def users():
    """
    Get all users
    ---
    tags:
        - users
    responses:
      200:
        description: List of users
    """
    
    # Find all users in the collection
    users_cursor = db.users.find()

    # Convert the cursor to a list of dictionaries
    users_list = list(users_cursor)
    
    # Serialize the list of dictionaries to JSON
    users_json = dumps(users_list)
    
    return users_json