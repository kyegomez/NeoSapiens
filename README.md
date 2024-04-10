[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Neo Sapiens


## install
`$ pip install -U swarms neo-sapiens`


## usage
```python
from neo_sapiens import run_swarm

# Run the swarm
out = run_swarm("Create a self-driving car system using a team of AI agents")
print(out)
```

# Todo
- [ ] Add tool processing

- [ ] Add tool router

- [ ] Add rules processing to map to each agent

- [ ] Prompt for swarm orchestrator to make the children workers in JSON

- [ ] Prompt to create functions with a tool decorator above the function with specific types and documentation. Create a tool for this: {input}, and create the functions in python with a tool decorator on top of the function with specific types and documentation with docstrings

- [ ] Logic to add each agent to a swarm network

- [ ] Add memory to boss agent using Chromadb

- [ ] Add agents as tools after the boss creates them

# License
MIT
