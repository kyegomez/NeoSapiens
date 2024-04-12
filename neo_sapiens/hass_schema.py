import json
import os
import re
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from swarms import Agent, Anthropic, SwarmNetwork, tool

from neo_sapiens.few_shot_prompts import (
    data,
    data1,
    data2,
    data3,
    orchestrator_prompt_agent,
    select_workers,
    boss_sys_prompt,
)
from loguru import logger
from neo_sapiens.tools_preset import (
    terminal,
    browser,
    file_editor,
    create_file,
)

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

    # Attempt to parse the JSON string
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.info(f"Error: JSON decoding failed with message '{e}'")
        return None, None, None

    hass_schema = HassSchema(**data)
    return (
        hass_schema.plan,
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
) -> List[Agent]:
    """
    Create and initialize agents based on the provided AgentSchema objects.

    Args:
        agents (List[AgentSchema]): A list of AgentSchema objects containing agent information.

    Returns:
        List[Agent]: The initialized Agent objects.

    """
    agent_list = []
    for agent in agents:
        name = agent.name
        system_prompt = agent.system_prompt

        logger.info(
            f"Creating agent: {name} with system prompt:"
            f" {system_prompt}"
        )

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
            tools=[browser, terminal, create_file, file_editor],
        )

        network.add_agent(out)
        agent_list.append(out)

    return agent_list


def print_agent_names(agents: list):
    for agent in agents:
        logger.info(f"Agent Name: {agent.agent_name}")


@tool
def send_task_to_network_agent(name: str, task: str):
    """
    Send a task to a network agent.

    Args:
        name (str): The name of the agent.
        task (str): The task to be sent to the agent.

    Returns:
        str: The response from the agent.
    """
    logger.info(f"Adding agent {name} as a tool")
    agent_id = find_agent_id_by_name(name)
    out = network.run_single_agent(agent_id, task)
    return out


def master_creates_agents(task: str, *args, **kwargs):
    """
    Master function to create agents based on a task.

    Args:
        task (str): The task to be executed.

    Returns:
        None
    """
    system_prompt_daddy = orchestrator_prompt_agent(task)

    # Create the agents
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
        *args,
        **kwargs,
    )

    # Call the agents [ Main Agents ]
    # Create the agents
    boss = Agent(
        agent_name="Swarm Orchestrator",
        system_prompt=boss_sys_prompt,
        llm=Anthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=4000,
        ),
        max_loops="auto",
        autosave=True,
        dashboard=False,
        verbose=True,
        stopping_token="<DONE>",
        interactive=True,
        *args,
        **kwargs,
    )

    # Task 1: Run the agent and parse the output
    logger.info("Creating the workers ...")
    out = agent.run(str(task))
    # logger.info(f"Output: {out}")
    out = parse_json_from_input(out)
    json_agentic_output = out
    # logger.info(str(out))
    plan, agents = out

    # Task 2: Print agent names and create agents
    # logger.info(agents)
    # logger.info("Creating agents...")
    agents = create_agents(agents)

    # Send JSON of agents to boss
    boss.add_message_to_memory(
        select_workers(json_agentic_output, task)
    )

    # Task 3: Now add the agents as tools
    boss.add_tool(send_task_to_network_agent)

    # Run the boss:
    out = boss.run(task)

    return out  # , agents, plan


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


def run_swarm(task: str = None, *args, **kwargs):
    """
    Run a task using the Swarm Orchestrator agent.

    Args:
        task (str): The task to be executed.

    Returns:
        None
    """
    out = master_creates_agents(task, *args, **kwargs)
    # return passed
    return out
