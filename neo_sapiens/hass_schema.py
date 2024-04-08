from pydantic import BaseModel, Field
from typing import List
from swarms.utils.json_utils import base_model_to_json
from swarms import Agent

# from swarms import OpenAIChat


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


def merge_plans_into_str(plan: List[str]) -> str:
    return "\n".join(plan)


parsed_schema = parse_hass_schema(data)
plan, number_of_agents, agents = parsed_schema


def create_agents(
    agents: List[AgentSchema],
):
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
            # llm=OpenAIChat(),
            max_loops="auto",
            autosave=True,
            dashboard=False,
            verbose=True,
            stopping_token="<DONE>",
            interactive=True,
        )

    return out


out = create_agents(agents)
print(out)
