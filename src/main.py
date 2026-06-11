from robot import SumoRobot

robot = SumoRobot()

try:

    robot.run()

except KeyboardInterrupt:

    robot.cleanup()
