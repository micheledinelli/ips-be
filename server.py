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
app.register_blueprint(room.bp, url_prefix='/api')
app.register_blueprint(user.bp, url_prefix='/api')
app.register_blueprint(device.bp, url_prefix='/api')
app.register_blueprint(position.bp, url_prefix='/api')
app.register_blueprint(live.bp, url_prefix='/api')
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
    app.run(host='0.0.0.0', port=8888, debug=True)