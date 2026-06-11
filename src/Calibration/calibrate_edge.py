import time
import statistics
import RPi.GPIO as GPIO

# Front Sensors
FL = 3
FC = 4
FR = 17

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

try:

    fl_readings = []
    fc_readings = []
    fr_readings = []

    print(f"Collecting {SAMPLES} samples...\n")

    for i in range(SAMPLES):

        fl = rc_time(FL)
        fc = rc_time(FC)
        fr = rc_time(FR)

        fl_readings.append(fl)
        fc_readings.append(fc)
        fr_readings.append(fr)

        print(
            f"Sample {i+1:3d} | "
            f"FL={fl:4d} "
            f"FC={fc:4d} "
            f"FR={fr:4d}"
        )

        time.sleep(0.05)

    print("\n============================")
    print("CALIBRATION RESULTS")
    print("============================\n")

    sensors = {
        "FL": fl_readings,
        "FC": fc_readings,
        "FR": fr_readings
    }

    for name, values in sensors.items():

        print(f"{name}")

        print(
            f"  Mean    : "
            f"{statistics.mean(values):.2f}"
        )

        print(
            f"  Min     : "
            f"{min(values)}"
        )

        print(
            f"  Max     : "
            f"{max(values)}"
        )

        print(
            f"  Std Dev : "
            f"{statistics.stdev(values):.2f}"
        )

        print()

    overall_mean = statistics.mean(
        fl_readings + fc_readings + fr_readings
    )

    print(
        f"Overall Mean = "
        f"{overall_mean:.2f}"
    )

finally:

    GPIO.cleanup()
