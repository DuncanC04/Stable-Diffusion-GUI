from flask import Flask, render_template, request, jsonify
import os
import base64
from io import BytesIO
import logging
import numpy as np
from PIL import Image
import keras
import keras_hub

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Keras backend to JAX
os.environ["KERAS_BACKEND"] = "jax"

app = Flask(__name__, template_folder='.')

# Initialize the model
try:
    logger.info("Initializing Stable Diffusion 3 model...")
    backbone = keras_hub.models.StableDiffusion3Backbone.from_preset(
        "stable_diffusion_3_medium", 
        image_shape=(128, 128, 3), 
        dtype="float16"
    )
    preprocessor = keras_hub.models.StableDiffusion3TextToImagePreprocessor.from_preset(
        "stable_diffusion_3_medium"
    )
    text_to_image = keras_hub.models.StableDiffusion3TextToImage(backbone, preprocessor)
    logger.info("Model initialized successfully")
except Exception as e:
    logger.error(f"Error initializing model: {str(e)}")
    raise

def generate_image(prompt: str) -> bytes:
    """Generate an image from the given prompt."""
    try:
        # Generate the image
        generated_image = text_to_image.generate(prompt)
        
        # Convert numpy array to PIL Image
        if isinstance(generated_image, np.ndarray):
            if generated_image.ndim == 3:
                image = Image.fromarray(generated_image)
            elif generated_image.ndim == 4:
                image = Image.fromarray(np.concatenate(list(generated_image), axis=1))
        else:
            raise ValueError("Unsupported image format")
        
        # Convert PIL Image to bytes
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return buffered.getvalue()
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        logger.info(f"Generating image for prompt: {prompt}")
        image_data = generate_image(prompt)
        
        # Convert image data to base64
        img_str = base64.b64encode(image_data).decode()
        
        return jsonify({
            'image': img_str,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error in generate endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 