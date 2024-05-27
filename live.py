from pickle import dumps
from flask import Blueprint, Response, jsonify
from db import db


bp = Blueprint('live', __name__, url_prefix='/live')


# Eventually this will be a stream of data from the server
# @bp.route('')
# def stream():
#     return Response(event_stream(), mimetype="text/event-stream")

# def event_stream():
#     data = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "name": "Building",
#                     "type": "perimeter"
#                 },
#                 "geometry": {
#                     "type": "Polygon",
#                     "coordinates": [
#                         [
#                             [0, 0],
#                             [0, 150],
#                             [100, 100],
#                             [100, 0],
#                             [0, 0]
#                         ]
#                     ]
#                 }
#             },
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "name": "Kitchen",
#                     "roomId": 1,
#                     "users": [2727],
#                     "type": "room"
#                 },
#                 "geometry": {
#                     "type": "Polygon",
#                     "coordinates": [
#                         [
#                             [10, 10],
#                             [30, 10],
#                             [30, 30],
#                             [10, 30],
#                             [10, 10]
#                         ]
#                     ]
#                 }
#             },
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "name": "Living Room",
#                     "roomId": 2,
#                     "users": [2727, 3030],
#                     "type": "room"
#                 },
#                 "geometry": {
#                     "type": "Polygon",
#                     "coordinates": [
#                         [
#                             [40, 10],
#                             [60, 10],
#                             [60, 30],
#                             [40, 30],
#                             [40, 10]
#                         ]
#                     ]
#                 }
#             }
#         ]
#     }
    
#     # Convert the data to a JSON string
#     json_data = json.dumps(data)

#     # Send the JSON data as an event
#     yield f"data: {json_data}\n\n"

#     # Wait for 5 seconds before sending the next event
#     time.sleep(5)

@bp.route('', methods=['GET'])
def live():
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Building",
                    "type": "perimeter",
                    "users": []
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0, 0],
                            [300, 0],
                            [350, 100],
                            [300, 210],
                            [150, 300],
                            [50, 250],
                            [0, 200],
                            [0, 0]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Assembly Line",
                    "roomId": 101,
                    "users": [],
                    "type": "room",
                    "color": "green"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 10],
                            [180, 10],
                            [180, 100],
                            [10, 100],
                            [10, 10]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Quality Control",
                    "roomId": 205,
                    "users": [],
                    "type": "room",
                    "color": "purple"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [200, 10],
                            [290, 10],
                            [340, 100],
                            [200, 100],
                            [200, 10]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Packaging",
                    "roomId": 309,
                    "users": [],
                    "type": "room",
                    "color": "blue"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 110],
                            [100, 110],
                            [100, 190],
                            [10, 190],
                            [10, 110]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Storage",
                    "roomId": 403,
                    "users": [],
                    "type": "room",
                    "color": "orange"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [60, 200],
                            [210, 200],
                            [210, 250],
                            [160, 280],
                            [60, 240],
                            [60, 200]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Maintenance",
                    "roomId": 507,
                    "users": [],
                    "type": "room",
                    "color": "red"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [120, 110],
                            [300, 110],
                            [300, 190],
                            [120, 190],
                            [120, 110]
                        ]
                    ]
                }
            }
        ]
    }

    # Find all users in the collection
    users_cursor = db.users.find()

    # Convert the cursor to a list of dictionaries
    users_list = list(users_cursor)   

    # Create a dictionary to map roomIds to users
    rooms_cursor = db.rooms.find()
    rooms_list = list(rooms_cursor)
    room_users = {room.get("name"): [] for room in rooms_list}
    not_seen = []

    # For each user, read the lastSeen property and update the corresponding room's users list
    for user in users_list:
        last_seen_room = user.get("lastSeen")
        user_id = user.get("userId")
        if last_seen_room != None and user_id:
            room_users[last_seen_room].append(user_id)
        else:
            not_seen.append(user_id)

    # Update the data object with the users for each room
    # If a user has not be seen it goes in the building
    for feature in data["features"]:
        if feature["properties"]["type"] == "room":
            room_id = feature["properties"]["name"]
            feature["properties"]["users"] = room_users.get(room_id, [])
        elif feature["properties"]["type"] == "perimeter":
            feature["properties"]["users"] = not_seen

    return jsonify(data)
