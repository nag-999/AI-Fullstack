from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests
import os
load_dotenv()


class MyOutPutModel(BaseModel):
    step: str = Field(..., description="The current step: START, PLAN, OUTPUT, TOOL, OBSERVE.")
    content: Optional[str] = Field(None, description="The content related to the current step.")
    tool: Optional[str] = Field(None, description="The tool to be called, if any.")
    answer: Optional[str] = Field(None, description="The final answer to the user query.")
    input: Optional[str] = Field(None, description="The input params for the tool")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_command(cmd: str) -> str:
    try:
        result = os.system(cmd)
        return result
    except Exception as e:
        return str(e)

def get_weather(location:str) -> str:
    url=f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)
    if response.status_code != 200:
        return "Sorry, I couldn't fetch the weather data right now."
    return f"the weather is in {location} is {response.json()}"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}


system_prompt= '''
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done.The PLAN can be multpitple steps.
Once you think enough PLAN has been donbe, finally you can give an OUTPUT.
You can also call a tool if required from the tool list below.
for every tool call, you need to observe the result and then give the final OUTPUT.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives input), PLAN (That can be multiple steps), OUTPUT (which is going to displayed to the user)

Output JSON Format:
{"step": "START|PLAN|OUTPUT|TOOL", "content": "string"}

Available Tools:
- get_weather(location: str) -> str : Use this tool to get the current weather information for a given location.
- run_command(cmd: str) -> str : Use this tool to run a system command and get the output.


Example 1:
START: Hey, Can you solve 2+3*5/10?
THOUGHT: {"step": "START", "content": "To solve 2+3*5/10, I need to follow the order of operations (PEMDAS/BODMAS). First, I will handle the multiplication and division, then the addition."}
PLAN: {"step": "PLAN", "content": "First, I will solve the multiplication 3*5=15. Then I will divide 15 by 10 to get 1.5. Finally, I will add 2 + 1.5 to get the final answer 3.5."}
OUTPUT: {"step": "OUTPUT", "content": "The final answer to 2+3*5/10 is 3.5."}

Example 2:  
START: what is the weather in New York?
THOUGHT: {"step": "START", "content": "To provide the weather information for New York, I need to use the get_weather tool to fetch the current weather data."}
PLAN: {"step": "PLAN", "content": "I will call the get_weather tool with the location set to New York to get the current weather information."}
TOOL: {"step": "TOOL", "content": "get_weather('New York')"}
OBSERVE: {"step": "OBSERVE", "content": "<weather data returned by the tool>"}
OUTPUT: {"step": "OUTPUT", "content": "The current weather in New York is <weather data returned by the tool>."}

'''
message_history = [
      {"role":"system", "content": system_prompt }
]

user_query = input("Enter your query: ")

message_history.append({"role":"user", "content": user_query})

while True:
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format = MyOutPutModel,
        messages= message_history
    )   

    raw_result = response.choices[0].message.content
    parsed_result = response.choices[0].message.parsed
    message_history.append({"role":"assistant", "content": raw_result})

    if parsed_result.step == 'PLAN':
        print("PLAN: ", parsed_result.content)
        continue

    if parsed_result.step == 'OUTPUT':
        print("OUTPUT: ", parsed_result.content)
        break

    if parsed_result.step == "TOOL":
        tool_to_call = parsed_result.tool
        tool_input = parsed_result.input
        if not tool_to_call:
            print("No tool specified by the model. Skipping tool call.")
            continue
        print(f"🛠️: {tool_to_call} ({tool_input})")
        tool_response = available_tools[tool_to_call](tool_input)
        print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")
        message_history.append({ "role": "developer", "content": json.dumps(
            { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        ) })
        continue

def main():
    user_quesry = input("Enter your query: ")
    response = client.chat.completions.create(
        model="gpt-4o-mini",    
        messages=[
            {"role": "user", "content": user_quesry}
        ]
    )

    print(f":: {response.choices[0].message.content}")

