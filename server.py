from flask import (Flask, jsonify, Response, logging, request)
from flask_cors import CORS
import utils
import room
import user
import device
import position

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(room.bp)
app.register_blueprint(user.bp)
app.register_blueprint(device.bp)
app.register_blueprint(position.bp)
CORS(app)


# @app.route('/stream')
# def stream():
#     return Response(event_stream(), mimetype="text/event-stream")


# def event_stream():
#     import time
#     while True:
#         time.sleep(10)
#         yield "data: {}\n\n".format("Hello, world!")


@app.route('/', methods=['GET', 'OPTIONS'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
        - health
    responses:
      200:
        description: Service status
    """
    return jsonify({"health": "up"})


if __name__ == '__main__':
    app.run(port=8888, debug=True)