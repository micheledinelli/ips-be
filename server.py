from flask import (Flask, jsonify, request, send_file)
from flask_cors import CORS
import room
import utils
import user
import device
import position
import live
import os
import model

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
    print(file_path)
    return send_file(file_path, mimetype='application/octet-stream', as_attachment=True, download_name='data.pkl')


@app.route('/api/dataset', methods=['POST'])
def post_dataset():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pkl'):
        print(os.path.join(app.config['DATA_PATH'], 'data.pkl'))
        file.save(os.path.join(app.config['DATA_PATH'], 'data.pkl'), overwrite=True)
        model.train(data_path=app.config['DATA_PATH'])
        return jsonify({"message": "Dataset uploaded"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)