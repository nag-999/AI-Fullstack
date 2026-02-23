from transformers import pipeline
from dotenv import load_dotenv
import os
load_dotenv()

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b",
                api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

messages = [
    {"role": "system", "content": "You are a helpful assistant that generates detailed image captions."},
    {"role": "user", "content": "Describe the content of the image in detail."}
]

image_path = "path_to_your_image.jpg"  # Replace with your image path
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read() 
    response = pipe(images=[image_bytes], messages=messages)    
    print(response[0]['generated_text'])


    