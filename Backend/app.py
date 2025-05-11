from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import keras_hub
import numpy as np
from PIL import Image
import uuid
import os

# Flask setup
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Output folder for generated images
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model: SD3 backbone + preprocessor
backbone = keras_hub.models.StableDiffusion3Backbone.from_preset(
    "stable_diffusion_3_medium", image_shape=(128, 128, 3), dtype="float16"
)
preprocessor = keras_hub.models.StableDiffusion3TextToImagePreprocessor.from_preset(
    "stable_diffusion_3_medium"
)
text_to_image = keras_hub.models.StableDiffusion3TextToImage(backbone, preprocessor)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Generate 128x128 image from prompt
    images = text_to_image.generate(prompt, batch_size=1)
    image = Image.fromarray(images[0])

    # Save to disk
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    image.save(filepath)

    return jsonify({"image_url": f"/{OUTPUT_DIR}/{filename}"})

@app.route(f'/{OUTPUT_DIR}/<filename>')
def serve_image(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
