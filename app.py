from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input

app = Flask(__name__)

# Set up the upload folder for storing the user-uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the pre-trained machine learning model
# Replace 'YOUR_MODEL_PATH' with the actual path to your model
model_path = "YOUR_MODEL_PATH"
if not os.path.exists(model_path):
    print(f"Model file '{model_path}' not found.")
    exit()
model = load_model(model_path)

# Load the class labels from a text file
# Replace 'YOUR_LABEL_PATH' with the actual path to your label file
label_path = 'YOUR_LABEL_PATH'
if not os.path.exists(label_path):
    print(f"Label file '{label_path}' not found.")
    exit()
class_labels = [line.strip() for line in open(label_path)]

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file chosen'}), 400

    try:
        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)

        # Preprocess the image
        processed_image = preprocess_image(img_path)

        # Make a prediction using the model
        prediction = model.predict(processed_image)

        # Get the predicted class label
        predicted_class = np.argmax(prediction)
        predicted_label = class_labels[predicted_class]

        # If predicted_label is not one of the labels, it's probably an error
        if predicted_label not in class_labels:
            return jsonify({'error': 'Prediction failed'}), 500

        response = {'predicted_class': predicted_label}
        return jsonify(response), 200

    except Exception as e:
        error_message = f"An error occurred while processing the image: {str(e)}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
