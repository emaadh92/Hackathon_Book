# Data Model: Robotic Nervous System Concepts

## Overview

This data model defines the key concepts and entities for Module 1: The Robotic Nervous System. The model is designed to be educational rather than technical, focusing on conceptual understanding for students and non-technical learners.

## Core Entities

### 1. RobotFunction (Node Concept)

**Description**: Represents a specialized department or organ within the robot that performs specific tasks.

**Attributes**:
- `id`: Unique identifier for the function
- `name`: Human-readable name (e.g., "Vision Department", "Motor Control")
- `responsibility`: Brief description of what this function does
- `inputTypes`: List of information types this function receives
- `outputTypes`: List of information types this function produces
- `analogy`: Real-world comparison to help students understand

**Relationships**:
- `communicatesWith`: Set of other RobotFunctions this one exchanges information with
- `hasSubordinates`: Child functions that report to this one (hierarchical structure)

**Example Instances**:
- VisionProcessor: processes visual data
- MotorController: handles movement commands
- DecisionMaker: coordinates behaviors
- SensorFusion: combines data from multiple sensors

### 2. CommunicationChannel (Topic Concept)

**Description**: Represents pathways through which robot functions share information.

**Attributes**:
- `id`: Unique identifier for the channel
- `name`: Human-readable name (e.g., "Obstacle Alerts", "Movement Commands")
- `type`: Category of information (sensor_data, command, status, feedback)
- `publisher`: The function that sends information through this channel
- `subscribers`: List of functions that receive information from this channel
- `frequency`: How often information is transmitted (for real-time systems)
- `urgency`: Priority level of the information (critical, important, routine)

**Relationships**:
- `connects`: Links to RobotFunction entities that use this channel
- `hasMessages`: Collection of information transmitted through the channel

### 3. RequestService (Service Concept)

**Description**: Represents formal request-response interactions between robot functions.

**Attributes**:
- `id`: Unique identifier for the service
- `name`: Human-readable name (e.g., "Path Calculation Service", "Object Recognition Service")
- `requestType`: Information needed from the client
- `responseType`: Information returned to the client
- `requester`: Function making the request
- `provider`: Function fulfilling the request
- `timeout`: Maximum time to wait for a response

**Relationships**:
- `interactsWith`: Links to RobotFunction entities involved in the service
- `hasRequests`: Collection of past request-response pairs

### 4. LongRunningTask (Action Concept)

**Description**: Represents complex operations that take time and may provide feedback during execution.

**Attributes**:
- `id`: Unique identifier for the task
- `name`: Human-readable name (e.g., "Navigation to Location", "Object Manipulation")
- `goal`: Desired outcome of the task
- `feedbackType`: Information provided during execution
- `resultType`: Final outcome information
- `initiator`: Function that started the task
- `executor`: Function performing the task

**Relationships**:
- `hasFeedback`: Collection of status updates during execution
- `hasResult`: Final outcome when task completes

### 5. RobotComponent (Physical Element)

**Description**: Represents physical parts of the robot that correspond to functions.

**Attributes**:
- `id`: Unique identifier for the component
- `name`: Human-readable name (e.g., "Left Camera", "Right Arm Motor")
- `type`: Category (sensor, actuator, controller)
- `location`: Physical position on the robot
- `connectedFunction`: The RobotFunction that controls this component
- `capabilities`: What this component can do

**Relationships**:
- `controlledBy`: Links to RobotFunction entity
- `hasSpecifications`: Technical details about the component

### 6. CommunicationAnalogy

**Description**: Real-world comparisons that help students understand robotic communication.

**Attributes**:
- `id`: Unique identifier for the analogy
- `targetConcept`: Which robotic concept the analogy explains
- `analogyDomain`: The real-world domain (company, human body, city)
- `detailedExplanation`: Full description of how the analogy works
- `applicabilityRange`: Situations where the analogy is most useful

**Relationships**:
- `explains`: Links to entities it helps explain (RobotFunction, CommunicationChannel, etc.)

## Conceptual Relationships

### Hierarchical Relationships
- RobotFunction may contain child RobotFunctions
- Higher-level functions coordinate lower-level functions

### Communication Relationships
- RobotFunction publishes to CommunicationChannel
- RobotFunction subscribes to CommunicationChannel
- RobotFunction requests from RequestService
- RobotFunction provides RequestService
- RobotFunction initiates LongRunningTask
- RobotFunction executes LongRunningTask

### Physical Relationships
- RobotFunction controls RobotComponent
- RobotComponent provides data to RobotFunction

### Educational Relationships
- All entities can be associated with CommunicationAnalogy
- CommunicationAnalogy enhances understanding of other entities

## Validation Rules

1. **Communication Integrity**: Every CommunicationChannel must have at least one publisher and one subscriber
2. **Function Completeness**: Every RobotFunction must have a responsibility description
3. **Service Response**: Every RequestService must have a defined response type
4. **Component Mapping**: Every RobotComponent must be controlled by exactly one RobotFunction
5. **Analogy Relevance**: Every CommunicationAnalogy must link to a real robotic concept

## State Transitions (where applicable)

### RobotFunction States
- Idle: Waiting for input
- Active: Processing information
- Communicating: Exchanging information
- Busy: Handling complex tasks

### CommunicationChannel States
- Available: Ready to transmit
- Active: Currently transmitting
- Congested: High traffic
- Failed: Communication breakdown

### RequestService States
- Available: Ready to accept requests
- Processing: Working on a request
- Busy: Cannot accept new requests
- Unavailable: Temporarily offline

## Sample Data Models for Exercises

### Basic Robot Configuration
```
RobotFunction: "Navigation Department"
- Responsibility: "Plans paths and avoids obstacles"
- InputTypes: ["sensor_data", "destination_request"]
- OutputTypes: ["movement_commands", "status_updates"]
- Analogy: "Like GPS and driver working together"

CommunicationChannel: "Sensor Fusion Feed"
- Type: "sensor_data"
- Publisher: "SensorFusion"
- Subscribers: ["Navigation Department", "Safety Monitor"]
- Urgency: "critical"
```

### Complex Interaction Example
```
LongRunningTask: "Move to Charging Station"
- Goal: "Navigate robot to charging dock"
- Initiator: "Power Management Function"
- Executor: "Navigation Department"
- Feedback: "progress_updates, battery_status"

CommunicationChannel: "Charging Status"
- Publisher: "Power Management Function"
- Subscribers: ["System Monitor", "User Interface"]
```

## Extensions for Advanced Learning

### Performance Metrics
- Communication latency between functions
- Message throughput on channels
- Service response times
- Task completion rates

### Failure Scenarios
- Function failure recovery
- Communication disruption handling
- Degraded mode operation
- Emergency procedures

### Optimization Concepts
- Bandwidth management
- Prioritization strategies
- Redundancy planning
- Load balancing