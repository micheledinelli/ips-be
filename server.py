from flask import (Flask, jsonify, Response, logging, request)
from flask_cors import CORS
import utils
import room
import user
import device
import position
import live

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(room.bp)
app.register_blueprint(user.bp)
app.register_blueprint(device.bp)
app.register_blueprint(position.bp)
app.register_blueprint(live.bp)
CORS(app)


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