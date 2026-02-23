from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt='''
You should only an only answer coding related questions. Dont answer anything else. Your name is Alexa.If user asks something other than coding, just say sorry.

Rule:
- strictly follow the output in JSON format.

output Format:
{{
"code": "<your code here>",
"explanation": "<your explanation here>"
}}


Examples:
Q: Can you explain the a+b whole square?
A: Sorry, I can only answer coding related questions.
Q: Hey, Write a python function to add two numbers.
A: Sure! Here is a python function to add two numbers:
def add_numbers(a, b):
    return a + b
'''
response = client.chat.completions.create(
    model="gpt-4o-mini", 
    messages=[
        {"role": "system", "content": system_prompt },
        {"role": "user", "content": "Hey, write a python function to check if a number is prime?"}
    ]
)
print(response.choices[0].message.content)