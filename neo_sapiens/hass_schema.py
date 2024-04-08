from pydantic import BaseModel, Field
from typing import List
from swarms.utils.json_utils import base_model_to_json
from swarms import Agent, OpenAIChat
from neo_sapiens.main import terminal, browser


def tool_router(tool: str, *args, **kwargs):
    if "terminal" in tool:
        return terminal(*args, **kwargs)
    elif "browser" in tool:
        return browser(*args, **kwargs)


class ToolSchema(BaseModel):
    tool: str = Field(
        ...,
        title="Tool name",
        description="Either `browser` or `terminal`",
    )


class AgentSchema(BaseModel):
    name: str = Field(
        ...,
        title="Name of the agent",
        description="Name of the agent",
    )
    system_prompt: str = Field(
        ...,
        title="System prompt for the agent",
        description="System prompt for the agent",
    )
    # tools: List[ToolSchema] = Field(
    #     ...,
    #     title="Tools available to the agent",
    #     description="Either `browser` or `terminal`",
    # )
    # task: str = Field(
    #     ...,
    #     title="Task assigned to the agent",
    #     description="Task assigned to the agent",
    # )
    # TODO: Add more fields here such as the agent's language model, tools, etc.


class HassSchema(BaseModel):
    plan: List[str] = Field(
        ...,
        title="Plan to solve the input problem",
        description="List of steps to solve the problem",
    )
    number_of_agents: int = Field(
        ...,
        title="Number of agents to use for the problem",
        description="Number of agents to use for the problem",
    )
    agents: List[AgentSchema] = Field(
        ...,
        title="List of agents to use for the problem",
        description="List of agents to use for the problem",
    )


json = HassSchema.model_json_schema()
json = base_model_to_json(HassSchema)
print(f"JSON Schema: {json}")


def parse_hass_schema(data: str) -> tuple:
    """
    Parses the Home Assistant schema data and returns a tuple containing the plan,
    number of agents, and the agents themselves.

    Args:
        data (str): The Home Assistant schema data to be parsed.

    Returns:
        tuple: A tuple containing the plan, number of agents, and the agents themselves.
    """
    parsed_data = eval(data)
    hass_schema = HassSchema(**parsed_data)
    return (
        hass_schema.plan,
        hass_schema.number_of_agents,
        hass_schema.agents,
    )


# Example usage
data = """
{
    "plan": ["Step 1", "Step 2", "Step 3"],
    "number_of_agents": 5,
    "agents": [
        {
            "name": "Agent 1",
            "system_prompt": "Prompt 1"
        },
        {
            "name": "Agent 2",
            "system_prompt": "Prompt 2"
        }
    ]
}
"""

# AI Research Team 1
data1 = """
{
    "plan": ["Data Collection", "Data Cleaning", "Model Training", "Model Evaluation"],
    "number_of_agents": 3,
    "agents": [
        {
            "name": "Data Agent",
            "system_prompt": "Collect and clean data"
        },
        {
            "name": "Training Agent",
            "system_prompt": "Train the model"
        },
        {
            "name": "Evaluation Agent",
            "system_prompt": "Evaluate the model"
        }
    ]
}
"""

# AI Research Team 2
data2 = """
{
    "plan": ["Literature Review", "Hypothesis Formulation", "Experiment Design", "Data Analysis", "Paper Writing"],
    "number_of_agents": 5,
    "agents": [
        {
            "name": "Review Agent",
            "system_prompt": "Review the literature"
        },
        {
            "name": "Hypothesis Agent",
            "system_prompt": "Formulate the hypothesis"
        },
        {
            "name": "Design Agent",
            "system_prompt": "Design the experiment"
        },
        {
            "name": "Analysis Agent",
            "system_prompt": "Analyze the data"
        },
        {
            "name": "Writing Agent",
            "system_prompt": "Write the paper"
        }
    ]
}
"""

# AI Research Team 3
data3 = """
{
    "plan": ["Problem Identification", "Solution Design", "Implementation", "Testing", "Deployment"],
    "number_of_agents": 4,
    "agents": [
        {
            "name": "Identification Agent",
            "system_prompt": "Identify the problem"
        },
        {
            "name": "Design Agent",
            "system_prompt": "Design the solution"
        },
        {
            "name": "Implementation Agent",
            "system_prompt": "Implement the solution"
        },
        {
            "name": "Deployment Agent",
            "system_prompt": "Deploy the solution"
        }
    ]
}
"""


data5 = """
{
    "plan": ["Room Management", "Guest Services", "Reservations Handling", "Facility Maintenance", "Staff Coordination"],
    "number_of_agents": 5,
    "agents": [
        {
            "name": "Room Management Agent",
            "system_prompt": "Automate room assignments, minibar restocking, and housekeeping schedules"
        },
        {
            "name": "Guest Services Agent",
            "system_prompt": "Handle check-ins, check-outs, guest requests, and complaints efficiently"
            "tool": "browser"
        },
        {
            "name": "Reservations Agent",
            "system_prompt": "Manage room bookings, table reservations, and special requests"
        },
        {
            "name": "Maintenance Agent",
            "system_prompt": "Schedule and track maintenance tasks for facilities and rooms"
        },
        {
            "name": "Staff Coordination Agent",
            "system_prompt": "Optimize staff schedules, task assignments, and workload distribution"
        }
    ]
}
"""


def merge_plans_into_str(
    plan: List[str] = [data, data1, data2, data3]
) -> str:
    """
    Merge a list of plans into a single string.

    Args:
        plan (List[str]): A list of plans to be merged.

    Returns:
        str: The merged plans as a single string.
    """
    return "\n".join(plan)


parsed_schema = parse_hass_schema(data5)
plan, number_of_agents, agents = parsed_schema


def create_agents(
    agents: List[AgentSchema],
):
    """
    Create and initialize agents based on the provided AgentSchema objects.

    Args:
        agents (List[AgentSchema]): A list of AgentSchema objects containing agent information.

    Returns:
        Agent: The initialized Agent object.

    """
    for agent in agents:
        print(agent)
        name = agent.name
        system_prompt = agent.system_prompt
        print(agent.name)
        print(agent.system_prompt)
        print("\n")

        out = Agent(
            agent_name=name,
            system_prompt=system_prompt,
            llm=OpenAIChat(
                openai_api_key="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",
            ),
            max_loops=1,
            autosave=True,
            dashboard=False,
            verbose=True,
            stopping_token="<DONE>",
            interactive=True,
        )

        out("What is your name")

    return out


out = create_agents(agents)
print(out)
