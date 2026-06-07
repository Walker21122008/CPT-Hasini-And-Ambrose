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

<img width="644" height="641" alt="image" src="https://github.com/user-attachments/assets/c85bfc5e-1b29-457b-9b25-cff29baf05be" />


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



### Wiring



### Decisions Made During the Build


# Sensor Calibration

I can't just hardcode a threshold and hope for the best on competition day... the arena lighting, the actual ring surface, and the specific photoresistors I'm using all affect the RC timing. So I ran calibration on the actual dohyo ring before locking in any values.

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

