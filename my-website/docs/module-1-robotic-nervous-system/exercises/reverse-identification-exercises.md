---
sidebar_position: 12
title: "Reverse Exercises: Identifying Software Decisions from Physical Actions"
---

# Reverse Exercises: Identifying Software Decisions from Physical Actions

## From Physical Behavior to Software Logic

These exercises help you practice identifying the underlying software decisions that cause observed physical robot behaviors. This reverse engineering approach deepens your understanding of the software-to-action connection.

## Exercise 1: Navigation Behavior Analysis

### Observed Physical Behavior
A mobile robot approaches a doorway and:
1. Slows down significantly as it approaches
2. Performs a slight zigzag motion while passing through
3. Accelerates gradually after clearing the doorway
4. Maintains a 0.5-meter distance from the door frame

### Questions
1. **What software decision parameters** likely caused the robot to slow down?

2. **What algorithmic decision** might explain the zigzag motion?

3. **What safety decision** accounts for the 0.5-meter distance maintenance?

4. **What planning decision** influenced the gradual acceleration after passing through?

### Answer Space
1. Parameter: ____________________

2. Algorithm: ___________________

3. Safety decision: _______________

4. Planning decision: _____________

### Solution Guidance
1. Likely a "MAX_SPEED_NEAR_OBSTACLES" parameter that reduces speed in confined spaces.
2. A "CORRIDOR_NAVIGATION" algorithm that accounts for localization uncertainty in narrow passages.
3. A "SAFETY_MARGIN" decision ensuring clearance from obstacles.
4. A "SMOOTH_TRAJECTORY" planning decision that avoids abrupt accelerations.

## Exercise 2: Manipulation Behavior Analysis

### Observed Physical Behavior
A robotic arm interacts with a glass of water and:
1. Approaches slowly from the side rather than directly from above
2. Opens its gripper wider than the glass diameter before closing
3. Lifts the glass with a perfectly vertical motion
4. Maintains constant grip pressure throughout the lift

### Questions
1. **What object property decision** influenced the side approach?

2. **What grasp planning decision** led to the oversized initial grip opening?

3. **What stability decision** resulted in the perfectly vertical lift?

4. **What force control decision** caused the constant grip pressure?

### Answer Space
1. Property decision: ______________

2. Grasp planning: ________________

3. Stability decision: _____________

4. Force control: _________________

### Solution Guidance
1. A "FRAGILITY_ASSESSMENT" decision recognizing the glass as breakable.
2. A "SAFE_GRASP_INITIATION" decision to prevent crushing before proper positioning.
3. A "SPILL_PREVENTION" decision ensuring liquid doesn't slosh during lift.
4. A "CONSTANT_FORCE_CONTROL" decision to maintain grip without crushing.

## Exercise 3: Emergency Response Analysis

### Observed Physical Behavior
A security robot detects unusual activity and:
1. Immediately stops all motion
2. Rotates its camera 360 degrees
3. Moves toward the source of activity but in a zigzag pattern
4. Maintains constant communication with base station during movement

### Questions
1. **What immediate response decision** caused the robot to stop?

2. **What sensor fusion decision** led to the 360-degree camera rotation?

3. **What tactical decision** resulted in the zigzag movement pattern?

4. **What communication decision** ensured constant base contact?

### Answer Space
1. Response decision: ______________

2. Sensor decision: _______________

3. Tactical decision: ______________

4. Communication decision: _________

### Solution Guidance
1. An "EMERGENCY_STOP" decision triggered by anomaly detection.
2. A "MAXIMIZE_SENSOR_COVERAGE" decision to gather complete situational awareness.
3. A "MINIMIZE_PREDICTABILITY" decision to make interception harder for potential threats.
4. A "CONTINUOUS_STATUS_REPORTING" decision to keep operators informed.

## Exercise 4: Adaptive Cleaning Behavior Analysis

### Observed Physical Behavior
A cleaning robot encounters a dirty spot and:
1. Increases cleaning intensity by making 3 additional passes over the area
2. Slows down its cleaning speed over the dirty area
3. Switches from sweeping to scrubbing mode
4. Extends its time in this zone by approximately 50%

### Questions
1. **What detection algorithm decision** identified the increased dirt concentration?

2. **What adaptive response decision** caused the multiple passes?

3. **What cleaning optimization decision** led to the speed reduction?

4. **What mode selection decision** switched from sweeping to scrubbing?

### Answer Space
1. Detection algorithm: ____________

2. Adaptive response: _____________

3. Optimization decision: __________

4. Mode selection: _______________

### Solution Guidance
1. A "DIRT_DETECTION_THRESHOLD" algorithm that triggers when sensor readings exceed baseline.
2. A "DEEP_CLEAN_PROTOCOL" decision to ensure thorough cleaning of problem areas.
3. A "CONTACT_TIME_OPTIMIZATION" decision to allow more effective cleaning.
4. A "CLEANING_MODE_SELECTION" decision based on the type of contamination detected.

## Exercise 5: Social Interaction Behavior Analysis

### Observed Physical Behavior
A service robot encounters a group of people and:
1. Reduces its speed to 30% of normal
2. Increases its distance from the group to 2 meters
3. Displays a friendly animation on its screen
4. Waits patiently until the group moves aside

### Questions
1. **What social navigation decision** reduced the robot's speed?

2. **What safety protocol decision** increased the distance from people?

3. **What interaction decision** triggered the friendly animation?

4. **What patience algorithm decision** made the robot wait rather than navigate through?

### Answer Space
1. Navigation decision: ____________

2. Safety protocol: _______________

3. Interaction decision: ___________

4. Patience algorithm: ____________

### Solution Guidance
1. A "PEOPLE_AWARE_NAVIGATION" decision that treats people as dynamic obstacles.
2. A "PERSONAL_SPACE_RESPECT" protocol ensuring comfort for nearby humans.
3. A "SOCIAL_SIGNALING" decision to communicate friendly intent.
4. A "POLITE_WAITING" algorithm that respects human movement patterns.

## Exercise 6: Resource Management Analysis

### Observed Physical Behavior
A robot operating in an area with limited charging stations:
1. Begins returning to base station when battery reaches 30%
2. Takes a more direct route than usual
3. Reduces non-essential operations (screen brightness, extra sensors)
4. Maintains minimum required functionality to complete return journey

### Questions
1. **What battery management decision** initiated the return at 30%?

2. **What route optimization decision** chose the direct path?

3. **What power conservation decision** reduced non-essential operations?

4. **What mission criticality decision** determined what functions to maintain?

### Answer Space
1. Battery management: ____________

2. Route optimization: ____________

3. Power conservation: ____________

4. Mission criticality: ____________

### Solution Guidance
1. A "BATTERY_RETURN_THRESHOLD" decision accounting for journey time and safety margin.
2. A "MINIMUM_ENERGY_ROUTE" decision to conserve power during return.
3. A "POWER_SAVING_MODE" decision that disables non-critical systems.
4. A "FUNCTION_PRIORITIZATION" decision ensuring navigation remains functional.

## Exercise 7: Multi-Robot Coordination Analysis

### Observed Physical Behavior
Two robots working in the same area exhibit:
1. One robot pauses when the other approaches a narrow passage
2. They take turns passing through the narrow area
3. The leading robot adjusts its speed to maintain separation distance
4. Communication signals indicate coordination before the passage

### Questions
1. **What collision avoidance decision** made one robot pause?

2. **What resource allocation decision** determined the turn-taking order?

3. **What formation control decision** maintained the separation distance?

4. **What communication protocol decision** enabled the coordination?

### Answer Space
1. Avoidance decision: _____________

2. Allocation decision: ____________

3. Formation decision: ____________

4. Communication protocol: ________

### Solution Guidance
1. A "RIGHT_OF_WAY" collision avoidance decision for narrow spaces.
2. A "FIRST_COME_FIRST_SERVED" allocation decision based on arrival time.
3. A "FORMATION_KEEPING" decision to maintain safe spacing during movement.
4. A "COORDINATION_HANDSHAKE" protocol ensuring both robots agree on the sequence.

## Challenge Questions

### Scenario Analysis
Given the following physical behaviors, identify the likely software decisions:

1. **Robot behavior**: A delivery robot slows down when approaching a location where children are playing.
   **Likely decision**: _________________________________

2. **Robot behavior**: A vacuum robot increases suction power when transitioning from carpet to hardwood.
   **Likely decision**: _________________________________

3. **Robot behavior**: A warehouse robot takes a longer route to avoid an area marked as "wet floor".
   **Likely decision**: _________________________________

4. **Robot behavior**: A security robot increases patrol frequency in an area where it previously detected anomalies.
   **Likely decision**: _________________________________

## Self-Assessment Quiz

### Multiple Choice Questions

1. When a robot maintains a constant distance from obstacles, what type of software decision is most likely responsible?
   a) Speed control decision
   b) Path planning decision
   c) Safety margin decision
   d) Communication decision

2. What software decision typically causes a robot to move more slowly in uncertain environments?
   a) Efficiency optimization
   b) Uncertainty-aware navigation
   c) Random movement generator
   d) Battery saving mode

3. Which decision would cause a robot to switch from one behavior to another?
   a) Mode selection decision
   b) Color recognition decision
   c) Time of day decision
   d) Ambient temperature decision

### True/False Questions

4. T/F: Physical robot behaviors always directly correspond to single software decisions.

5. T/F: Multiple software decisions often work together to produce a single physical behavior.

6. T/F: Understanding physical behaviors can help infer the underlying software architecture.

### Answer Key
1. c) Safety margin decision
2. b) Uncertainty-aware navigation
3. a) Mode selection decision
4. False (Behaviors often result from multiple interacting decisions)
5. True
6. True

## Advanced Challenge

### Reverse Engineering Exercise
Watch a video of a robot performing a task (or imagine one) and identify:
1. 5 distinct physical behaviors
2. The likely software decisions behind each behavior
3. How these decisions might interact with each other
4. What sensors and algorithms would be required to make these decisions

## Reflection Questions

After completing these reverse exercises, consider:

1. How does analyzing physical behavior help understand software decision-making?
2. What challenges arise when multiple decisions affect the same physical behavior?
3. How might the same physical behavior result from different decision-making approaches?
4. What role do sensors play in enabling these software decisions?

## Application to Real Systems

These reverse identification skills apply to:
- Robot debugging and troubleshooting
- Understanding robot behavior in unexpected situations
- Improving robot-human interaction
- Enhancing robot safety and reliability
- Optimizing robot performance