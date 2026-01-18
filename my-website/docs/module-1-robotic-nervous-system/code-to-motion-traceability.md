---
sidebar_position: 16
title: "Traceability: From Code to Motion Examples"
---

# Traceability: From Code to Motion Examples

## Connecting Software to Physical Action

This section provides detailed traceability examples that show how specific lines of code translate into physical robot motion. Understanding these connections is essential for comprehending the complete software-to-motion pathway.

## Example 1: Basic Movement Command

### Code Snippet
```python
def move_forward(distance):
    """Move robot forward by specified distance"""
    # Calculate required wheel rotations
    rotations = distance / WHEEL_CIRCUMFERENCE

    # Set wheel velocities for forward motion
    left_wheel_vel = FORWARD_SPEED
    right_wheel_vel = FORWARD_SPEED

    # Execute motion command
    robot.left_wheel.set_velocity(left_wheel_vel)
    robot.right_wheel.set_velocity(right_wheel_vel)

    # Wait for motion completion
    time.sleep(distance / FORWARD_SPEED)

    # Stop wheels
    robot.left_wheel.set_velocity(0)
    robot.right_wheel.set_velocity(0)
```

### Code-to-Motion Traceability

#### Line-by-Line Analysis:
1. `move_forward(distance)` - Function definition with distance parameter
2. `rotations = distance / WHEEL_CIRCUMFERENCE` - Calculates physical wheel rotations needed
3. `left_wheel_vel = FORWARD_SPEED` - Sets left wheel to forward speed
4. `right_wheel_vel = FORWARD_SPEED` - Sets right wheel to same forward speed
5. `robot.left_wheel.set_velocity(left_wheel_vel)` - Sends command to left wheel controller
6. `robot.right_wheel.set_velocity(right_wheel_vel)` - Sends command to right wheel controller
7. `time.sleep(...)` - Pauses program to allow motion to complete
8. Wheel velocity resets to 0 - Stops the wheels

#### Physical Result:
- Robot moves forward in straight line
- Distance traveled equals input parameter
- Smooth start and stop motion

### Real-World Scenario
**Code Call:** `move_forward(2.0)` (move 2 meters forward)
**Physical Outcome:** Robot's wheels rotate to move the robot exactly 2 meters forward at a steady pace.

## Example 2: Turn Command

### Code Snippet
```python
def turn_right(angle_degrees):
    """Turn robot right by specified angle"""
    # Convert angle to radians
    angle_rad = math.radians(angle_degrees)

    # Calculate arc distance for turning
    arc_distance = angle_rad * ROBOT_WIDTH / 2

    # Set differential wheel speeds for turning
    left_wheel_vel = FORWARD_SPEED
    right_wheel_vel = -FORWARD_SPEED  # Negative for opposite direction

    # Execute turn
    robot.left_wheel.set_velocity(left_wheel_vel)
    robot.right_wheel.set_velocity(right_wheel_vel)

    # Calculate turn duration
    turn_duration = arc_distance / FORWARD_SPEED
    time.sleep(turn_duration)

    # Stop wheels
    robot.left_wheel.set_velocity(0)
    robot.right_wheel.set_velocity(0)
```

### Code-to-Motion Traceability

#### Key Transformations:
1. `math.radians(angle_degrees)` - Converts human-readable degrees to mathematical radians
2. `arc_distance = angle_rad * ROBOT_WIDTH / 2` - Calculates physical distance wheels must travel
3. `right_wheel_vel = -FORWARD_SPEED` - Creates differential motion for turning
4. Differential velocities cause robot to pivot in place

#### Physical Result:
- Robot pivots clockwise in place
- Rotation equals input angle
- Left wheel moves forward, right wheel moves backward

### Real-World Scenario
**Code Call:** `turn_right(90.0)` (turn 90 degrees right)
**Physical Outcome:** Robot rotates 90 degrees clockwise, ending facing perpendicular to original direction.

## Example 3: Sensor-Based Conditional Motion

### Code Snippet
```python
def navigate_with_obstacle_avoidance():
    """Navigate forward while avoiding obstacles"""
    # Read distance sensor
    distance_to_obstacle = robot.front_sensor.read()

    # Check if obstacle is too close
    if distance_to_obstacle < SAFE_DISTANCE:
        # Obstacle detected - turn to avoid
        turn_right(45)  # Turn 45 degrees
        move_forward(1.0)  # Move forward 1 meter
        turn_left(45)  # Turn back to original direction
    else:
        # No obstacle - continue forward
        move_forward(0.5)  # Move forward 0.5 meters
```

### Code-to-Motion Traceability

#### Decision Points:
1. `distance_to_obstacle = robot.front_sensor.read()` - Reads physical sensor data
2. `if distance_to_obstacle < SAFE_DISTANCE:` - Compares sensor reading to threshold
3. Conditional execution based on sensor input
4. Different motion sequences for obstacle vs. clear path

#### Physical Result:
- Robot moves forward until obstacle detected
- When obstacle detected: turn, move around, return to original direction
- When clear: continue forward

### Real-World Scenario
**Code Call:** `navigate_with_obstacle_avoidance()`
**Physical Outcome:** Robot moves forward, detects obstacle 0.3m away (less than SAFE_DISTANCE of 0.5m), executes avoidance maneuver around obstacle.

## Example 4: Complex Navigation Path

### Code Snippet
```python
def execute_delivery_route():
    """Execute predefined delivery route"""
    # Define waypoints
    waypoints = [
        (0.0, 0.0),    # Start
        (2.0, 0.0),    # Move 2m forward
        (2.0, 1.5),    # Move 1.5m right
        (0.0, 1.5),    # Move 2m back
        (0.0, 0.0)     # Return to start
    ]

    # Navigate to each waypoint
    for i in range(1, len(waypoints)):
        start_pos = waypoints[i-1]
        end_pos = waypoints[i]

        # Calculate direction vector
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        # Calculate distance and angle
        distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)

        # Face the correct direction
        target_angle = math.degrees(angle)
        current_heading = robot.get_heading()
        turn_angle = target_angle - current_heading
        turn_right(turn_angle)

        # Move to destination
        move_forward(distance)
```

### Code-to-Motion Traceability

#### Sequential Operations:
1. Waypoint array defines path geometry
2. Loop iterates through path segments
3. Vector calculations determine navigation parameters
4. Heading adjustments ensure proper orientation
5. Distance-based movements execute path segments

#### Physical Result:
- Robot follows rectangular path
- Precise positioning at each waypoint
- Smooth transitions between path segments

### Real-World Scenario
**Code Call:** `execute_delivery_route()`
**Physical Outcome:** Robot traces a 2m x 1.5m rectangle, returning to starting position with high positional accuracy.

## Example 5: Manipulation Control

### Code Snippet
```python
def pick_up_object():
    """Pick up object with robotic arm"""
    # Move arm to object location
    arm.move_to_position(OBJECT_X, OBJECT_Y, ARM_HEIGHT)

    # Lower gripper to object
    arm.lower_gripper(GRIPPER_APPROACH_HEIGHT)

    # Close gripper
    gripper.close_with_force(PREDEFINED_GRIP_FORCE)

    # Wait for grip confirmation
    time.sleep(0.5)

    # Lift object
    arm.raise_gripper(LIFT_HEIGHT)

    # Confirm successful grasp
    if gripper.has_object():
        return True
    else:
        return False
```

### Code-to-Motion Traceability

#### Manipulation Sequence:
1. `arm.move_to_position(...)` - Positions arm near object
2. `arm.lower_gripper(...)` - Moves gripper to object level
3. `gripper.close_with_force(...)` - Applies controlled gripping force
4. `arm.raise_gripper(...)` - Lifts object from surface
5. `gripper.has_object()` - Confirms successful grasp

#### Physical Result:
- Arm moves to precise location
- Gripper approaches and grasps object
- Object is lifted and secured

### Real-World Scenario
**Code Call:** `pick_up_object()`
**Physical Outcome:** Robot arm precisely moves to object location, grasps it with appropriate force, and lifts it securely.

## Example 6: Feedback-Controlled Motion

### Code Snippet
```python
def precise_position_control(target_x, target_y):
    """Move to precise location using feedback control"""
    current_x, current_y = robot.get_position()

    # Calculate error
    error_x = target_x - current_x
    error_y = target_y - current_y
    distance_error = math.sqrt(error_x*error_x + error_y*error_y)

    # Continue until within acceptable tolerance
    while distance_error > POSITION_TOLERANCE:
        # Calculate required heading
        required_heading = math.atan2(error_y, error_x)
        current_heading = robot.get_heading()

        # Calculate heading error
        heading_error = required_heading - current_heading

        # Apply proportional control
        linear_vel = min(MAX_LINEAR_VEL, distance_error * LINEAR_GAIN)
        angular_vel = min(MAX_ANGULAR_VEL, heading_error * ANGULAR_GAIN)

        # Set wheel velocities
        robot.set_velocity(linear_vel, angular_vel)

        # Update position
        current_x, current_y = robot.get_position()
        error_x = target_x - current_x
        error_y = target_y - current_y
        distance_error = math.sqrt(error_x*error_x + error_y*error_y)

    # Stop robot
    robot.stop()
```

### Code-to-Motion Traceability

#### Control Loop Operations:
1. Position feedback acquisition
2. Error calculation between current and target
3. Proportional control algorithm
4. Velocity command generation
5. Continuous loop until tolerance achieved

#### Physical Result:
- Smooth approach to target position
- Automatic correction for deviations
- Precise positioning within tolerance

### Real-World Scenario
**Code Call:** `precise_position_control(3.0, 2.0)` (move to coordinates 3.0, 2.0)
**Physical Outcome:** Robot smoothly navigates to exact coordinates with high precision, automatically correcting for any deviations during motion.

## Key Traceability Insights

### 1. Abstraction Levels
Each example demonstrates how high-level commands translate through multiple layers:
- **Application Layer:** High-level goals (navigate, manipulate)
- **Control Layer:** Motion planning and execution
- **Hardware Layer:** Direct component control
- **Physical Layer:** Actual robot movement

### 2. Feedback Integration
Most examples include feedback mechanisms that close the control loop, ensuring accurate motion execution.

### 3. Safety Considerations
Code includes safety checks and limitations that prevent harmful physical actions.

### 4. Timing Dependencies
Physical motion requires careful timing coordination between software commands and hardware response.

## Learning Objectives

After studying these traceability examples, you should be able to:

1. **Trace** how specific code statements result in physical motion
2. **Identify** the different layers involved in code-to-motion transformation
3. **Recognize** feedback mechanisms that ensure accurate motion execution
4. **Understand** the relationship between software parameters and physical outcomes
5. **Appreciate** the complexity of converting abstract code into precise physical actions

## Check Your Understanding

1. In Example 1, which code line directly commands the physical wheels to move?

2. How does Example 3 use sensor feedback to influence physical motion?

3. What safety mechanism prevents Example 6 from exceeding safe velocity limits?

4. Which example demonstrates the most complex code-to-motion transformation?

## Advanced Connections

These traceability examples connect to:
- Control systems engineering principles
- Real-time programming concepts
- Feedback control theory
- Robotics kinematics and dynamics
- Safety-critical system design