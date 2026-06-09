import RPi.GPIO as GPIO
import time

# ============================
# PIN DEFINITIONS
# ============================

# Start button
Button_Pin = 0      

# LED indicators
LEDS = [ ]        

# Photoresistor pins
FL = 0             
FC = 0
FR = 0

BL = 0
BC = 0
BR = 0

# Left H-bridge
FrontL_EN = 0
FrontL_IN1 = 0
FrontL_IN2 = 0

RearL_EN = 0
RearL_IN1 = 0
RearL_IN2 = 0

# Right H-bridge
FrontR_EN = 0
FrontR_IN1 = 0
FrontR_IN2 = 0

RearR_EN = 0
RearR_IN1 = 0
RearR_IN2 = 0

# Distance sensors
trigger_pin_front = 0       
echo_pin_front = 0

trigger_pin_back = 0        
echo_pin_back = 0

# ============================
# CONSTANTS
# ============================

THRESHOLD = 500

WANDER_SPEED = 60
ATTACK_SPEED = 85
FULL_SPEED = 100

START_DELAY = 3

GPIO.setmode(GPIO.BCM)

# ============================
# LED SETUP
# ============================

for led in LEDS:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)

# ============================
# MOTOR SETUP
# ============================

motor_pins = [
    FrontL_IN1, FrontL_IN2, RearL_IN1, RearL_IN2,
    FrontR_IN1, FrontR_IN2, RearR_IN1, RearR_IN2,
    FrontL_EN, RearL_EN, FrontR_EN, RearR_EN
]

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# PWM
pwm_fl = GPIO.PWM(FrontL_EN, 1000)
pwm_rl = GPIO.PWM(RearL_EN, 1000)
pwm_fr = GPIO.PWM(FrontR_EN, 1000)
pwm_rr = GPIO.PWM(RearR_EN, 1000)

for pwm in [pwm_fl, pwm_rl, pwm_fr, pwm_rr]:
    pwm.start(0)

# ============================
# RC EDGE SENSORS
# ============================

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

def front_edge():
    return edge(FL) or edge(FC) or edge(FR)

def back_edge():
    return edge(BL) or edge(BC) or edge(BR)

# ============================
# MOTOR HELPERS
# ============================

def set_speed(speed):
    pwm_fl.ChangeDutyCycle(speed)
    pwm_rl.ChangeDutyCycle(speed)
    pwm_fr.ChangeDutyCycle(speed)
    pwm_rr.ChangeDutyCycle(speed)

def stop():
    set_speed(0)

# ============================
# DISTANCE SENSOR HELPERS
# ============================

def read_distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(echo_pin) == GPIO.LOW:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo_pin) == GPIO.HIGH:
        stop_time = time.time()

    elapsed = stop_time - start_time
    distance_cm = (elapsed * 34300) / 2
    return distance_cm

def front_opponent_detected():
    return read_distance(trigger_pin_front, echo_pin_front) < 40

def back_opponent_detected():
    return read_distance(trigger_pin_back, echo_pin_back) < 40

# ============================
# MOVEMENT
# ============================

def forward(speed):
    GPIO.output(FrontL_IN1, GPIO.HIGH)
    GPIO.output(FrontL_IN2, GPIO.LOW)

    GPIO.output(RearL_IN1, GPIO.HIGH)
    GPIO.output(RearL_IN2, GPIO.LOW)

    GPIO.output(FrontR_IN1, GPIO.HIGH)
    GPIO.output(FrontR_IN2, GPIO.LOW)

    GPIO.output(RearR_IN1, GPIO.HIGH)
    GPIO.output(RearR_IN2, GPIO.LOW)

    set_speed(speed)

def reverse(speed):
    GPIO.output(FrontL_IN1, GPIO.LOW)
    GPIO.output(FrontL_IN2, GPIO.HIGH)

    GPIO.output(RearL_IN1, GPIO.LOW)
    GPIO.output(RearL_IN2, GPIO.HIGH)

    GPIO.output(FrontR_IN1, GPIO.LOW)
    GPIO.output(FrontR_IN2, GPIO.HIGH)

    GPIO.output(RearR_IN1, GPIO.LOW)
    GPIO.output(RearR_IN2, GPIO.HIGH)

    set_speed(speed)

def turn_left(speed):
    GPIO.output(FrontL_IN1, GPIO.LOW)
    GPIO.output(FrontL_IN2, GPIO.HIGH)

    GPIO.output(RearL_IN1, GPIO.LOW)
    GPIO.output(RearL_IN2, GPIO.HIGH)

    GPIO.output(FrontR_IN1, GPIO.HIGH)
    GPIO.output(FrontR_IN2, GPIO.LOW)

    GPIO.output(RearR_IN1, GPIO.HIGH)
    GPIO.output(RearR_IN2, GPIO.LOW)

    set_speed(speed)

def turn_right(speed):
    GPIO.output(FrontL_IN1, GPIO.HIGH)
    GPIO.output(FrontL_IN2, GPIO.LOW)

    GPIO.output(RearL_IN1, GPIO.HIGH)
    GPIO.output(RearL_IN2, GPIO.LOW)

    GPIO.output(FrontR_IN1, GPIO.LOW)
    GPIO.output(FrontR_IN2, GPIO.HIGH)

    GPIO.output(RearR_IN1, GPIO.LOW)
    GPIO.output(RearR_IN2, GPIO.HIGH)

    set_speed(speed)

# ============================
# ACTIONS
# ============================

def front_escape():
    print("Front edge!")
    reverse(ATTACK_SPEED)
    time.sleep(0.8)
    turn_right(ATTACK_SPEED)
    time.sleep(0.5)
    stop()

def back_escape():
    print("Back edge!")
    forward(ATTACK_SPEED)
    time.sleep(0.8)

def charge():
    forward(FULL_SPEED)

def brutal_push():
    print("Brutal push")
    for _ in range(3):
        forward(FULL_SPEED)
        time.sleep(0.7)
        reverse(70)
        time.sleep(0.2)

# ============================
# WANDER MODE
# ============================

last_turn = time.time()

def wander():
    global last_turn
    forward(WANDER_SPEED)

    if time.time() - last_turn > 5:
        turn_right(WANDER_SPEED)
        time.sleep(0.5)
        last_turn = time.time()

# ============================
# MAIN LOGIC
# ============================

print("Waiting for start button...")

GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while GPIO.input(Button_Pin) == GPIO.HIGH:
    time.sleep(0.01)

print("Button pressed! Starting in 3 seconds...")
time.sleep(START_DELAY)

while True:

    if front_edge():
        front_escape()

    elif back_edge():
        back_escape()

    elif front_opponent_detected():
        charge()

    elif back_opponent_detected():
        turn_right(80)
        time.sleep(1.0)
        charge()

    else:
        wander()



