import RPi.GPIO as GPIO
import config


class MotorController:

    def __init__(self):

        pins = [
            config.FRONTL_IN1,
            config.FRONTL_IN2,
            config.REARL_IN1,
            config.REARL_IN2,
            config.FRONTR_IN1,
            config.FRONTR_IN2,
            config.REARR_IN1,
            config.REARR_IN2
        ]

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def stop(self):

        outputs = [
            config.FRONTL_IN1,
            config.FRONTL_IN2,
            config.REARL_IN1,
            config.REARL_IN2,
            config.FRONTR_IN1,
            config.FRONTR_IN2,
            config.REARR_IN1,
            config.REARR_IN2
        ]

        for pin in outputs:
            GPIO.output(pin, GPIO.LOW)

    def forward(self):

        GPIO.output(config.FRONTL_IN1, GPIO.HIGH)
        GPIO.output(config.FRONTL_IN2, GPIO.LOW)

        GPIO.output(config.REARL_IN1, GPIO.HIGH)
        GPIO.output(config.REARL_IN2, GPIO.LOW)

        GPIO.output(config.FRONTR_IN1, GPIO.HIGH)
        GPIO.output(config.FRONTR_IN2, GPIO.LOW)

        GPIO.output(config.REARR_IN1, GPIO.HIGH)
        GPIO.output(config.REARR_IN2, GPIO.LOW)

    def reverse(self):

        GPIO.output(config.FRONTL_IN1, GPIO.LOW)
        GPIO.output(config.FRONTL_IN2, GPIO.HIGH)

        GPIO.output(config.REARL_IN1, GPIO.LOW)
        GPIO.output(config.REARL_IN2, GPIO.HIGH)

        GPIO.output(config.FRONTR_IN1, GPIO.LOW)
        GPIO.output(config.FRONTR_IN2, GPIO.HIGH)

        GPIO.output(config.REARR_IN1, GPIO.LOW)
        GPIO.output(config.REARR_IN2, GPIO.HIGH)

    def turn_right(self):

        GPIO.output(config.FRONTL_IN1, GPIO.HIGH)
        GPIO.output(config.FRONTL_IN2, GPIO.LOW)

        GPIO.output(config.REARL_IN1, GPIO.HIGH)
        GPIO.output(config.REARL_IN2, GPIO.LOW)

        GPIO.output(config.FRONTR_IN1, GPIO.LOW)
        GPIO.output(config.FRONTR_IN2, GPIO.HIGH)

        GPIO.output(config.REARR_IN1, GPIO.LOW)
        GPIO.output(config.REARR_IN2, GPIO.HIGH)

    def turn_left(self):

        GPIO.output(config.FRONTL_IN1, GPIO.LOW)
        GPIO.output(config.FRONTL_IN2, GPIO.HIGH)

        GPIO.output(config.REARL_IN1, GPIO.LOW)
        GPIO.output(config.REARL_IN2, GPIO.HIGH)

        GPIO.output(config.FRONTR_IN1, GPIO.HIGH)
        GPIO.output(config.FRONTR_IN2, GPIO.LOW)

        GPIO.output(config.REARR_IN1, GPIO.HIGH)
        GPIO.output(config.REARR_IN2, GPIO.LOW)
