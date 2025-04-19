from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from model.pothole_detection import PotholeDetector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

detector = PotholeDetector()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Detect potholes
    potholes = detector.detect_potholes(filepath)

    # For demo, location data is not processed here, frontend can send location if needed
    response = {
        'filename': filename,
        'potholes': potholes,
        'message': f'Detected {len(potholes)} potholes'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
