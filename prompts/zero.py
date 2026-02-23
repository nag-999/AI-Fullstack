from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt='You should only an only answer coding related questions. Dont answer anything else. Your name is Alexa.If user asks something other than coding, just say sorry.'
response = client.chat.completions.create(
    model="gpt-4o-mini", 
    messages=[
        {"role": "system", "content": system_prompt },
        {"role": "user", "content": "Hey, Can you tell me a coding joke?"}
    ]
)
print(response.choices[0].message.content)