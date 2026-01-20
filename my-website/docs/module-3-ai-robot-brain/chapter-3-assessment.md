---
title: Chapter 3 Assessment - Intelligent Motion Planning with Nav2
sidebar_position: 6
---

# Chapter 3 Assessment - Intelligent Motion Planning with Nav2

## Multiple Choice Questions

1. What does Nav2 stand for?
   - A) Navigation 2
   - B) Navigational Algorithm Version 2
   - C) Networked Autonomous Vehicles 2
   - D) Neural Adaptive Vehicle System

2. Which of the following is NOT a level in the robot motion planning hierarchy?
   - A) Task planning
   - B) Path planning
   - C) Weather planning
   - D) Control

3. What is the main purpose of recovery behaviors in Nav2?
   - A) To increase robot speed
   - B) To handle exceptional situations and get unstuck
   - C) To improve sensor accuracy
   - D) To reduce battery consumption

## Short Answer Questions

4. Explain the difference between global and local planners in the Nav2 framework.

5. Describe the three main components of the perception-action loop.

6. What are the main types of obstacles that robots must handle, and how does Nav2 address them?

## Scenario-Based Questions

7. A robot is navigating through a hospital corridor when a medical cart is left in the middle of the hallway. How would Nav2's obstacle avoidance system respond to this situation?

8. Compare the effectiveness of different obstacle avoidance strategies (Dynamic Window Approach, Vector Field Histogram, Potential Fields) in a crowded environment with many moving obstacles.

## Practical Application

9. Design a navigation system for an autonomous delivery robot that operates in a university campus with pedestrians, bicycles, and vehicles. What Nav2 components would you configure and how?

10. A warehouse robot needs to transport goods through areas with moving forklifts, workers, and automated guided vehicles (AGVs). How would you configure Nav2 to ensure safe and efficient navigation in this dynamic environment?

## Answers

1. A) Navigation 2
2. C) Weather planning
3. B) To handle exceptional situations and get unstuck

4. Global planners find a geometric route from start to goal based on a known map using algorithms like A* or Dijkstra's. Local planners adjust this path in real-time based on immediate obstacles detected by sensors, accounting for dynamic changes in the environment and ensuring collision-free movement.

5. The perception-action loop consists of: 1) Perception - understanding the current state of the world through sensors, 2) Planning - determining the next course of action based on goals and current state, 3) Execution - carrying out planned motions using robot actuators.

6. Main types of obstacles include: Static obstacles (fixed objects) handled through pre-mapped environment data, Dynamic obstacles (moving objects) detected and avoided in real-time, Temporary obstacles (objects that appear/disappear) detected and responded to dynamically, Predictable obstacles (regular patterns) anticipated and planned around. Nav2 addresses these through costmap updates, local path replanning, and predictive models.

7. Nav2's system would respond by: detecting the cart as an obstacle through sensor data (LiDAR, cameras), updating the costmap to reflect the new obstacle, using the local planner to find a path around the cart, adjusting the robot's trajectory in real-time, and if needed, activating recovery behaviors if the robot becomes stuck or uncertain.

8. In a crowded environment: Dynamic Window Approach balances speed and safety by evaluating feasible trajectories in real-time, Vector Field Histogram creates a polar histogram of obstacle density to find navigable directions, Potential Fields uses attractive forces toward the goal and repulsive forces from obstacles. The Dynamic Window Approach is often most effective as it considers robot dynamics and can quickly adapt to changing conditions.

9. For a campus delivery robot: Configure global planners for efficient route planning across the campus map, set up local planners with conservative parameters for pedestrian safety, implement recovery behaviors for common campus obstacles (benches, event setups), tune costmaps for different surface types (sidewalks, grass, road crossings), and integrate with traffic rules for road crossings and bicycle lanes.

10. For the warehouse environment: Configure Nav2 with high-frequency costmap updates to track moving forklifts and AGVs, set up dynamic obstacle detection with appropriate prediction horizons, implement layered costmaps to distinguish between different types of moving obstacles, configure safety margins based on obstacle speed and size (larger buffers for forklifts), and use behavior trees for complex decision-making when multiple obstacle types are present.