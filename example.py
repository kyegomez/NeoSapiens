import argparse
from neo_sapiens.hass_schema import run_swarm

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Run the swarm")

# Add arguments for team_task and task
parser.add_argument(
    "--team_task", type=str, help="The team task for the swarm"
)
parser.add_argument("--task", type=str, help="The task for the swarm")

# Parse the command line arguments
args = parser.parse_args()

# Run the swarm with the provided message, team_task, and task
out = run_swarm(args.team_task, args.task)
print(out)
