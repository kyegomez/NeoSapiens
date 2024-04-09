
{
  "plan": [
    "Step 1: Create agents specialized in different areas like computer vision, sensor fusion, controls, planning, etc.",
    "Step 2: Have the team leader agent decompose the overall self-driving task into sub-problems and assign them to the specialized agents", 
    "Step 3: Have each agent focus on solving their specific sub-problem using the latest AI techniques",
    "Step 4: Have agents coordinate solutions with each other through the team leader to make sure components work together",
    "Step 5: Integrate components into a complete self-driving system and validate performance through simulation and real-world testing"
  ],
  "number_of_agents": 5,
  "agents": [
    {
      "name": "Computer Vision Agent",
      "system_prompt": "Create an AI agent specialized in computer vision for self-driving cars, focused on object detection, segmentation and tracking using deep learning models like convolutional neural networks. Coordinate with other agents through the team leader."
    },
    { 
      "name": "Sensor Fusion Agent",
      "system_prompt": "Create an AI agent specialized in sensor fusion for self-driving cars, focused on combining camera, radar and lidar data into a consistent 3D representation of the environment. Coordinate with other agents through the team leader."
    }
  ]
}