from typing import List

from pydantic import BaseModel, Field
from swarms import Agent, OpenAIChat
from swarms.utils.json_utils import base_model_to_json
from neo_sapiens.hass_schema import (
    data,
    data1,
    data2,
    data3,
    data5,
)
from neo_sapiens.main import browser, terminal
from swarms import SwarmNetwork
from swarms.utils.parse_code import extract_code_from_markdown

# Swarmnetowr
network = SwarmNetwork(api_enabled=True, logging_enabled=True)


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
    # Rules for the agents
    # rules: str = Field(
    #     ...,
    #     title="Rules for the agents",
    #     description="Rules for the agents",
    # )


def transform_schema_to_json(schema: BaseModel):
    json = schema.model_json_schema()
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
        # hass_schema.rules,
    )


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


def merge_rules_into_str(prompts: List[str]):
    """
    Merge a list of prompts into a single string.

    Args:
        prompts (List[str]): A list of prompts to be merged.

    Returns:
        str: The merged prompts as a single string.
    """
    return "\n".join(prompts)


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
            max_loops="auto",
            autosave=True,
            dashboard=False,
            verbose=True,
            stopping_token="<DONE>",
            interactive=True,
        )

        network.add_agent(out)

    return out


out = create_agents(agents)
# print(out)

# Use network
list_agents = network.list_agents()
print(list_agents)

# # Run the workflow on a task
# run = network.run_single_agent(
#     agent2.id, "What's your name?"
# )
# print(out)


def run_task(task: str = None):
    agent = Agent(
        agent_name="Swarm Orchestrator",
        system_prompt=None,
        llm=OpenAIChat(
            openai_api_key=None,
        ),
        max_loops="auto",
        autosave=True,
        dashboard=False,
        verbose=True,
        stopping_token="<DONE>",
        # interactive=True,
    )
    out = agent(task)
    json = extract_code_from_markdown(out)
    parsed_schema = parse_hass_schema(json)
    plan, number_of_agents, agents = parsed_schema
    agents = create_agents(agents)
    # Run the agents
    
    