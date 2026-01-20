# Data Model: Digital Twin Simulation Concepts

## Overview
This document defines the key entities and relationships for the digital twin simulation concepts taught in Module 2. Since this is an educational module, the data model represents conceptual entities rather than implementation structures.

## Core Entities

### Digital Twin
- **Definition**: A virtual representation of a robot and its environment
- **Purpose**: Safe testing, observation, and improvement of robot behavior
- **Characteristics**:
  - Mirrors physical properties of real robot
  - Exists in simulated environment
  - Uses simulated sensors to perceive virtual world

### Simulated Environment
- **Definition**: A virtual space that replicates real-world physics and conditions
- **Components**:
  - Physical laws (gravity, friction, momentum)
  - Spatial elements (rooms, floors, obstacles)
  - Interactive objects
  - Environmental conditions (lighting, weather effects)

### Physics Simulation
- **Definition**: Mathematical models that represent real-world physical laws
- **Core Elements**:
  - Gravity: Downward force affecting all objects
  - Movement: Translation and rotation mechanics
  - Collisions: Interaction between objects
  - Friction: Resistance to motion

### Simulated Sensors
- **Definition**: Virtual equivalents of real robot sensors
- **Types**:
  - LiDAR: Distance sensing and spatial mapping
  - Depth Camera: 3D perception and obstacle detection
  - IMU: Balance and motion awareness
- **Function**: Enable robot to perceive and navigate virtual environment

### Human Presence Model
- **Definition**: Representation of human actors in simulation
- **Purpose**: Enable safe testing of human-robot interaction
- **Attributes**: Position, movement patterns, interaction behaviors

## Relationships

### Digital Twin → Simulated Environment
- A digital twin exists within and interacts with a simulated environment
- The environment provides the context for the twin's operation

### Simulated Environment → Physics Simulation
- The environment implements physics simulation rules
- Physics govern how objects behave within the environment

### Digital Twin → Simulated Sensors
- A digital twin utilizes simulated sensors to perceive its environment
- Sensors provide input data for the twin's decision-making

### Simulated Environment → Human Presence Model
- The environment may contain human presence models
- Enables interaction testing between digital twin and virtual humans

## Conceptual States

### Digital Twin States
- **Operational**: Actively simulating robot behavior
- **Learning**: Adapting behavior based on simulation experiences
- **Evaluation**: Being assessed for safety/performance

### Simulation States
- **Paused**: Simulation temporarily stopped
- **Running**: Active simulation with physics calculations
- **Recording**: Capturing simulation data for analysis
- **Playback**: Replaying recorded simulation data

## Educational Attributes

### Conceptual Properties (for learning)
- **Complexity Level**: Beginner, Intermediate, Advanced
- **Visual Representation**: Diagram, Animation, Interactive Demo
- **Real-World Analogy**: Flight simulator, Video game physics, etc.
- **Learning Objective**: Specific concept being taught

## Validation Rules

### Educational Content Requirements
- All concepts must be explained without requiring deep technical knowledge
- Visual examples must accompany each abstract concept
- Real-world analogies must be provided for complex topics
- Content must be suitable for diverse technical backgrounds

### Conceptual Integrity
- Digital twin concepts must align with industry understanding
- Physics simulation explanations must be conceptually accurate
- Sensor descriptions must relate to real-world equivalents
- Human-robot interaction concepts must emphasize safety

## State Transitions

### Learning Progression
- **Introduction** → **Basic Understanding** → **Advanced Concepts** → **Application**
- Students progress through conceptual layers as understanding develops
- Each stage builds upon previous conceptual foundations