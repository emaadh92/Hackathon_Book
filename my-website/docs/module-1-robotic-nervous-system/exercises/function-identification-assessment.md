---
sidebar_position: 10
title: "Assessment: Robot Function Identification"
---

# Assessment: Robot Function Identification

## Evaluating Your Understanding

This assessment evaluates your ability to identify and differentiate between robot functions in various scenarios. Achieve 80% accuracy (4 out of 5 questions) to demonstrate proficiency in function identification.

## Question 1: Function Classification (Multiple Choice)

Which of the following best describes the primary responsibility of a robot's "Vision Department"?

A) Controlling physical movements and actuation
B) Processing visual information to understand the environment
C) Coordinating behaviors and making high-level decisions
D) Monitoring for safety hazards and ensuring safe operation

**Answer Space:** ________________

## Question 2: Scenario Analysis (Short Answer)

A warehouse robot has the following components: cameras, LIDAR, wheel motors, lifting mechanism, communication module, and decision-processing computer.

List the 5 primary functions you would identify in this robot and briefly describe each function's responsibility:

1. Function 1: _________________________
   Responsibility: _____________________

2. Function 2: _________________________
   Responsibility: _____________________

3. Function 3: _________________________
   Responsibility: _____________________

4. Function 4: _________________________
   Responsibility: _____________________

5. Function 5: _________________________
   Responsibility: _____________________

## Question 3: Communication Pattern Matching (Matching)

Match each robot function with the most appropriate communication pattern for the given scenario:

**Functions:**
- A. Vision Department
- B. Motor Control Department
- C. Decision-Making Department
- D. Safety Monitor Department

**Scenarios:**
1. Requesting a specific path calculation from a navigation service
2. Broadcasting location updates to multiple other functions
3. Initiating a long-term navigation task with progress updates
4. Continuously monitoring and sharing obstacle detection data

**Answers:**
- 1. _____
- 2. _____
- 3. _____
- 4. _____

## Question 4: Problem-Solving Application (Analysis)

A hospital delivery robot is navigating a corridor when it encounters a medical emergency. The robot must decide whether to continue its delivery task or yield to the emergency situation.

**Part A:** Which robot function would make the priority decision? Explain your reasoning.

**Part B:** How would this function communicate with other functions to coordinate the response?

**Part C:** What type of communication pattern would be most appropriate for this situation?

## Question 5: Integration Challenge (Comprehensive)

Design a robot function configuration for an underwater exploration robot with these capabilities:
- Underwater cameras and sonar
- Propulsion system for navigation
- Sample collection mechanism
- Buoyancy control system
- Communication to surface vessel
- Environmental monitoring sensors

**Requirements:**
1. Identify 4 primary robot functions
2. Describe each function's responsibilities
3. Explain how these functions would communicate and coordinate
4. Identify which function would handle emergency surfacing decisions

**Function 1:** ________________
**Responsibilities:** ___________
**Communication Role:** __________

**Function 2:** ________________
**Responsibilities:** ___________
**Communication Role:** __________

**Function 3:** ________________
**Responsibilities:** ___________
**Communication Role:** __________

**Function 4:** ________________
**Responsibilities:** ___________
**Communication Role:** __________

**Emergency Coordination:** ________

## Answer Key

### Question 1:
**Correct Answer:** B) Processing visual information to understand the environment

### Question 2:
**Expected Answers Include:**
1. Vision Department: Process camera and LIDAR data to identify objects and obstacles
2. Motor Control Department: Control wheel motors for navigation and movement
3. Manipulation Department: Operate lifting mechanism for package handling
4. Communication Department: Handle communication with warehouse systems
5. Decision-Making Department: Coordinate activities and make operational decisions

### Question 3:
**Correct Matches:**
1. C (Decision-Making) - Service request for path calculation
2. A (Vision) or B (Motor Control) - Topic for location broadcasts
3. C (Decision-Making) - Action for long-term navigation
4. A (Vision) - Topic for continuous obstacle data

### Question 4:
**Part A:** Decision-Making Department - Responsible for prioritizing tasks and handling exceptional situations
**Part B:** Would communicate via topics to inform other functions of the change in priorities, and via services to request adjustments to current operations
**Part C:** Combination of topics (broadcasting status changes) and services (requesting specific actions)

### Question 5:
**Expected Functions:**
1. Vision/Navigational Department: Process camera and sonar data for navigation
2. Propulsion Department: Control underwater movement and navigation
3. Sampling Department: Operate sample collection and buoyancy control
4. Communication Department: Handle surface communication and environmental monitoring
5. Emergency/Decision Department: Coordinate emergency responses including surfacing decisions

## Scoring Rubric

### Question 1 (1 point): Multiple Choice
- 1 point for correct answer
- 0 points for incorrect answer

### Question 2 (5 points): Function Identification
- 1 point for each correctly identified function and responsibility
- Partial credit (0.5) for partially correct answers

### Question 3 (4 points): Matching
- 1 point for each correct match
- 0 points for incorrect matches

### Question 4 (3 points): Analysis
- 1 point for identifying Decision-Making Department
- 1 point for explaining communication approach
- 1 point for identifying appropriate communication pattern

### Question 5 (7 points): Integration Challenge
- 1 point for each function identification (4 points total)
- 1 point for responsibilities description
- 1 point for communication explanation
- 1 point for emergency coordination

### Total Possible Score: 20 points
- **Passing Score (80%): 16 points or higher**
- **Proficient: 18-20 points**
- **Developing: 14-15 points**
- **Needs Improvement: Below 14 points**

## Reflection Questions

After completing this assessment:

1. Which question type was most challenging for you and why?
2. How did you approach the integration challenge differently than the simpler identification tasks?
3. What strategies helped you differentiate between similar robot functions?
4. How might you apply these function identification skills to analyze real robotic systems?

## Remediation Resources

If you scored below 80%, review:
- Module 1, Lesson 3: Node, Topic, and Service Analogies
- Module 1, Lesson 4: Connecting Software Logic to Physical Actions
- The RobotFunction entity documentation
- Practical examples of robot functions