import time
import statistics
import RPi.GPIO as GPIO

PIN = 3      # change to whichever photoresistor pin you want
SAMPLES = 100

GPIO.setmode(GPIO.BCM)

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

readings = []

print("Collecting samples...")

for _ in range(SAMPLES):

    value = rc_time(PIN)

    readings.append(value)

    print(value)

    time.sleep(0.05)

print("\nResults")
print("Mean:", statistics.mean(readings))
print("Min:", min(readings))
print("Max:", max(readings))
print("Std Dev:", statistics.stdev(readings))

GPIO.cleanup()
