from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

def generate_hello_world():
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= "Hello, world!"
    )
    print(response.text)

if __name__ == "__main__":
    generate_hello_world()