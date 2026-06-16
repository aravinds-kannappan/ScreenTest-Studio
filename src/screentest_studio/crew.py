import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	JinaScrapeWebsiteTool,
	ScrapeWebsiteTool
)






DEFAULT_MODEL = os.getenv("SCREENTEST_LLM_MODEL", "openai/gpt-4o-mini")


@CrewBase
class ScreentestStudioCrew:
    """ScreentestStudio crew"""

    
    @agent
    def brand_intake_specialist_reel_timeline_architect(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["brand_intake_specialist_reel_timeline_architect"],
            
            
            tools=[				JinaScrapeWebsiteTool(),
				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model=DEFAULT_MODEL,
                
                
            ),
            
        )
        
    
    @agent
    def synthetic_target_customer_persona_panel(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["synthetic_target_customer_persona_panel"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model=DEFAULT_MODEL,
                
                
            ),
            
        )
        
    
    @agent
    def content_surgeon_re_screen_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["content_surgeon_re_screen_specialist"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model=DEFAULT_MODEL,
                
                
            ),
            
        )
        
    

    
    @task
    def brand_intake_task(self) -> Task:
        return Task(
            config=self.tasks_config["brand_intake_task"],
            markdown=False,
            
            
        )
    
    @task
    def timeline_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["timeline_generation_task"],
            markdown=False,
            
            
        )
    
    @task
    def audience_screening_task(self) -> Task:
        return Task(
            config=self.tasks_config["audience_screening_task"],
            markdown=False,
            
            
        )
    
    @task
    def diagnosis_task(self) -> Task:
        return Task(
            config=self.tasks_config["diagnosis_task"],
            markdown=False,
            
            
        )
    
    @task
    def fix_and_re_screen_task(self) -> Task:
        return Task(
            config=self.tasks_config["fix_and_re_screen_task"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ScreentestStudio crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model=DEFAULT_MODEL),
        )

