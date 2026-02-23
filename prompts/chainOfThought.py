from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_prompt= '''
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done.The PLAN can be multpitple steps.
Once you think enough PLAN has been donbe, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives input), PLAN (That can be multiple steps), OUTPUT (which is going to displayed to the user)

Output JSON Format:
{"step": "START|PLAN|OUTPUT", "content": "string"}


Examples:
START: Hey, Can you solve 2+3*5/10?
THOUGHT: {"step": "START", "content": "To solve 2+3*5/10, I need to follow the order of operations (PEMDAS/BODMAS). First, I will handle the multiplication and division, then the addition."}
PLAN: {"step": "PLAN", "content": "First, I will solve the multiplication 3*5=15. Then I will divide 15 by 10 to get 1.5. Finally, I will add 2 + 1.5 to get the final answer 3.5."}
OUTPUT: {"step": "OUTPUT", "content": "The final answer to 2+3*5/10 is 3.5."}
'''


message_history = [
      {"role":"system", "content": system_prompt }
]

user_query = input("Enter your query: ")

message_history.append({"role":"user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format = {"type": "json_object"},
        messages= message_history
    )   

    raw_result = response.choices[0].message.content
    parsed_result = json.loads(raw_result)
    message_history.append({"role":"assistant", "content": raw_result})

    if parsed_result['step'] == 'PLAN':
        print("PLAN: ", parsed_result['content'])
        continue

    if parsed_result['step'] == 'OUTPUT':
        print("OUTPUT: ", parsed_result['content'])
        break

# response = client.chat.completions.create(
#     model="gpt-4o-mini", 
#     response_format = {"type": "json_object"},
#     messages=[
#         {"role":"system", "content": system_prompt },
#         {"role":"user", "content": "Hey, Can you add n numbers in python?"},

#         {"role": "assistant", "content": json.dumps({"step": "START", "content": "To add n numbers in Python, I can provide a method that uses either a loop or the built-in sum function. First, I need to determine how the numbers will be provided (e.g., from user input, a list, etc.)."})},
#         {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I will outline a solution using the built-in sum function for simplicity. First, I will prompt the user for input on how many numbers they want to add. Then, I can either ask for each number individually or provide a method to input them in one line. Finally, I will calculate the sum of the numbers and display the result."})},
#     ]
# )

# Print the response content
#print(response.choices[0].message.content)