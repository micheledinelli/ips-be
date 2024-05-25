from flask import Blueprint, Response, jsonify


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
                    "type": "perimeter"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0, 0],
                            [0, 150],
                            [100, 100],
                            [100, 0],
                            [0, 0]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Kitchen",
                    "roomId": 1,
                    "users": [2727],
                    "type": "room"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 10],
                            [30, 10],
                            [30, 30],
                            [10, 30],
                            [10, 10]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Living Room",
                    "roomId": 2,
                    "users": [2727, 3030],
                    "type": "room"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [40, 10],
                            [60, 10],
                            [60, 30],
                            [40, 30],
                            [40, 10]
                        ]
                    ]
                }
            }
        ]
    }

    return jsonify(data)
