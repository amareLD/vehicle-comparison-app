from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# from vehicle_comparison_backend.tools.web_scraper import WebScraperTool, SriLankanCarSearchTool
# from vehicle_comparison_backend.tools.vehicle_comparison import VehicleComparisonTool
# from vehicle_comparison_backend.tools.vehicle_search import VehicleSearchTool
from vehicle_comparison_backend.tools.web_scraper import WebScraperTool, SriLankanCarSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class VehicleComparisonBackend():
    """VehicleComparisonBackend crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def vehicle_comparison_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['vehicle_comparison_agent'],
            tools=[WebScraperTool()],
            verbose=True
        )

    @agent
    def sri_lankan_ad_finder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sri_lankan_ad_finder_agent'],
            tools=[SriLankanCarSearchTool()],
            verbose=True
        )

    @agent
    def ad_details_extractor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ad_details_extractor_agent'],
            tools=[WebScraperTool()],
            verbose=True
        )

    @task
    def vehicle_comparison_task(self) -> Task:
        return Task(
            config=self.tasks_config['vehicle_comparison_task'],
            agent=self.vehicle_comparison_agent()
        )

    @task
    def sri_lankan_ad_finder_task(self) -> Task:
        return Task(
            config=self.tasks_config['sri_lankan_ad_finder_task'],
            agent=self.sri_lankan_ad_finder_agent()
        )

    @task
    def ad_details_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['ad_details_extraction_task'],
            agent=self.ad_details_extractor_agent(),
            context=[self.sri_lankan_ad_finder_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Vehicleanalyst crew"""
        return Crew(
            agents=self.agents(),
            tasks=self.tasks(),
            process=Process.sequential,
            verbose=2,
        )