import base64
import numpy as np
from PIL import Image
from keras_cv.models import StableDiffusion

model = StableDiffusion(img_height=128, img_width=128)

def generate_images():
    prompts = ["a small cartoon cat", "a small cartoon dog"]
    images = model.text_to_image(prompt=prompts, batch_size=2)
    encoded = []
    for i, img_array in enumerate(images):
        image = Image.fromarray(np.array(img_array).astype("uint8"))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        encoded.append({"id": f"img_{i}", "data": base64_img})
    return encoded