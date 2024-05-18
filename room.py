from flask import (Blueprint, jsonify, request)
from bson.json_util import dumps
from db import db


bp = Blueprint('rooms', __name__, url_prefix='/rooms')


@bp.route('', methods=['GET'])
def get_rooms():
    """
    Get all rooms
    ---
    tags:
        - rooms
    responses:
      200:
        description: List of rooms
    """
    room_cursor = db.rooms.find()

    # Convert the cursor to a list of dictionaries
    rooms_list = list(room_cursor)
    
    # Serialize the list of dictionaries to JSON
    users_json = dumps(rooms_list)
    return users_json


@bp.route('/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):  
    """
    Get room by id
    ---
    tags:
        - rooms
    parameters:
      - name: room_id
        in: path
        type: integer
        required: true
        description: ID of the room
    responses:
      200:
        description: Room object
    """
    room = db.rooms.find_one_or_404({"roomId": room_id})
    
    # Serialize the dictionary to JSON
    room_json = dumps(room)
    return room_json


@bp.route('/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    # Read the request data
    data = request.get_json()
    
    # Find the room by id
    room = get_room_by_id(room_id)

    # If the room is found, update its attributes
    if room:    
        db.rooms.update_one({"roomId": room_id}, {
            "$set": {
                "name": data["name"],
                "grantedTo": data["grantedTo"],
                "public": data["public"],
                "devices": data["devices"],
                "notification": data["notification"]
            }
        })
        
        return jsonify(room)

    # If the room is not found, return an error message
    return jsonify({"error": "Room not found"}), 404