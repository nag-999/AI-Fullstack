from pydantic import BaseModel, Field

class ResearchFindingJSONOutput(BaseModel):
    introduction: str = Field(..., description="Introduction of the research finding")
    key_insights: str = Field(..., description="Key insights from recent reports")
