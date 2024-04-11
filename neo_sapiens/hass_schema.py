import json
import os
import re
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from swarms import Agent, Anthropic, SwarmNetwork

from neo_sapiens.few_shot_prompts import (
    data,
    data1,
    data2,
    data3,
    orchestrator_prompt_agent,
)
from loguru import logger

# from neo_sapiens.chroma_db_s import ChromaDB

# Load environment variables
load_dotenv()

# Swarmnetowr
network = SwarmNetwork(api_enabled=True, logging_enabled=True)


# Initialize memory
# memory = ChromaDB(
#     metric="cosine",
#     output_dir="swarms",
#     limit_tokens=1000,
#     n_results=2,
#     verbose=False,
# )

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
    for agent in network.agent_pool:
        if agent.agent_name == name:
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
        logger.info("Error: Input string is None or empty.")
        return None, None, None

    # Attempt to extract JSON from markdown using regular expression
    json_pattern = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
    match = json_pattern.search(input_str)
    json_str = match.group(1).strip() if match else input_str.strip()
    # logger.info(json_str)

    # Attempt to parse the JSON string
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.info(f"Error: JSON decoding failed with message '{e}'")
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
        name = agent.name
        system_prompt = agent.system_prompt

        logger.info(
            f"Creating agent: {name} with system prompt:"
            f" {system_prompt}"
        )
        logger.info("\n")

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
            # long_term_memory=memory,
        )

        network.add_agent(out)

    return out


def print_agent_names(agents: list):
    for agent in agents:
        logger.info(agent.name)


# out = create_agents(agents)
# # logger.info(out)

# # # Use network
# # list_agents = network.list_agents()
# # logger.info(list_agents)

# # Run the workflow on a task
# run = network.run_single_agent(
#     agent2.id, "What's your name?"
# )
# logger.info(out)


def master_creates_agents(task: str):
    """
    Master function to create agents based on a task.

    Args:
        task (str): The task to be executed.

    Returns:
        None
    """
    system_prompt_daddy = orchestrator_prompt_agent(task)
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
        interactive=True,
        # long_term_memory=memory,
    )
    out = agent.run(task)
    out = str(out)
    logger.info(f"Output: {out}")
    out = parse_json_from_input(out)
    logger.info(str(out))
    plan, number_of_agents, agents = out
    logger.info(agents)
    logger.info(print_agent_names(agents))
    agents = create_agents(agents)
    logger.info(agents)
    return out, agents, plan


def message_metadata_log(task: str, message: str, agent, plan: str):
    """
    Create a document with metadata for a log message.

    Args:
        task (str): The task associated with the log message.
        message (str): The log message.
        agent: The agent object.
        plan (str): The plan associated with the log message.

    Returns:
        dict: A dictionary containing the log message metadata.
    """
    doc = {
        "message": message,
        "task": task,
        "agent_name": agent.agent_name,
        "plan": plan,
    }

    return doc


def run_swarm(task: str = None):
    """
    Run a task using the Swarm Orchestrator agent.

    Args:
        task (str): The task to be executed.

    Returns:
        None
    """
    create_agents, agents, plan = master_creates_agents(task)

    # Then the agents work on sequentially on the task
    task = {
        "task": task,
        "plan": create_agents,
    }
    # Now transform dict into string
    task = json.dumps(task)
    task = str(task)

    # Run the workflow on a task
    for agent in agents:
        run = agent.run(task)
        passed = agent.run(run)

    return passed


# out = run_task(
#     "Create a team of AI engineers to create an AI for a"
#     " self-driving car"
# )
# # logger.info(out)
