# Sumo Robot: Cheng 2.0

**Capaccino Assasino** — Hasini and Ambrose

> *What does your robot do and how does it compete? If you added any extensions beyond the guided build, mention them here. Write this after the rest of the document is done.*

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
> **Branch point:** After edge/conflict resolution, check — is it the back sensor that triggered?
 
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

<img width="344" height="341" alt="image" src="https://github.com/user-attachments/assets/c85bfc5e-1b29-457b-9b25-cff29baf05be" />


### Circuit Design


### Physical Layout


## Build


### Chassis



### Wiring



### Decisions Made During the Build


### Calibration



---

## Code


## Competition & Reflection

### Results


### What Worked


### What Failed


### Next Iteration

