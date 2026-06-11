import time


class UltrasonicSensor:

    def __init__(self, trigger, echo, gpio):

        self.trigger = trigger
        self.echo = echo
        self.GPIO = gpio

        gpio.setup(trigger, gpio.OUT)
        gpio.setup(echo, gpio.IN)

    def distance(self):

        self.GPIO.output(self.trigger, False)

        time.sleep(0.000002)

        self.GPIO.output(self.trigger, True)

        time.sleep(0.00001)

        self.GPIO.output(self.trigger, False)

        start = time.time()
        timeout = start + 0.03

        while self.GPIO.input(self.echo) == 0:

            start = time.time()

            if start > timeout:
                return 999

        stop = time.time()
        timeout = stop + 0.03

        while self.GPIO.input(self.echo) == 1:

            stop = time.time()

            if stop > timeout:
                return 999

        return ((stop - start) * 34300) / 2
