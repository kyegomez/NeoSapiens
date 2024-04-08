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
