from flask import (Blueprint, jsonify, request)
from bson.json_util import dumps
from db import db


bp = Blueprint('devices', __name__, url_prefix='/api/devices')


@bp.route('', methods=['GET'])
def get_devices():
    """
    Get all devices
    ---
    tags:
        - devices
    responses:
      200:
        description: List of devices
    """
    device_cursor = db.devices.find()

    # Convert the cursor to a list of dictionaries
    devices_list = list(device_cursor)
    
    # Serialize the list of dictionaries to JSON
    devices_json = dumps(devices_list)
    return devices_json