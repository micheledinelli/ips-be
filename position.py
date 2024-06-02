import enum
from flask import (Blueprint, jsonify, request, current_app)
from db import db
import utils
import model


bp = Blueprint('position', __name__, url_prefix='/api/position')


class ViolationType(enum.Enum):
    ACCESS_GRANTED = 0
    ACCESS_DENIED = 1
    NOT_HOLDING_REQUIRED_DEVICES = 2
    LEFT_ROOM_WITH_REQUIRED_DEVICES = 3

    @property
    def message(self, messages = {
        "ACCESS_GRANTED": "Access granted",
        "ACCESS_DENIED": "Access denied, you are not granted access to this room",
        "NOT_HOLDING_REQUIRED_DEVICES": "Access denied, you are not holding the required devices",
        "LEFT_ROOM_WITH_REQUIRED_DEVICES": "Warning! you left the room with required devices"
    }):
        return messages.get(self.name, "Unknown violation type")


@bp.route('', methods=['POST'])
def postion():
    data = request.get_json()

    # Get the user id
    user_id = int(data.get('userId'))

    # Check user exists
    user = db.users.find_one({"userId": user_id})

    if user is None:
        return jsonify({"message": "User not found"}), 404

    # Get the access points
    access_points = data.get('accessPoints')

    # Get ble devices
    ble_devices = data.get('bleDevices')
    
    # Get the location (may be None)
    room = data.get('room')

    # If room is provided, then save the data otherwise return a prediction
    if not room:
        # Predict where the user is
        prediction = model.predict(access_points, data_path=current_app.config["DATA_PATH"])
        
        # Find the room in the database
        room = db.rooms.find_one({"name": prediction})
        if not room:
            return jsonify({"message": "Room not found"}), 404
        
        room_devices_cursor = db.devices.find({"deviceId": {"$in": room["devices"]}})
        room_devices = list(room_devices_cursor)

        # Check if the user has access to the room
        userAccess = checkUserAccess(user=user, room=room, ble_devices=ble_devices, room_devices=room_devices)

        # Check if the room requires any devices
        required_devices = getRequiredDevices(room=room)

        # Update the last seen time of the user
        db.users.update_one({"userId": user_id}, {"$set": {"lastSeen": prediction}})
        return jsonify({"room": prediction,
                        "granted": userAccess == ViolationType.ACCESS_GRANTED, 
                        "violation": userAccess.message, 
                        "devicesRequired": required_devices,
                        "notificationType": room["notification"]})

    utils.async_save_data(online_data=access_points, room=room, data_path=current_app.config["DATA_PATH"])
    return jsonify({"message": "Data received"})

def checkUserAccess(user, room, ble_devices, room_devices) -> ViolationType:
    # The user has to be granted access and has to hold devices required
    # It is ensured in the backend that if a room is public there are no devices required and no granted users
    # It would be cool if this method returns a list of violations, maybe in the future
    granted_user_ids = room["grantedTo"]
    
    required_devices_ids = room["devices"]
    required_devices_names = [device["name"] for device in room_devices]
    
    # Keep only the ble devices with at least -70 rssi
    ble_devices = [device for device in ble_devices if device["rssi"] > -70]
    ble_devices_ids = [device["deviceId"] for device in ble_devices]
    ble_devices_names = [device["name"] for device in ble_devices]
    
    # Check if the user can access the new room
    if not room["public"] and user["userId"] not in granted_user_ids:
        return ViolationType.ACCESS_DENIED
    
    # Check if the user holds the required devices for the new room
    # (required devices has to be a subset of the ble devices)
    # It is check both the id and the name of the device
    if ((not set(required_devices_ids).issubset(set(ble_devices_ids))) and 
        (not set(required_devices_names).issubset(set(ble_devices_names)))):
        return ViolationType.NOT_HOLDING_REQUIRED_DEVICES

    # If the new room is different from the current room it means user left the room
    # so we have to ensure that the user is not holding any devices required in the previous room
    # (ble devices set has to have no intersection with required devices)
    if user.get("lastSeen") is not None:
        room_user_last_seen = db.rooms.find_one({"name": user["lastSeen"]})
        required_device_ids_last_seen = room_user_last_seen["devices"]
        if (room_user_last_seen["name"] != room["name"] 
            and (set(required_device_ids_last_seen).intersection(set(ble_devices_ids)) or 
            set(required_devices_names).intersection(set(ble_devices_names)))):
            return ViolationType.LEFT_ROOM_WITH_REQUIRED_DEVICES
               
    return ViolationType.ACCESS_GRANTED

def getRequiredDevices(room):
    device_ids = room["devices"]
    devices = list(db.devices.find({"deviceId": {"$in": device_ids}}))
    
    # Remove the _id field
    for device in devices:
        device.pop("_id")
    return devices