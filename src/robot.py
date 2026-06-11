import time
import RPi.GPIO as GPIO

import config

from motors import MotorController
from ultrasonic import UltrasonicSensor
from edge_sensors import EdgeSensors


class SumoRobot:

    def __init__(self):

        GPIO.setmode(GPIO.BCM)

        self.motors = MotorController()

        self.edges = EdgeSensors()

        self.front_ultra = UltrasonicSensor(
            config.TRIGGER_FRONT,
            config.ECHO_FRONT,
            GPIO
        )

        self.back_ultra = UltrasonicSensor(
            config.TRIGGER_BACK,
            config.ECHO_BACK,
            GPIO
        )

        GPIO.setup(
            config.BUTTON_PIN,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP
        )

        self.last_rotate = time.time()

    # ==========================
    # ESCAPE LOGIC
    # ==========================

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

        time.sleep(0.2)

    def back_escape(self):

        self.motors.forward()

        time.sleep(config.BACK_ESCAPE_TIME)

    def side_escape(self):

        self.motors.turn_right()

        time.sleep(config.TURN_90_TIME)

    # ==========================
    # ATTACK
    # ==========================

    def brutal_push(self):

        for _ in range(3):

            self.motors.forward()
            time.sleep(0.7)

            self.motors.reverse()
            time.sleep(0.25)

    def charge_front(self):

        self.motors.forward()

    def charge_back(self):

        self.motors.turn_right()

        time.sleep(config.TURN_180_TIME)

        self.motors.forward()

        time.sleep(1)

    # ==========================
    # WANDER
    # ==========================

    def wander(self):

        self.motors.forward()

        if (
            time.time() - self.last_rotate
            > config.WANDER_ROTATE_INTERVAL
        ):

            self.motors.turn_right()

            time.sleep(
                config.WANDER_ROTATE_TIME
            )

            self.last_rotate = time.time()

    # ==========================
    # MAIN LOOP
    # ==========================

    def run(self):

        print("Waiting for button")

        while GPIO.input(config.BUTTON_PIN):

            time.sleep(0.01)

        print("Start in 3 sec")

        time.sleep(config.START_DELAY)

        while True:

            front_edge = self.edges.front_edge()
            back_edge = self.edges.back_edge()

            # ==================================
            # PRIORITY 1 : EDGE SENSORS
            # ==================================

            if front_edge:

                self.front_escape(front_edge)
                continue

            if back_edge:

                self.back_escape()
                continue

            # ==================================
            # PRIORITY 2 : OPPONENT
            # ==================================

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

            # ==================================
            # PRIORITY 3 : WANDER
            # ==================================

            self.wander()

    def cleanup(self):

        self.motors.stop()

        GPIO.cleanup()
