from typing_extensions import TypedDict
from typing import Optional, Annotated
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from  dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model='gpt-4.1-mini',
    model_provider='openai'
)



class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    print("\n\n this message from chatbot node", state)
    response = llm.invoke(state.get("messages", []))
    return {"messages": [response]}

def samplenode(state: State):
    print("\n\n this message from samplenode node", state)
    return {"messages": ["\\n this message from samplenode node"]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()
print("\n\n this message from invoke")
updated_state = graph.invoke(State({"messages": ["\\n my name is nag"]}))
print(updated_state)
