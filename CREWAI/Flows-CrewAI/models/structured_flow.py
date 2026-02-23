from pydantic import BaseModel

class StructuredFlow(BaseModel):
    task: str = "None"
    status: str = "None"
    recommendation: str = "None"
    genre: str = "None"
