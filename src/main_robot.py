import RPi.GPIO as GPIO
import time

# ==================================================
# PIN DEFINITIONS
# ==================================================

Button_Pin = 2

# Front edge sensors
FL = 3
FC = 4
FR = 17

# Back edge sensors
BL = 27
BC = 22
BR = 10

# Motor pins

FrontL_IN1 = 12
FrontL_IN2 = 16

RearL_IN1 = 25
RearL_IN2 = 24

FrontR_IN1 = 20
FrontR_IN2 = 21

RearR_IN1 = 7
RearR_IN2 = 8

# Ultrasonic sensors

trigger_pin_front = 0
echo_pin_front = 0

trigger_pin_back = 0
echo_pin_back = 0

# ==================================================
# CONSTANTS
# ==================================================

THRESHOLD = 500

START_DELAY = 3

OPPONENT_DETECT = 40
OPPONENT_CLOSE = 15

TURN_90_TIME = 0.45
TURN_180_TIME = 0.90

FRONT_ESCAPE_TIME = 0.8
BACK_ESCAPE_TIME = 1.2

GPIO.setmode(GPIO.BCM)

# ==================================================
# SETUP
# ==================================================

motor_pins = [
    FrontL_IN1, FrontL_IN2,
    RearL_IN1, RearL_IN2,
    FrontR_IN1, FrontR_IN2,
    RearR_IN1, RearR_IN2
]

for pin in motor_pins:
    if pin != 0:
        GPIO.setup(pin, GPIO.OUT)

GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(trigger_pin_front, GPIO.OUT)
GPIO.setup(echo_pin_front, GPIO.IN)

GPIO.setup(trigger_pin_back, GPIO.OUT)
GPIO.setup(echo_pin_back, GPIO.IN)

# ==================================================
# EDGE SENSOR FUNCTIONS
# ==================================================

def rc_time(pin):

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

    time.sleep(0.001)

    GPIO.setup(pin, GPIO.IN)

    count = 0

    while GPIO.input(pin) == GPIO.LOW:

        count += 1

        if count > 5000:
            break

    return count

def edge(pin):
    return rc_time(pin) > THRESHOLD

def get_front_edge():

    if edge(FL):
        return "FL"

    if edge(FC):
        return "FC"

    if edge(FR):
        return "FR"

    return None

def get_back_edge():

    if edge(BL):
        return "BL"

    if edge(BC):
        return "BC"

    if edge(BR):
        return "BR"

    return None

# ==================================================
# ULTRASONIC FUNCTIONS
# ==================================================

def read_distance(trigger_pin, echo_pin):

    GPIO.output(trigger_pin, GPIO.LOW)
    time.sleep(0.000002)

    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    start_time = time.time()
    timeout = start_time + 0.03

    while GPIO.input(echo_pin) == GPIO.LOW:

        start_time = time.time()

        if start_time > timeout:
            return 999

    stop_time = time.time()
    timeout = stop_time + 0.03

    while GPIO.input(echo_pin) == GPIO.HIGH:

        stop_time = time.time()

        if stop_time > timeout:
            return 999

    elapsed = stop_time - start_time

    distance_cm = (elapsed * 34300) / 2

    return distance_cm

def front_opponent_detected():

    return read_distance(
        trigger_pin_front,
        echo_pin_front
    ) < OPPONENT_DETECT

def back_opponent_detected():

    return read_distance(
        trigger_pin_back,
        echo_pin_back
    ) < OPPONENT_DETECT

def opponent_close():

    return read_distance(
        trigger_pin_front,
        echo_pin_front
    ) < OPPONENT_CLOSE

# ==================================================
# MOVEMENT
# ==================================================

def stop():

    GPIO.output(FrontL_IN1, GPIO.LOW)
    GPIO.output(FrontL_IN2, GPIO.LOW)

    GPIO.output(RearL_IN1, GPIO.LOW)
    GPIO.output(RearL_IN2, GPIO.LOW)

    GPIO.output(FrontR_IN1, GPIO.LOW)
    GPIO.output(FrontR_IN2, GPIO.LOW)

    GPIO.output(RearR_IN1, GPIO.LOW)
    GPIO.output(RearR_IN2, GPIO.LOW)

def forward():

    GPIO.output(FrontL_IN1, GPIO.HIGH)
    GPIO.output(FrontL_IN2, GPIO.LOW)

    GPIO.output(RearL_IN1, GPIO.HIGH)
    GPIO.output(RearL_IN2, GPIO.LOW)

    GPIO.output(FrontR_IN1, GPIO.HIGH)
    GPIO.output(FrontR_IN2, GPIO.LOW)

    GPIO.output(RearR_IN1, GPIO.HIGH)
    GPIO.output(RearR_IN2, GPIO.LOW)

def reverse():

    GPIO.output(FrontL_IN1, GPIO.LOW)
    GPIO.output(FrontL_IN2, GPIO.HIGH)

    GPIO.output(RearL_IN1, GPIO.LOW)
    GPIO.output(RearL_IN2, GPIO.HIGH)

    GPIO.output(FrontR_IN1, GPIO.LOW)
    GPIO.output(FrontR_IN2, GPIO.HIGH)

    GPIO.output(RearR_IN1, GPIO.LOW)
    GPIO.output(RearR_IN2, GPIO.HIGH)

def turn_left():

    GPIO.output(FrontL_IN1, GPIO.LOW)
    GPIO.output(FrontL_IN2, GPIO.HIGH)

    GPIO.output(RearL_IN1, GPIO.LOW)
    GPIO.output(RearL_IN2, GPIO.HIGH)

    GPIO.output(FrontR_IN1, GPIO.HIGH)
    GPIO.output(FrontR_IN2, GPIO.LOW)

    GPIO.output(RearR_IN1, GPIO.HIGH)
    GPIO.output(RearR_IN2, GPIO.LOW)

def turn_right():

    GPIO.output(FrontL_IN1, GPIO.HIGH)
    GPIO.output(FrontL_IN2, GPIO.LOW)

    GPIO.output(RearL_IN1, GPIO.HIGH)
    GPIO.output(RearL_IN2, GPIO.LOW)

    GPIO.output(FrontR_IN1, GPIO.LOW)
    GPIO.output(FrontR_IN2, GPIO.HIGH)

    GPIO.output(RearR_IN1, GPIO.LOW)
    GPIO.output(RearR_IN2, GPIO.HIGH)

# ==================================================
# RECOVERY
# ==================================================

def front_escape(sensor):

    print("Front edge:", sensor)

    reverse()
    time.sleep(FRONT_ESCAPE_TIME)

    if sensor == "FL":

        turn_right()
        time.sleep(TURN_180_TIME)

    elif sensor == "FR":

        turn_left()
        time.sleep(TURN_180_TIME)

    else:

        turn_right()
        time.sleep(TURN_180_TIME)

    stop()
    time.sleep(0.2)

def back_escape():

    print("Back edge")

    forward()
    time.sleep(BACK_ESCAPE_TIME)

def side_escape():

    turn_right()
    time.sleep(TURN_90_TIME)

# ==================================================
# ATTACK
# ==================================================

def brutal_push():

    print("BRUTAL PUSH")

    for _ in range(3):

        forward()
        time.sleep(0.7)

        reverse()
        time.sleep(0.25)

def charge():

    while True:

        if get_front_edge():
            return

        if get_back_edge():
            return

        forward()

        if opponent_close():

            brutal_push()
            return

def engage_back_opponent():

    turn_right()
    time.sleep(TURN_180_TIME)

    charge()

# ==================================================
# WANDER
# ==================================================

last_turn = time.time()

def wander():

    global last_turn

    forward()

    if time.time() - last_turn > 5:

        turn_right()
        time.sleep(0.5)

        last_turn = time.time()

# ==================================================
# MAIN
# ==================================================

print("Waiting for start button...")

while GPIO.input(Button_Pin) == GPIO.HIGH:
    time.sleep(0.01)

print("Button pressed.")
print("Starting in 3 seconds...")

time.sleep(START_DELAY)

try:

    while True:

        front_edge = get_front_edge()
        back_edge = get_back_edge()

        # ------------------------------------------
        # EDGE PRIORITY (ALSO HANDLES CONFLICTS)
        # ------------------------------------------

        if front_edge:

            front_escape(front_edge)
            continue

        if back_edge:

            back_escape()
            continue

        # ------------------------------------------
        # OPPONENT DETECTION
        # ------------------------------------------

        if front_opponent_detected():

            charge()
            continue

        if back_opponent_detected():

            engage_back_opponent()
            continue

        # ------------------------------------------
        # DEFAULT
        # ------------------------------------------

        wander()

except KeyboardInterrupt:

    stop()
    GPIO.cleanup()



