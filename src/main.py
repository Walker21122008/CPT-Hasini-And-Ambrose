from robot import SumoRobot

robot = SumoRobot()

try:
    robot.run()

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    robot.cleanup()
