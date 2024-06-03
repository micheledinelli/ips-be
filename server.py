from flask import (Flask, jsonify, send_file)
from flask_cors import CORS
import room
import utils
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


@app.route('/api/dataset', methods=['GET', 'OPTIONS'])
def get_dataset():
    file_path = utils.get_dataset_path(data_path=app.config['DATA_PATH'])
    return send_file(file_path, mimetype='application/octet-stream', as_attachment=True, download_name='data.pkl')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)