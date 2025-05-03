from PIL import Image, ImageOps
import io

def process_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    processed_img = ImageOps.invert(img)
    output_buffer = io.BytesIO()
    processed_img.save(output_buffer, format="PNG")
    return output_buffer.getvalue()