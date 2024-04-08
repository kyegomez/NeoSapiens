from pydantic import BaseModel, Field
from typing import List
from swarms.utils.json_utils import base_model_to_json

class AgentSchema(BaseModel):
    name: str = Field(
        ...,
        title="Name of the agent",
    )
    system_prompt: str = Field(
        ...,
        title = "System prompt for the agent",
    )


class HassSchema(BaseModel):
    plan: List[str] = Field(
        ...,
        title="Plan to solve the input problem",
    )
    number_of_agents: int = Field(
        ...,
        title="Number of agents to use for the problem",
    )
    
    agents: List[AgentSchema] = Field(
        ...,
        title="List of agents to use for the problem",
    )
    
    
    
json = HassSchema.model_json_schema()
json = base_model_to_json(HassSchema)
# print(json)



def parse_hass_schema(data: str) -> tuple:
    parsed_data = eval(data)
    hass_schema = HassSchema(**parsed_data)
    return hass_schema.plan, hass_schema.number_of_agents, hass_schema.agents

# Example usage
data = '''
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
'''

parsed_schema = parse_hass_schema(data)
print(parsed_schema)
