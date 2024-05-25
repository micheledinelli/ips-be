from flask import (Blueprint, jsonify, request, current_app)
from db import db
import utils
import model


bp = Blueprint('position', __name__, url_prefix='/position')


@bp.route('', methods=['POST'])
def postion():
    data = request.get_json()

    # Get the user id
    user_id = data.get('userId')

    # Check user exists
    user = db.users.find_one({"userId": user_id})

    if user is None:
        return jsonify({"message": "User not found"}), 404

    # Get the access points
    access_points = data.get('accessPoints')

    # Get the location (may be None)
    room = data.get('room') 

    # If room is provided, then save the data otherwise return a prediction
    if not room:
        prediction = model.predict(access_points, data_path=current_app.config["DATA_PATH"])
        db.users.update_one({"userId": user_id}, {"$set": {"lastSeen": prediction}})
        return jsonify({"room": prediction})

    utils.async_save_data(online_data=access_points, room=room, data_path=current_app.config["DATA_PATH"])
    return jsonify({"message": "Data received"})    