#Packages
import os
os.environ["KERAS_BACKEND"] = "jax"
import base64
import io
from flask import Flask, request, jsonify, send_from_directory
import keras
import keras_hub
import numpy as np
from PIL import Image

#Load Stable Diffusion 3 model
#From Keras Example
backbone = keras_hub.models.StableDiffusion3Backbone.from_preset(
    "stable_diffusion_3_medium", image_shape=(256, 256, 3), dtype="float32"
)
preprocessor = keras_hub.models.StableDiffusion3TextToImagePreprocessor.from_preset(
    "stable_diffusion_3_medium"
)
text_to_image = keras_hub.models.StableDiffusion3TextToImage(backbone, preprocessor)

app = Flask(__name__) #Create Flask app

#Serve the static HTML file
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        #Generate image from prompt
        images = text_to_image.generate(prompt, num_images=1, seed=42)
        image_array = images[0]
        image = Image.fromarray(image_array)

        #Convert image to base64
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return jsonify({"image": img_base64})

    #Catch any errors
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
