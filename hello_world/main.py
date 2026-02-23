from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()


client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini", 
    messages=[
        {"role": "system", "content": "You are an expert in maths and only answer maths related questions. That if the query is not related to Maths, just say sorry i can only answer maths related questions."},
        {"role": "user", "content": "Hey, Can you help me solve (a+b)^2?"}
    ]
)
print(response.choices[0].message.content)