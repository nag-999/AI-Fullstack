from litellm import completion
import os
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
    
my_agent = ReActManualExecutionAgent()
response = my_agent.generate_response("Write a python function to check if the given string has valid parentheses.")
print(response)