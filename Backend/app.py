from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Create output directory
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Stable Diffusion pipeline (you can change model if needed)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    # Generate image at 128x128 resolution
    image = pipe(prompt, height=128, width=128).images[0]

    # Save image to disk
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    image.save(filepath)

    return jsonify({"image_url": f"/{OUTPUT_DIR}/{filename}"})

@app.route(f'/{OUTPUT_DIR}/<filename>')
def serve_image(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
