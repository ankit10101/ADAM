from dotenv import load_dotenv
from typing import List

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from src.adam.tools.create_gtm_ga4_event_tag_tool import create_a_gtm_ga4_event_tag
from src.adam.tools.fetch_network_requests_tool import (
    fetch_the_network_requests_on_page_load,
)
from src.adam.tools.get_ga4_report_tool import get_a_ga4_report
from src.adam.tools.run_js_code_tool import run_a_js_code_on_a_web_page

from datetime import datetime

# ---------- Agentcore imports --------------------
from bedrock_agentcore.runtime import BedrockAgentCoreApp


# ENV + LLM setup
load_dotenv(override=True)
# llm = LLM(model="gemini/gemini-2.0-flash", temperature=0)
llm = LLM(
    model="bedrock/arn:aws:bedrock:ap-south-1:501931553097:inference-profile/apac.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0,
)


# CrewAI Agent Setup
@CrewBase
class WebAnalyticsAutomationCrew:
    """
    CrewAI crew for automating web analytics workflows.

    This class sets up agents and tasks for digital analytics automation,
    including GTM/GA4 event tagging, network request fetching, JS execution,
    and GA4 reporting. Uses Anthropic Claude Sonnet via AWS Bedrock as the LLM.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def adam(self) -> Agent:
        """
        Defines the main agent 'adam' for web analytics automation.

        Returns:
            Agent: Configured CrewAI agent with relevant tools and LLM.
        """
        return Agent(
            config=self.agents_config["adam"],
            verbose=True,
            tools=[
                run_a_js_code_on_a_web_page,
                create_a_gtm_ga4_event_tag,
                fetch_the_network_requests_on_page_load,
                get_a_ga4_report,
            ],
            llm=llm,
        )

    @task
    def web_analytics_automation_task(self) -> Task:
        """
        Defines the main task for web analytics automation.

        Returns:
            Task: CrewAI task configuration for automation.
        """
        return Task(config=self.tasks_config["web_analytics_automation_task"])

    @crew
    def crew(self) -> Crew:
        """
        Creates and returns the CrewAI crew for web analytics automation.

        Returns:
            Crew: Configured CrewAI crew with agents and tasks.
        """
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )


app = BedrockAgentCoreApp()


@app.entrypoint
def agent_invocation(payload):
    """
    Entrypoint handler for BedrockAgentCoreApp agent invocation.

    Args:
        payload (dict): Input payload containing the user prompt.

    Returns:
        dict: Result from CrewAI agent or error message.
    """
    print(f"Payload: {payload}")
    try:
        # Extract user message from payload with default
        user_message = payload.get("prompt", "Artificial Intelligence in Healthcare")
        print(f"Processing topic: {user_message}")

        # Use synchronous kickoff instead of async - this avoids all event loop issues
        result = (
            WebAnalyticsAutomationCrew()
            .crew()
            .kickoff(
                inputs={
                    "user_query": user_message,
                    "current_date": datetime.now().strftime(r"%d/%m/%Y"),
                }
            )
        )

        print("Result Raw:\n*******\n", result.raw)

        # Safely access json_dict if it exists
        if hasattr(result, "json_dict"):
            print("Result JSON:\n*******\n", result.json_dict)

        return {"result": result.raw}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    app.run()
