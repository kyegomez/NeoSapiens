import json
import os
import re
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from swarms import Agent, Anthropic, SwarmNetwork

from few_shot_prompts import (
    data,
    data1,
    data2,
    data3,
    orchestrator_prompt_agent,
)

# Load environment variables
load_dotenv()

# Swarmnetowr
network = SwarmNetwork(api_enabled=True, logging_enabled=True)


# def tool_router(tool: str, *args, **kwargs):
#     if "terminal" in tool:
#         return terminal(*args, **kwargs)
#     elif "browser" in tool:
#         return browser(*args, **kwargs)


def find_agent_id_by_name(name: str):
    """
    Find an agent's ID by its name.

    Args:
        name (str): The name of the agent.

    Returns:
        str: The ID of the agent.
    """
    agents = network.list_agents()
    for agent in agents:
        if agent.name == name:
            return agent.id


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


# import json
def parse_json_from_input(input_str):
    # Validate input is not None or empty
    if not input_str:
        print("Error: Input string is None or empty.")
        return None, None, None

    # Attempt to extract JSON from markdown using regular expression
    json_pattern = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
    match = json_pattern.search(input_str)
    json_str = match.group(1).strip() if match else input_str.strip()
    # print(json_str)

    # Attempt to parse the JSON string
    try:
        data = json.loads(json_str)
        # print(str(data))
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding failed with message '{e}'")
        return None, None, None

    hass_schema = HassSchema(**data)
    return (
        hass_schema.plan,
        hass_schema.number_of_agents,
        hass_schema.agents,
        # hass_schema.rules,
    )


# You can test the function with a markdown string similar to the one provided.


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


# parsed_schema = parse_hass_schema(data5)
# plan, number_of_agents, agents = parsed_schema


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
            llm=Anthropic(
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            ),
            max_loops=1,
            autosave=True,
            dashboard=False,
            verbose=True,
            stopping_token="<DONE>",
            interactive=True,
        )

        network.add_agent(out)

    return out


# out = create_agents(agents)
# # print(out)

# # # Use network
# # list_agents = network.list_agents()
# # print(list_agents)

# # Run the workflow on a task
# run = network.run_single_agent(
#     agent2.id, "What's your name?"
# )
# print(out)


def run_task(task: str = None):
    """
    Run a task using the Swarm Orchestrator agent.

    Args:
        task (str): The task to be executed.

    Returns:
        None
    """
    system_prompt_daddy = orchestrator_prompt_agent(task)
    # print(system_prompt_daddy)
    agent = Agent(
        agent_name="Swarm Orchestrator",
        system_prompt=system_prompt_daddy,
        llm=Anthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=4000,
        ),
        max_loops=1,
        autosave=True,
        dashboard=False,
        verbose=True,
        stopping_token="<DONE>",
        # interactive=True,
    )
    out = agent.run(task)
    # print(out)
    out = str(out)
    print(f"Output: {out}")
    out = parse_json_from_input(out)
    print(str(out))
    plan, number_of_agents, agents = out
    print(agents)
    agents = create_agents(agents)
    print(agents)
    # return agents
    # print(out)
    # json_template = extract_code_from_markdown(str(out))
    # print(json_template)
    # parsed_schema = parse_json_from_markdown(json_template)
    # plan, number_of_agents, agents = parsed_schema
    # print(f"Plan: {agents}")
    # # agents = create_agents(agents)
    # print(agents)
    # return agents
    return out


out = run_task(
    "Create a team of AI engineers to create an AI for a"
    " self-driving car"
)
# print(out)
