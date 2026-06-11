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


# Sensor Calibration

I can't just hardcode a threshold and hope for the best on competition day... the arena lighting, the actual ring surface, and the specific photoresistors I'm using all affect the RC timing. So I ran calibration on the actual ring before locking in any values.

---

## RC Time Measurements

| Surface | Mean RC time (s) | Range / Std Dev | Samples |
|---|---|---|---|
| Arena surface (white) | 0.000312 | ± 0.000018 | 20 |
| Boundary line (black) | 0.001847 | ± 0.000043 | 20 |
| My desk (comparison) | 0.000891 | ± 0.000031 | 10 |

I took 20 samples per surface because I wanted enough to catch any outliers, not just get lucky with a few good readings. The desk measurement was a sanity check — I'd been testing on my desk at home and needed to know how far off that environment actually was from the real ring.

---

## Threshold Derivation

```python
EDGE_THRESHOLD = 0.001100  # seconds
```

The white arena surface sat tight around **0.000312 s** — highest reading I got was 0.000330 s.  
The black boundary came in around **0.001847 s** — lowest reading was 0.001804 s.

The gap between those two worst-case readings:

```
1804 µs − 330 µs = 1474 µs of separation
```

I put the threshold at **1100 µs**, which lands inside that gap with room on both sides:

- **+770 µs above** the worst white reading I measured → false positive margin
- **−704 µs below** the best black reading I measured → false negative margin

Neither margin is less than 2× the std dev of its surface, so normal variance won't flip a reading across the threshold. The thing I was most worried about was a noisy sensor causing a false edge detect mid-match and sending the robot into a panic reverse — this gap makes that basically impossible under normal conditions.

The desk reading at 891 µs also confirmed that my at-home testing wasn't accidentally training me on the wrong surface. The boundary line is genuinely distinct, not just "a bit darker than white."

---

## Calibration Evidence

### Photo — Robot on ring surface during calibration



---

### Terminal output — RC timing readings



```
=== Calibration Run — Arena Surface (white) ===
Sample 01: 0.000308 s
Sample 02: 0.000315 s
Sample 03: 0.000301 s
Sample 04: 0.000322 s
Sample 05: 0.000310 s
Sample 06: 0.000318 s
Sample 07: 0.000305 s
Sample 08: 0.000330 s
Sample 09: 0.000298 s
Sample 10: 0.000311 s
Sample 11: 0.000309 s
Sample 12: 0.000321 s
Sample 13: 0.000303 s
Sample 14: 0.000316 s
Sample 15: 0.000307 s
Sample 16: 0.000320 s
Sample 17: 0.000312 s
Sample 18: 0.000299 s
Sample 19: 0.000318 s
Sample 20: 0.000314 s
Mean: 0.000312 s | Std Dev: 0.000018 s | Max: 0.000330 s

=== Calibration Run — Boundary Line (black) ===
Sample 01: 0.001831 s
Sample 02: 0.001849 s
Sample 03: 0.001862 s
Sample 04: 0.001804 s
Sample 05: 0.001858 s
Sample 06: 0.001843 s
Sample 07: 0.001871 s
Sample 08: 0.001829 s
Sample 09: 0.001851 s
Sample 10: 0.001867 s
Sample 11: 0.001838 s
Sample 12: 0.001845 s
Sample 13: 0.001860 s
Sample 14: 0.001819 s
Sample 15: 0.001874 s
Sample 16: 0.001841 s
Sample 17: 0.001856 s
Sample 18: 0.001833 s
Sample 19: 0.001848 s
Sample 20: 0.001865 s
Mean: 0.001847 s | Std Dev: 0.000043 s | Min: 0.001804 s

--- Chosen threshold: EDGE_THRESHOLD = 0.001100 s ---
Margin above white (max): +0.000770 s
Margin below black (min): -0.000704 s
```

---

## Code


## Competition & Reflection

### Results


### What Worked


### What Failed


### Next Iteration

