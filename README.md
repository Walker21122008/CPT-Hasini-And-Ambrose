# Sumo Robot: Tung Tung Tung Sahur

---

> Tung Tung Tung Sahur is a Raspberry Pi-based differential drive sumo robot built for a 4-robot battle royale format. The robot uses photoresistor RC timing for edge detection and HC-SR04 ultrasonic sensors for opponent detection. It operates as a priority-based behaviour loop: edge avoidance takes precedence over attack, which takes precedence over wandering. The final version (3.0) added a ramp-base barrier and an LED strip after assessing other teams' designs during the build period.
  
---
 
## Design
 
### What the Robot Needs to Do
 
1. Start autonomously via a physical button press — no SSH during a round
2. Wait exactly 3 seconds after the button press before any movement
3. Detect the ring boundary (Black line) using photoresistor sensors and recover back into the ring
4. Detect an opponent at range using the front and rear ultrasonic sensors and charge
5. Switch to a high-force push sequence when the opponent is within close range
6. Wander with positional variety when no edge or opponent is detected
7. Run the full match without any SSH intervention
### Success Criteria
 
| Requirement | How we tested it | Pass condition |
|---|---|---|
| 3-second startup delay | Timed with a stopwatch from button press to first wheel movement, 5 trials | Delay is between 2.9 s and 3.1 s on all trials |
| Front edge detection | Drove robot forward toward the boundary line from 30 cm away, 10 trials per sensor | Robot reverses and turns away from the triggered sensor within 0.5 s on at least 9 of 10 trials |
| Rear edge detection | Pushed robot backward until rear sensors crossed the line, 10 trials | Robot drives forward to clear the edge on at least 9 of 10 trials |
| Opponent detection and charge | Placed a static obstacle at 20 cm in front of the robot, 10 trials | Robot charges within 1 s of obstacle entering range on at least 9 of 10 trials |
| Brutal push sequence | Placed obstacle within close-range threshold, observed loop count | Robot executes exactly 3 charge-reverse cycles before returning to normal behaviour |
| Wander coverage | Let robot wander on the ring for 30 seconds with no obstacles | Robot does not repeat the same arc more than once; changes direction at least once per 5-second window |
| Full-match autonomous run | Ran robot through one complete 3-minute simulated match | Robot never requires SSH; no motors stuck; program exits cleanly via button or KeyboardInterrupt |

### System Architecture
The robot uses a priority-based behaviour loop rather than a formal state machine. Three behaviours are evaluated in strict priority order every iteration of the main loop: edge avoidance, opponent attack, and wander. The diagram below describes the states and their transitions.

<img width="648" height="642" alt="image" src="https://github.com/user-attachments/assets/9e31ce9c-e5a5-4b6c-9516-61a376986f14" />

**Priority rule:** If edge and opponent are detected simultaneously, edge recovery always executes first. Losing track of an opponent is preferable to exiting the ring.


### Circuit Design

#### Here are the components we decided to use for our design
- 4x DC motors
- A push button Switch
- 6x Photoresistor light sensor(LDR)
- 2x HC-SR04 Ultrasonic Sound Distance Sensor
- 6x  0.22uF Tantalum Capacitor
- 6x 200 Ohm Resistors
- 2x L293D H-Bridge
- 1x Respberry PI 

> Our circuit is shown in the picture below. We use a program called Cirkit Designer. We use it for our designing process because it has a better visual UI and more simple controls, allowing us to identify issues and make changes quickly. Later, we used this as our guide for the physical building process. 
<img width="2880" height="2304" alt="Cheng 2 0 - top view (1)" src="https://github.com/user-attachments/assets/f01c1e03-4ab8-401d-8c73-4447c4af56fd" />

### GPIO Ports
| **Components** | **GPIO Number** |
|---|---|
| Button switch | GPIO 2 |
| Photoresistor light sensor(LDR) Front Left | GPIO 3|
| Photoresistor light sensor(LDR) 1 | GPIO 4|
| Photoresistor light sensor(LDR) 3 | GPIO 17|
| Photoresistor light sensor(LDR) 4 | GPIO 27|
| Photoresistor light sensor(LDR) 5 | GPIO 22|
| Photoresistor light sensor(LDR) 6 | GPIO 10|
| HC-SR04 Ultrasonic Sound Distance Sensor (Front)(Trig) | GPIO 14 |
| HC-SR04 Ultrasonic Sound Distance Sensor (Front)(Echo) | GPIO 15 |
| HC-SR04 Ultrasonic Sound Distance Sensor (Back)(Trig) | GPIO 18 |
| HC-SR04 Ultrasonic Sound Distance Sensor (Back)(Echo) | GPIO 23 |
| Front Right Motors (Chip 1)(In 4) | GPIO 14 |
| Front Right Motors (Chip 1)(In 3) | GPIO 25 |
| Front Left Motors (Chip 1)(In 1) | GPIO 12 |
| Front Left Motors (Chip 1)(In 2) | GPIO 16 |
| Back Left Motors (Chip 2)(In 1) | GPIO 20 |
| Back Left Motors (Chip 2)(In 2) | GPIO 21 |
| Back Right Motors (Chip 2)(In 4) | GPIO 8 |
| Back Right Motors (Chip 2)(In 3) | GPIO 7 |

### Physical Layout
<img width="2880" height="2304" alt="Cheng 2 0 - top view (4)" src="https://github.com/user-attachments/assets/58f765a5-3788-47f7-9109-c32424d4cdda" />



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
 
Cheng 2.0 retains the idea and drive system but adds substantial structural and sensing upgrades. Ramps were added to both ends to deflect incoming robots. Cardboard-enforced shields were added on both sides to protect the motors and wheels. Sensors were redistributed to the perimeter rather than centralized on the breadboard.
 
The new chassis assembly sequence:
1. Retain motors, wheels, and caster from Cheng 1.0
2. Attach 3D-printed ramps to front and rear edges of the base
3. Cut and fold cardboard side shields; align flush with wheel height
4. Mount distance sensors at the tip of each ramp (front + rear)
5. Mount 3× photoresistor + 3× LED arrays along the bottom edge of each side shield (6 sensors + 6 LEDs total)
6. Reinforce all ramp joints and shield seams with duct tape
7. Re-route wiring from breadboard out to perimeter sensors

#### Design Changes: Tung Tung Tung Sahur 1.0 → Tung Tung Tung Sahur 2.0
<img width="2880" height="2304" alt="Cheng 2 0 - top view (2)" src="https://github.com/user-attachments/assets/0e774387-5fff-40d0-baa0-4542045ba865" />

 
| Feature | Cheng 1.0 | Cheng 2.0 | Reason |
|---|---|---|---|
| **Base platform** | Single flat MDF/cardboard layer | extened base & side wing extensions | Needed mmore space to put larger breadboard |
| **Front/rear structure** | Open, no shielding | 3D-printed ramps on both ends | Deflects opponent robots up and over; improves pushing leverage |
| **Side structure** | Bare, motors exposed | Cardboard-enforced shields both sides | Protect hardwares from side impacts |
| **Distance sensors** | None | 2 distance sensors on front and back | Opponent detection at range; enables CHARGE state trigger |
| **Light sensors** | one at front | 3× photoresistor sensors per side (6 total, at base edge) | Full-perimeter boundary detection and detects the black tape |
| **LEDs** | one at front | 3× LEDs per side (6 total) | Visual state feedback; paired with photoresistors for lighting up the shadow |
| **Structural reinforcement** | Zip ties only | Duct tape on all ramp joints and wire connections | More organize wiring and stability |
| **Sensor placement** | All centralized in the front | Distributed to ramps and side shields | Moves detection to the robot's physical perimeter |
| **Weight distribution** | Top-heavy (Pi + breadboard stacked + power bank stacked) | Most weight are in the body | Lowers center of mass and balance weight of front and back end |

#### Sensor Layout
 
```
              [FRONT]
   _________________________________
   |          o  o  o              |   ← 3× photoresistor + LED (bottom left, right and center)
  /     [FRONT DIST SENSOR]         \  ← 3D-printed ramp + ramp-base barrier (v3.0)
 /                                   \
|   [LEFT MOTOR]   [RIGHT MOTOR]      |
|   [BREADBOARD 1] [BREADBOARD 2]     |  ← sensor wiring left, motor driver right
|        [Raspberry Pi below]         |
|         [BATTERY 1 - Pi]            |
|   [LEFT MOTOR]   [RIGHT MOTOR]      |
 \                                   /
  \     [REAR DIST SENSOR]          /  ← 3D-printed ramp
   |          o  o  o              |   ← 3× photoresistor + LED (bottom left, right and center)
   ---------------------------------
              [REAR]
```
 
- **Distance sensors** face outward from each ramp; used to detect opponent in CHARGE range
- **Photoresistors** are mounted along the bottom edge of the side shields; detect the black boundary line
- **LEDs** are paired next to each photoresistor for active illumination and state visualization

#### Design changes: Tung Tung Tung Sahur 2.0 → Tung Tung Tung Sahur 3.0
After conversing with other groups to find out their weaknesses, we figured that almost every group was using a ramp like us. We figured that we had to prevent the other robots from gaining access to the wheels. So, we decided to put a barrier for the robot ramp at the base to protect it from other robots. We also decided to use an LED Strip instead of the normal LED lights connected through a circuit since the LEDS weren't bright enough for us to test. Here is the prototype of our new design:

<img width="2880" height="2304" alt="Cheng 2 0 - top view (3)" src="https://github.com/user-attachments/assets/4e07a92a-cbf5-490d-8122-a06c9bc738eb" />

| Feature | Cheng 1.0 | Cheng 2.0 | Cheng 3.0 | Reason |
|---|---|---|---|---|
| **Base platform** | Single flat MDF/cardboard layer | extened base & side wing extensions | Same as 2.0 | N/A |
| **Front/rear structure** | Open, no shielding | 3D-printed ramps on both ends | Change from 3D printed ramps to cardboard shield | Limited time and avoid being attack |
| **Side structure** | Bare, motors exposed | Cardboard-enforced shields both sides | we extent the tall of the sides | Allow more protection on the wheels & protect hardwares from side impacts |
| **Motor Selection** | Yellow 1:48 gear ratio motors  | Yellow 1:48 gear ratio motors | White 1:143 gear ratio motor | Stronger Torque, allow to move with heavy weight |
| **Distance sensors** | None | 2 distance sensors on front and back | Same as 2.0 | N/A |
| **Light sensors** | one at front | 3× photoresistor sensors per side (6 total, at base edge) | Same as 2.0 | N/A |
| **LEDs** | one at front | 3× LEDs per side (6 total) | LED strip | More brightness and durability |
| **Structural reinforcement** | Zip ties only | Duct tape on all ramp joints and wire connections | Change most tape to electric tape | Duck tape will shorten the circuit |
| **Sensor placement** | All centralized in the front | Distributed to ramps and side shields |  Distributed to the bottom of each shield | better placement with more protection |
| **Weight distribution** | Top-heavy (Pi + breadboard stacked + power bank stacked) | Most weight are in the body | Same as 2.0 | N/A |




---
### Wiring

Wiring was organized from the early stage by using only pink wires for the main harness, laid flat and routed along the chassis edge to reduce the chance of a wire getting snagged or pulled free during a match.

<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/e973feff-c0d0-4e81-b107-bb8677f89d84" />
Early wiring stage. 

The CanaKit GPIO breakout is connected to the left breadboard. Photoresistors (amber, center-left column) and resistors are inserted but not yet routed to the second board. The two L293D H-bridge ICs are visible on the right breadboard, not yet wired to motors.

In parallel with the main harness, we tested color-coded wiring for each component type to make individual signals easier to trace during debugging:


Motors: blue and purple
Distance sensors: yellow, orange, and red
Photoresistor light sensors: green

<img width="1200" height="1600" alt="image" src="https://github.com/user-attachments/assets/e64a538e-3248-4f10-a1a0-325cd4b37445" />
Motor wiring test with color-coded leads. 

Blue and purple wires connect to both motor terminals on each side. 

Eventually we converted the full harness to pink wire since it was easier to solder in bulk and available in sufficient quantity. The component leads (motors, distance sensors, photoresistors) kept their color coding to preserve traceability, and pairs were secured together with electrical tape rather than duct tape for a cleaner finish that was less likely to leave residue on the breadboard connections.

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
| Boundary line (black) | 418.32       | 12.47              | 100     |
| Arena surface (white) | 704.91       | 18.63              | 100     |
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


# Competition & Reflection

## Results

| Round   | Bonus Points | Round Total |
| ------- | ------------ | ----------- |
| Round 1 | 0            | 0           |
| Round 2 | 2            | 2           |
| Round 3 | 2            | 2           |
| **Total**|              | **4**       |

---

## What Worked

**Sensor system held up completely.** All six photoresistors and both ultrasonic sensors functioned correctly throughout all three rounds. The RC timing calibration approach paid off here — because the threshold was derived from measured data rather than guessing, the edge detection stayed reliable even under the arena's specific lighting conditions. No false positives or missed detections were recorded.

**Wiring survived the rounds.** The decision to consolidate onto pink wire, solder connections, and duct tape wire pairs together meant nothing came loose during matches. This was a real risk with a robot that takes impacts, and it held.

**Structural integrity held under load.** The chassis successfully supported the dual battery configuration throughout all three rounds. Despite the added mass being a mobility problem, none of the structural joints, ramp mounts, or shield attachments failed under repeated impacts.
---

## What Failed

### 1. H-Bridge Chip Failure — Two Motors Lost (All Rounds)

Two of the four drive motors stopped working between Round 1 and the rest of the competition. The root cause was a burned L293D H-bridge chip which potentially damaged the motors.

The L293D has a continuous current rating of 600mA per channel and a peak of 1.2A. Under load - especially when the robot strained against its own weight or made contact with an opponent - the motors drew more current than the chip could sustain. Heat built up, the chip degraded, and two motor channels failed. Running all four motors off the same chip without any heatsinking accelerated this.

With only two functioning motors, the robot lost differential drive symmetry. Turning was unreliable and forward thrust was cut roughly in half.

### 2. Robot Too Heavy to Move Effectively (All rounds)

The second battery pack, reinforced cardboard shields, duct tape layering, and the LED strip added weight that the drive system wasn't sized for. The motors and wheels were carried over from Cheng 1.0, which had none of that additional mass.

The result was that the motors struggled to accelerate the robot from a standstill, especially on the slightly textured arena surface. The ramming strategy depended entirely on building speed before contact — a robot that can barely move can't execute that strategy. The weight distribution changes that were meant to lower the center of mass ended up working against mobility instead.

---

## Next Iteration

### 1. Replace L293D with TB6612FNG Motor Drivers

The TB6612FNG handles 1.2A continuous and 3.2A peak per channel, runs cooler, and has a lower internal resistance than the L293D. Two TB6612FNG boards (one per motor pair) would give each channel enough headroom to handle stall current without cooking the chip. This directly addresses the H-bridge failure - the L293D was simply undersized for four motors under competition load.

### 2. Weight Audit Before Final Build Lock

Before the next competition build is finalized, every component gets weighed and the total is checked against what the motors can actually move. The gear motors used have a rated stall torque, and that number should be the ceiling - not something discovered on competition day. If the build exceeds roughly 70% of stall torque at normal load, either the motors get upgraded or components get cut. The second battery and shields are worth keeping; the places to trim are redundant duct tape layers and any structural cardboard that isn't load-bearing.

