from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("Google_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta")
response = client.chat.completions.create(
    model="gemini-2.5-flash", 
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ]
)
print(response.choices[0].message.content)