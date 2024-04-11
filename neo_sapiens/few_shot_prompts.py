from typing import List

# Example usage
data = """
{
    "plan": ["Step 1", "Step 2", "Step 3"],
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
    "agents": [
        {
            "name": "Room Management Agent",
            "system_prompt": "Automate room assignments, minibar restocking, and housekeeping schedules"
        },
        {
            "name": "Guest Services Agent",
            "system_prompt": "Handle check-ins, check-outs, guest requests, and complaints efficiently"
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


def merge_fewshots_into_str(
    plan: List[str] = [data, data1, data2, data3, data5]
) -> str:
    """
    Merge a list of plans into a single string.

    Args:
        plan (List[str]): A list of plans to be merged.

    Returns:
        str: The merged plans as a single string.
    """
    return "\n".join(plan)


self_driving_car_prompt = """

{
    "plan": [
        (
            "Step 1: Create agents specialized in different areas"
            " like computer vision, sensor fusion, controls,"
            " planning, etc."
        ),
        (
            "Step 2: Have the team leader agent decompose the overall"
            " self-driving task into sub-problems and assign them to"
            " the specialized agents"
        ),
        (
            "Step 3: Have each agent focus on solving their specific"
            " sub-problem using the latest AI techniques"
        ),
        (
            "Step 4: Have agents coordinate solutions with each other"
            " through the team leader to make sure components work"
            " together"
        ),
        (
            "Step 5: Integrate components into a complete"
            " self-driving system and validate performance through"
            " simulation and real-world testing"
        ),
    ],
    "agents": [
        {
            "name": "Computer Vision Agent",
            "system_prompt": (
                "Create an AI agent specialized in computer vision"
                " for self-driving cars, focused on object detection,"
                " segmentation and tracking using deep learning"
                " models like convolutional neural networks."
                " Coordinate with other agents through the team"
                " leader."
            ),
        },
        {
            "name": "Sensor Fusion Agent",
            "system_prompt": (
                "Create an AI agent specialized in sensor fusion for"
                " self-driving cars, focused on combining camera,"
                " radar and lidar data into a consistent 3D"
                " representation of the environment. Coordinate with"
                " other agents through the team leader."
            ),
        },
    ],
}


"""


def orchestrator_prompt_agent(objective: str):
    prompt = (
        "Create an instruction prompt for an swarm orchestrator to"
        " create a series of personalized, agents for the following"
        f" objective: {objective} to decompose a very complicated"
        " problem or tasks, the orchestrator is the team leader."
        " Teach the orchestrator how to decompose the tasks to very"
        " certain agents with names, and system prompts, we need the"
        " plan, with a step by stpe instructions, number of agents,"
        " and a list of agents with a name, system prompt for each,"
        " and then the rules of the swarm,  compact the prompt, and"
        " say only return JSON data in markdown and nothing"
        f" else.Follow the schema here: {data} *############ Here are"
        f" some examples:{data5} and another example{data3} "
    )
    return str(prompt)


boss_sys_prompt = (
    "You're the Swarm Orchestrator, like a project manager of a"
    " bustling hive. When a task arises, you tap into your network of"
    " worker agents who are ready to jump into action. Whether it's"
    " organizing data, handling logistics, or crunching numbers, you"
    " delegate tasks strategically to maximize efficiency. Picture"
    " yourself as the conductor of a well-oiled machine,"
    " orchestrating the workflow seamlessly to achieve optimal"
    " results with your team of dedicated worker agents."
)


def select_workers(agents: str, task: str):
    return (
        f"These are the agents available for the task: {task} Agents"
        f" available: {agents}"
    )
