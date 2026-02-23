from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerpApiGoogleSearchTool
from research_output import ResearchFindingJSONOutput
from dotenv import load_dotenv
import os
import certifi

# Fix SSL certificate verification for Windows
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()


@CrewBase
class ResearchCrew:
    """A crew for conducting research, summarizing findings, and fact-checking"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        load_dotenv()
        self.search_tool = SerpApiGoogleSearchTool(api_key=os.getenv("SERPAPI_API_KEY"))

    @agent
    def research_agent(self) -> Agent:
        return Agent(config=self.agents_config['research_agent'],
                     tools=[self.search_tool])

    @agent
    def summarization_agent(self) -> Agent:
        return Agent(config=self.agents_config['summarization_agent'])

    @agent
    def fact_checker_agent(self) -> Agent:
        return Agent(config=self.agents_config['fact_checker_agent'],
                     tools=[self.search_tool])

    
    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'],
                    tools=[self.search_tool])

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'],
            output_pydantic=ResearchFindingJSONOutput
        )

    @task
    def fact_checking_task(self) -> Task:
        return Task(config=self.tasks_config['fact_checking_task'],
                    tools=[self.search_tool])
  
    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents,
                    tasks=self.tasks,
                    process=Process.sequential)