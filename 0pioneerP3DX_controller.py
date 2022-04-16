"""
@author PJ Olender
Date Created: 3-02-2022
Python Version 3.9
0pioneerP3DX_controller.py
"""

import math, logging, time

PIONEER_ROBOT = '/PioneerP3DX'
PIONEER_LEFT_MOTOR = '/leftMotor'
PIONEER_RIGHT_MOTOR = '/rightMotor'

FLOOR = '/Floor'

def connectionMessage(message):
    logging.warning(f'[Connection]:{message}')

def mapEntityOrientationFromRadiansToDegrees(orientationObj):
    newOrientationList = []
    for i in range(len(orientationObj)):
        # Convert radians to degrees
        if orientationObj[i] < 0:
            result = math.degrees(orientationObj[i]) % -360
        else:
            result = math.degrees(orientationObj[i]) % 360

        # Adjust the result by 10000 if the string of the value contains an E
        # This might have to be adjusted later
        if "e" in str(orientationObj[i]):
            result = result * 100000
        newOrientationList.append(result)
    return newOrientationList

class UltraSonicSensorReading:

    def __init__(self, sensorReading):
        if sensorReading != 0:
            self.result, self.distance, self.detectedPoint, self.detectedObjectHandle, self.detectedSurfaceNormalVector = sensorReading
        else:
            self.result = None
            self.distance = None
            self.detectedPoint = None
            self.detectedObjectHandle = None
            self.detectedSurfaceNormalVector = None

    def __str__(self):
        return f"Result: {self.result}, " \
               f"Distance: {self.distance}, " \
               f"DetectedPoint: {self.detectedPoint}, " \
               f"DetectedObjectHandle: {self.detectedObjectHandle}, " \
               f"DetectedSurfaceNormalVector: {self.detectedSurfaceNormalVector}"


''' This class is mostly set up for a pioneer robot, but could be configured for others as well'''

class Robot:

    def __init__(self, sim, robotPath=PIONEER_ROBOT):
        self.sim = sim
        self.robotPath = robotPath
        self.entityHandle = self.sim.getObject(PIONEER_ROBOT)
        self.floorHandle = self.sim.getObject(FLOOR)

    def setLeftMotorVelocity(self, velocity):
        leftMotor = self.sim.getObject(PIONEER_LEFT_MOTOR)
        self.sim.setJointTargetVelocity(leftMotor, velocity)

    def setRightMotorVelocity(self, velocity):
        rightMotor = self.sim.getObject(PIONEER_RIGHT_MOTOR)
        self.sim.setJointTargetVelocity(rightMotor, velocity)

    def setBothMotorsToSameVelocity(self, velocity):
        self.setLeftMotorVelocity(velocity)
        self.setRightMotorVelocity(velocity)

    def readUltrasonicSensor(self, sensorNumber):
        sensorNumber = self.__generateUltrasonicSensorPath(sensorNumber)
        sensorHandle = self.sim.getObject(sensorNumber)
        sensorReading = UltraSonicSensorReading(self.sim.readProximitySensor(sensorHandle))
        return sensorReading

    # Pivots the robot 90 degrees
    #def pivotLeft90Degrees(self, velocity=.4, targetAngle=90):
    #    self.setLeftMotorVelocity(velocity)
    #
    #    currentEntityAngleDegrees = mapEntityOrientationFromRadiansToDegrees(self.getEntityAngle())
    #
    #    print("Current:", currentEntityAngleDegrees[2])
    #    targetValues = [abs(math.ceil(currentEntityAngleDegrees[2] + targetAngle)),
    #                    abs(math.ceil(currentEntityAngleDegrees[2] - targetAngle))]
    #
    #    print("Targets:", targetValues)
    #
    #    while True:
    #        currentEntityAngleDegrees = mapEntityOrientationFromRadiansToDegrees(self.getEntityAngle())
    #        print(math.ceil(currentEntityAngleDegrees[2] % 180), targetValues)
    #        if math.ceil(currentEntityAngleDegrees[2]) % 180 in targetValues:
    #            print("Reached Pos")
    #            self.setBothMotorsToSameVelocity(0)
    #            break

    # pivot the motor, note that with higher velocities, accuracy may decrease
    def pivot(self, targetAngle, motor, velocity=.5, ):
        if velocity > 1:
            velocity = 1

        # Left pivot
        if motor == 1:
            self.setRightMotorVelocity(velocity)

        # Right Pivot
        elif motor == 2:
            self.setLeftMotorVelocity(velocity)

        # Right-Dual wheel pivot
        elif motor == 3:
            self.setLeftMotorVelocity(velocity)
            self.setRightMotorVelocity(-1 * velocity)

        # Left-Dual wheel pivot
        elif motor == 4:
            self.setLeftMotorVelocity(-1 * velocity)
            self.setRightMotorVelocity(velocity)

        # self.setLeftMotorVelocity(velocity)

        currentEntityAngleDegrees = mapEntityOrientationFromRadiansToDegrees(self.getEntityAngle())
        self.logMessageToSim(f"Current:{currentEntityAngleDegrees[2]}")
        targetValues = [abs(math.ceil(currentEntityAngleDegrees[2] + targetAngle)) % 180,
                        abs(math.ceil(currentEntityAngleDegrees[2] - targetAngle)) % 180]

        print("Targets:", targetValues)

        while True:
            currentEntityAngleDegrees = mapEntityOrientationFromRadiansToDegrees(self.getEntityAngle())
            print(math.ceil(currentEntityAngleDegrees[2] % 180), targetValues)
            self.logMessageToSim(f" Current Angle{(math.ceil(currentEntityAngleDegrees[2] % 180))}, Targets: {targetValues}")
            if math.ceil(currentEntityAngleDegrees[2]) % 180 in targetValues:
                self.logMessageToSim(f"Entity {self.entityHandle} has arrived at it's desired position")
                self.setBothMotorsToSameVelocity(0)
                break

    # roll = x, pitch = y, yaw = z
    def setEntityAngle(self, roll, pitch, yaw):
        self.sim.setObjectOrientation(self.entityHandle, self.floorHandle, [roll, pitch, yaw])

    def getEntityAngle(self):
        orientation = self.sim.getObjectOrientation(self.entityHandle, self.floorHandle)
        return orientation

    # Incomplete
    def getCenterOfTwoObjectsWithFrontSensor(self):
        leftReading = self.readUltrasonicSensor(3)
        rightReading = self.readUltrasonicSensor(4)

        # An object exists within the front of the robot
        if leftReading.distance is not None and rightReading.distance is not None:
            distanceFromCenterOfRobot = (leftReading.distance + rightReading.distance) / 2
            print(f"Center Distance:{distanceFromCenterOfRobot} meters")
            return distanceFromCenterOfRobot
        else:
            # nothing exists within 1 meter in front of the robot
            return 0

    def safeToMoveForward(self):
        nearestObject = self.getCenterOfTwoObjectsWithFrontSensor()
        self.logMessageToSim(f"Nearest Object: {nearestObject}m")

        if nearestObject == 0 or nearestObject > 0.3:
            return True
        else:
            return False

    # Not sure what to use this for
    def checkFrontDistance(self):
        leftSensorReading = self.readUltrasonicSensor(3)
        rightSensorReading = self.readUltrasonicSensor(4)

        print(leftSensorReading)
        print(rightSensorReading)

        distance = self.sim.checkDistance(self.entityHandle, leftSensorReading.detectedObjectHandle, 0)
        print("Dist", distance)

    def stop(self):
        self.setBothMotorsToSameVelocity(0)
        self.logMessageToSim("Command sent to Stop")


    def logErrorToSim(self, message):
        self.sim.addLog(self.sim.verbosity_errors, message)

    def logMessageToSim(self, message):
        self.sim.addLog(self.sim.verbosity_default, message)

    @staticmethod
    def __generateUltrasonicSensorPath(sensorNumber):
        return f'/ultrasonicSensor[{sensorNumber}]'
