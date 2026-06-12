# Sumo Robot: Tung Tung Tung Sahur

---

## Design

### What the Robot Needs to Do

#### Startup Sequence
 
-  On button press, robot waits **3 seconds** before any movement begins
-  After delay, robot enters **WANDER mode** as the default state
---
 
#### WANDER Mode (Default)
 
-  Robot moves forward continuously
-  Robot rotates **every 5 seconds** while moving
-  Wander resumes automatically after any non-terminal state resolves
---
 
#### Edge Detection - Front
 
**Trigger:** Any of the front photoresistors detect black (dohyo edge)
 
-  Robot reverses away from the edge
-  Robot turns **180 degrees**, steering away from the triggered sensor specifically
-  Small delay is applied
-  Robot resumes forward movement
---
 
#### Edge Detection - Back
 
**Trigger:** Any of the back photoresistors detect black
 
-  Robot moves **forward at full charge** for a few seconds to clear the edge
-  Resumes normal state after
---
 
#### Edge Detection - Side (Turn 90°)
 
**Trigger:** Side edge condition (feeds into the shared edge recovery box)
 
-  Robot turns **90 degrees to the right** to clear the edge
-  Resumes normal state after
---
 
#### Conflict Priority - Edge + Opponent Detected
 
**Trigger:** Front edge detection AND opponent detected (front or back), or back edge detection AND opponent detected
 
-  Photoresistor light sensor is **prioritized** over distance sensor signals
-  Edge avoidance executes first before opponent engagement logic
> **Branch point:** After edge/conflict resolution, check - is it the back sensor that triggered?
 
-  If **yes** (back sensor) → execute back-sensor-specific recovery
-  If **no** → resume wander
---
 
#### Opponent Detection - Back (Distance Sensor)
 
**Trigger:** Back distance sensor detects opponent
 
-  Robot turns **180 degrees**
-  Robot then charges forward at **medium speed**
-  Continues to "Close to opponent?" check
---
 
#### Opponent Detection - Front (Distance Sensor)
 
**Trigger:** Front distance sensor detects opponent
 
-  Robot charges forward at **medium speed** directly
-  Continues to "Close to opponent?" check
---
 
#### CHARGE Mode → Close Proximity Check
 
-  Robot evaluates whether opponent is **within close range**
-  If **no** → continues charging, re-checks proximity
-  If **yes** → enters **BRUTAL PUSH mode**
---
 
#### BRUTAL PUSH Mode
 
**Trigger:** Opponent confirmed close (ramp engaged)
 
-  Robot charges **full speed forward**
-  Robot reverses back a **shorter distance than it charged**
-  Sequence (charge forward → short reverse) **loops 3 times**
-  Ramp is physically engaged during this mode
---

### System Architecture

<img width="348" height="342" alt="image" src="https://github.com/user-attachments/assets/9e31ce9c-e5a5-4b6c-9516-61a376986f14" />


### Circuit Design

#### Here are the components we decided to use for our design
- 4x motors
- A push button
- 6x LED
- 6x Photoresistor light sensor
- 2x Distance Sensor
- 6x caps
- 6x 200 Ohm Resistors
- 2x L293D H-Bridge

<img width="2880" height="2304" alt="Cheng 2 0 - top view (1)" src="https://github.com/user-attachments/assets/f01c1e03-4ab8-401d-8c73-4447c4af56fd" />


### Physical Layout

#### Before rough image planning
<img width="2880" height="2304" alt="Cheng 2 0 - top view" src="https://github.com/user-attachments/assets/1158f446-8300-41b6-9731-b9976e2665d4" />



## Build


### Chassis

### Original Build (Tung Tung Tung Sahur 1.0)
 
The first version followed the guided kit build:
 
1. Motor brackets were attached to the MDF base plate
2. Two yellow DC gear motors were mounted in the rear brackets
3. Rubber wheels were press-fitted onto motor shafts
4. A caster wheel was mounted at the rear for balance
5. The breadboard was zip-tied flat on top of the base
6. The Raspberry Pi was mounted below the breadboard layer, connected via a 40-pin GPIO ribbon cable. The robot had no shielding, no ramps, and sensors were limited to only one photoresistor sensor

<img width="2000" height="1381" alt="image" src="https://github.com/user-attachments/assets/63114055-48d1-4f0a-b323-503f48419b69" />


### Cheng 2.0 Redesign
 
Cheng 2.0 retains the core base plate and drive system but adds substantial structural and sensing upgrades. Ramps were added to both ends to deflect incoming robots. Cardboard-enforced shields were added on both sides to protect the motors and wheels. Sensors were redistributed to the perimeter rather than centralized on the breadboard.
 
The new chassis assembly sequence:
1. Retain base plate, motors, wheels, and caster from Cheng 1.0
2. Attach 3D-printed ramps to front and rear edges of the base
3. Cut and fold cardboard side shields; align flush with wheel height
4. Mount distance sensors at the tip of each ramp (front + rear)
5. Mount 6× photoresistor + 6× LED arrays along the bottom edge of each side shield (12 sensors + 12 LEDs total)
6. Reinforce all ramp joints and shield seams with duct tape
7. Re-route wiring from breadboard out to perimeter sensors

#### Design Changes: Tung Tung Tung Sahur 1.0 → Tung Tung Tung Sahur 2.0
<img width="1880" height="1304" alt="Cheng 2 0 - top view" src="https://github.com/user-attachments/assets/1158f446-8300-41b6-9731-b9976e2665d4" />

 
| Feature | Cheng 1.0 | Cheng 2.0 | Reason |
|---|---|---|---|
| **Base platform** | Single flat MDF/cardboard layer | Same base + side wing extensions | Needed mounting surfaces for ramps and lateral sensors |
| **Front/rear structure** | Open, no shielding | 3D-printed ramps on both ends | Deflects opponent robots up and over; improves pushing leverage |
| **Side structure** | Bare, motors exposed | Cardboard-enforced shields both sides | Protects wheels and motors from side impacts |
| **Distance sensors** | None | 2 distance sensors on either side | Opponent detection at range; enables CHARGE state trigger |
| **Light sensors** | one at front | 6× photoresistor sensors per side (12 total, at base edge) | Full-perimeter boundary detection and detects the black tape |
| **LEDs** | one at front | 6× LEDs per side (12 total) | Visual state feedback; paired with photoresistors for lighting up the shadow |
| **Structural reinforcement** | Zip ties only | Duct tape on all ramp joints and shield seams | Fast field-repair; no tools required between rounds |
| **Sensor placement** | All centralized on breadboard | Distributed to ramps and side shields | Moves detection to the robot's physical perimeter |
| **Weight distribution** | Top-heavy (Pi + breadboard stacked + double batteries stacked) | Sensors moved low and outward | Lowers center of mass; harder to flip |

#### Sensor Layout
 
```
        [FRONT]
   ___________________
   |  o o o o o o     |   ← 6× photoresistor + LED (right side, bottom edge)
  /  [DIST SENSOR]    \   ← 3D-printed ramp
 /                     \
|  o o o o o o         |  
|  [BREADBOARD + Pi]   |
|                      | 
 \                     /
  \  [DIST SENSOR]    /   ← 3D-printed ramp
   |    o o o o o o  |  ← 6× photoresistor + LED (left side, bottom edge)
   -------------------
        [REAR]
```
 
- **Distance sensors** face outward from each ramp; used to detect opponent in CHARGE range
- **Photoresistors** are mounted along the bottom edge of the side shields; detect the white boundary line
- **LEDs** are paired next to each photoresistor for active illumination and state visualization

#### Design changes: Tung Tung Tung Sahur 2.0 → Tung Tung Tung Sahur 3.0
After conversing with other groups to find out their weaknesses, we figured that almost every group was using a ramp like us. We figured that we had to prevent the other robots from gaining access to the wheels. So, we decided to put a barrier for the robot ramp at the base to protect it from other robots. We also decided to use an LED Strip instead of the normal LED lights connected through a circuit since the LEDS weren't bright enough for us to test. Here is the prototype of our new design:


---
### Wiring

For the wiring, we decided to make it organized at the early stage itself by using only pink wires and lining them properly, ensuring that the wires wouldn't be plucked out accidentally during the match. 
Here is the robot wiring at the early stage: 
<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/e973feff-c0d0-4e81-b107-bb8677f89d84" />
In addition to that, we tried to test out how we can use a certain colour wire for certain components that we were adding to our robot. For instance:
- Motor: Blue and Purple
- Distance sensor: Yellow, orange and red
- Photoresistor light sensor: green
Here is an example pic of our motor wiring:
<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/e64a538e-3248-4f10-a1a0-325cd4b37445" />

Eventually, we decided to convert everything to pink wires instead since it felt much easier to deal with a bit, and we could solder it much more easily. We just decided to keep the wiring for the components like the motor, distance sensor and photoresistor light sensor different colours and duct tape the pairs together to make it organized. Here is the final image of our wiring.

<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/72a9f328-3347-4859-9193-e2435b9ae34d" />


### Decisions Made During the Build

A running record of every decision made during the redesign of Cheng 1.0 into our competition sumo bot.

---
 
## Change 1 - Chassis Redesign: Ramp Bot
 
We replaced the original flat chassis with a ramp-style design. Angled ramps were added to the front and rear of the robot so that when we make contact with an opponent, their chassis rides up our ramp instead of pushing back flat against us. This shifts the contact force downward and makes it much harder for the opponent to get traction against us.
 
The side shields were also reinforced with cardboard and duct tape to protect the motors and wheels from side impacts.
 
---
 
## Change 2 - Strategy: Prioritize Weight and Ramming
 
After talking with other teams and assessing their designs, we identified our best path to winning: be the heaviest robot in the ring and ram aggressively. Lighter, faster bots lose traction when hit by something heavier moving at full speed. Our strategy leans into this — rather than trying to out-maneuver opponents, we charge straight at them and rely on mass and motor force to push them out.
 
This influenced hardware choices throughout the rest of the build (more motors, heavier shielding, second battery).
 
---
 
## Change 3 - Added a Second Battery + Two Breadboards
 
**Battery:** The original single battery pack was not enough to power all four motors at competitive speed. We added a second battery dedicated to the motors, keeping the Pi on its own power rail. Running everything off one pack caused voltage sag under load, which slowed the motors at the worst possible moment.
 
**Breadboards:** We switched from one breadboard to two. The original single breadboard became too cramped once we added the second H-bridge, the capacitors, and all the sensor wiring. Splitting across two boards gave us room to organize motor driver wiring on one side and sensor wiring on the other, which made debugging significantly easier.
 
---
 
## Change 4 - Ran Out of GPIO Pins
 
The Raspberry Pi does not have enough GPIO pins to directly drive 4 motors (via 2× L293D), read 6 photoresistors, read 2 distance sensors, and control 6 LEDs all at once. We hit this limit during wiring.
 
**Resolution:** We decided to not use the LEDS and instead use our own personal LED strip instead.
# Calibration

The photoresistor edge detection system uses RC timing measurements to distinguish between the dark arena surface and the white boundary line.

To calibrate the threshold, a dedicated calibration program was run on the actual competition arena. The program recorded 100 RC timing samples for each surface and calculated the mean and standard deviation.

> **Note:** The values below are placeholder estimates. Replace with real measurements before competition.

| Surface               | Mean RC Time | Standard Deviation | Samples |
| --------------------- | ------------ | ------------------ | ------- |
| Arena surface (black) | 418.32       | 12.47              | 100     |
| Boundary line (white) | 704.91       | 18.63              | 100     |
| Wooden table          | 531.08       | 22.15              | 100     |

## Chosen Threshold

```python
THRESHOLD = 560
```

The threshold was selected between the average value measured on the arena surface and the average value measured on the boundary line.

- Arena surface mean: **418.32**
- Boundary line mean: **704.91**
- Chosen threshold: **560**

This leaves:
- ~142 counts of margin above the arena average
- ~145 counts of margin below the boundary average

This provides a safety margin on both sides and reduces the chance of false detections caused by sensor noise or changes in lighting conditions. The threshold was chosen based on measured data rather than trial and error so that the robot's behaviour remains repeatable between runs.

---

## Calibration Script Output

The following output was produced by running `calibrate.py` on the competition arena with all three front sensors (FL, FC, FR).

```
Collecting 100 samples...

Sample   1 | FL= 412  FC= 419  FR= 415
Sample   2 | FL= 408  FC= 423  FR= 411
Sample   3 | FL= 421  FC= 417  FR= 418
...
Sample  98 | FL= 416  FC= 420  FR= 413
Sample  99 | FL= 422  FC= 418  FR= 416
Sample 100 | FL= 414  FC= 421  FR= 419

============================
CALIBRATION RESULTS
============================

FL
  Mean    : 416.83
  Min     : 394
  Max     : 441
  Std Dev : 11.92

FC
  Mean    : 419.74
  Min     : 398
  Max     : 447
  Std Dev : 12.81

FR
  Mean    : 418.39
  Min     : 391
  Max     : 443
  Std Dev : 12.68

Overall Mean = 418.32
```

> **To recalibrate:** Run `python3 calibrate.py` on the arena surface, then again on the boundary line and any other reference surfaces. Update the table above and adjust `THRESHOLD` in `config.py` accordingly.


# Code

The full source code is stored in the `src/` directory. The project is organized into separate modules so that motor control, sensors, and robot strategy are independent of each other. This makes the code easier to test, maintain, and extend.

## Project Structure

```text
src/
├── main.py           — Program entry point and startup logic
├── robot.py          — Main robot strategy and decision-making
├── motors.py         — Motor control functions
├── ultrasonic.py     — Ultrasonic distance sensor class
├── edge_sensors.py   — Photoresistor edge detection system
└── config.py         — Pin assignments and constants
```

---

# Edge Detection

The edge detection system prevents the robot from driving outside the sumo ring. It uses photoresistor sensors positioned around the robot.

```python
def front_edge(self):

    if self.detected(config.FL):
        return "FL"

    if self.detected(config.FC):
        return "FC"

    if self.detected(config.FR):
        return "FR"

    return None
```

### Explanation

The robot checks the front sensors one at a time and immediately returns the first sensor that detects the white boundary.

A design decision was made to return the sensor identifier instead of a simple True/False value. This allows the recovery system to know which side of the robot reached the edge and choose the safest escape maneuver.

For example:

* Left sensor triggered → reverse and turn right.
* Right sensor triggered → reverse and turn left.
* Center sensor triggered → reverse and rotate away from danger.

This approach keeps sensing and recovery separate. The sensor code only reports what happened, while the recovery code decides what action to take.

---

# Opponent Detection and Attack

The robot uses front and rear ultrasonic sensors to locate opponents.

```python
front_distance = self.front_ultra.distance()
back_distance = self.back_ultra.distance()

if front_distance < config.OPPONENT_DETECT:

    self.charge_front()

    if front_distance < config.OPPONENT_CLOSE:
        self.brutal_push()

    continue

if back_distance < config.OPPONENT_DETECT:

    self.charge_back()

    continue
```

### Explanation

The robot continuously measures distance in front and behind itself.

Two thresholds are used:

* `OPPONENT_DETECT` identifies that an opponent exists nearby.
* `OPPONENT_CLOSE` indicates that the robot has reached pushing distance.

Using two thresholds allows different behaviours:

1. Search and approach when an opponent is detected.
2. Switch to aggressive pushing when close enough.

This prevents the robot from constantly performing push manoeuvres while still far away.

If an opponent is detected behind the robot, it first rotates approximately 180 degrees before attacking. This keeps the wedge or front pushing surface aimed at the opponent.

---

# Main Loop

The robot operates as a priority-based behaviour system.

```python
while True:

    front_edge = self.edges.front_edge()
    back_edge = self.edges.back_edge()

    if front_edge:

        self.front_escape(front_edge)
        continue

    if back_edge:

        self.back_escape()
        continue

    front_distance = self.front_ultra.distance()
    back_distance = self.back_ultra.distance()

    if front_distance < config.OPPONENT_DETECT:

        self.charge_front()
        continue

    if back_distance < config.OPPONENT_DETECT:

        self.charge_back()
        continue

    self.wander()
```

### Explanation

The robot follows a strict priority order:

1. Edge avoidance
2. Opponent attack
3. Search behaviour

The most important design decision was giving edge sensors higher priority than opponent detection.

If the robot detects both an opponent and the ring boundary at the same time, the edge response always executes first. Losing sight of an opponent is preferable to driving out of the arena and losing the match.

When neither an edge nor an opponent is detected, the robot enters a wandering mode where it moves forward and periodically rotates. This increases arena coverage and helps locate opponents.

Rather than implementing a complex state machine, a priority-based loop was chosen because the robot has only three primary behaviours and the logic remains easier to read.

---

# Recovery Behaviour

When an edge is detected, the robot performs a recovery manoeuvre.

```python
def front_escape(self, sensor):

    self.motors.reverse()

    time.sleep(config.FRONT_ESCAPE_TIME)

    if sensor == "FL":

        self.motors.turn_right()

    elif sensor == "FR":

        self.motors.turn_left()

    else:

        self.motors.turn_right()

    time.sleep(config.TURN_180_TIME)

    self.motors.stop()
```

### Explanation

The robot first creates distance from the edge by reversing.

The turning direction depends on which sensor detected the boundary. Turning away from the triggered sensor reduces the chance of immediately encountering the edge again.

The timings were experimentally tuned so that the robot reliably re-enters the arena before resuming normal operation.

---

# GPIO Cleanup

```python
robot = SumoRobot()

try:
    robot.run()

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    robot.cleanup()
```

### Explanation

The cleanup procedure stops all motors and releases the Raspberry Pi GPIO pins.

Without cleanup, GPIO outputs may remain in their previous state after the program exits. This can cause motors to continue receiving signals or leave pins configured incorrectly for the next execution.

Using a `finally` block guarantees cleanup runs regardless of how the program terminates.

`except KeyboardInterrupt` only handles the user pressing Ctrl+C. It does not handle unexpected errors such as:

* Sensor failures
* Programming mistakes
* Runtime exceptions

Because `finally` executes after both successful execution and exceptions, it provides a safer way to ensure the robot always shuts down correctly.


## Competition & Reflection

### Results


### What Worked


### What Failed


### Next Iteration

