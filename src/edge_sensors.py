import time
import RPi.GPIO as GPIO
import config


class EdgeSensors:

    def rc_time(self, pin):

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

    def detected(self, pin):

        return self.rc_time(pin) > config.THRESHOLD

    def front_edge(self):

        if self.detected(config.FL):
            return "FL"

        if self.detected(config.FC):
            return "FC"

        if self.detected(config.FR):
            return "FR"

        return None

    def back_edge(self):

        if self.detected(config.BL):
            return "BL"

        if self.detected(config.BC):
            return "BC"

        if self.detected(config.BR):
            return "BR"

        return None
