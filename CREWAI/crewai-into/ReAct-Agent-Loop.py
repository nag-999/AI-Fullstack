from litellm import completion
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


class ReActManualExecutionAgent:
    def __init__(self, model="openai/gpt-4o", temperature=0, system_prompt="You are a helpful assistant."):
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.history = []

        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

    def generate_response(self, prompt):
        if prompt:
            self.history.append({"role": "user", "content": prompt})
        result = self.invoke()
        self.history.append({"role": "assistant", "content": result})
        print(f"\nMessages History: {self.history}\n")
        return result

    def invoke(self):
 
        response = completion(
            model=self.model,
            messages=self.history,
            temperature=self.temperature,
            api_key=API_KEY
        )
        assistant_message = response.choices[0].message['content']
        return assistant_message
    
    def agent_loop(self, query, system_prompt=""):
        my_agent = ReActManualExecutionAgent(system_prompt=system_prompt)
        available_tools = {
            "math": self.math,
            "lookup_population": self.lookup_population
        }

        current_prompt = query
        previous_step=""

        while "ANSWER" not in current_prompt:
            llm_response = my_agent.generate_response(current_prompt)
            print(f"Agent Response: {llm_response}")

            if "Answer" in llm_response:
                break
            elif "Thought" in llm_response:
                previous_step = "Thought"
                current_prompt = ""
            elif "PAUSE" in llm_response and previous_step == "Thought":
                previous_step = "PAUSE"
                current_prompt = ""
                continue
            elif "Action" in llm_response:
                previous_step = "Action"
                pattern = r"Action:\s*(\w+):\s*(.+)"
                match = re.search(pattern, llm_response)
                if match:
                    chosen_tool = match.group(1)
                    tool_input = match.group(2).strip()
                    if chosen_tool in available_tools:
                        tool_result = available_tools[chosen_tool](tool_input)
                        current_prompt = f"Observation: {tool_result}"
                    else:
                        current_prompt = f"Observation: Tool '{chosen_tool}' not found. Retry the action"
    
    def math(self, expression):
        try:
            result =    eval(expression)
            return str(result)
        except Exception as e:
            return f"Error in math evaluation: {str(e)}"
    
    def lookup_population(self, country):
        population_data = {
            "USA": "331 million",
            "India": "1.4 billion",
            "China": "1.4 billion",
            "Brazil": "213 million"
        }
        return population_data.get(country, "Population data not found for the specified country.") 
    
system_prompt = """You are an intelligent agent that can perform actions using tools to answer user queries.
You have access to the following tools:
1. math: Use this tool to perform mathematical calculations. Input should be a valid mathematical expression.
2. lookup_population: Use this tool to look up the population of a given country. Input
    should be the name of the country.
    When you need to use a tool, respond with the format:   
Action: <tool_name>: <input>
    After receiving the observation, you can continue your reasoning or provide the final answer in the format:
ANSWER: <your answer>   
    Always think step-by-step and use the tools wisely to arrive at the correct answer.
"""
agent = ReActManualExecutionAgent(system_prompt=system_prompt)
query = "What is the population of India plus 100 million?" 
response = agent.agent_loop(query, system_prompt=system_prompt)
print(f"\nFinal Response: {response}\n")