"""
Nick Waggoner
4-15-22
Robot class for robot control. Primarily build for differential drive Pioneer P3DX robot
"""

import sim as vrep

class Robot:
    def __init__(self, sim, handle, id):
        self.clientID = sim # The simulation's clientID
        self.handle = handle # The robot's simulation handle
        self.ID = id # The robot's number in the swarm. More for user use
        self.path # The individual path of the robot. This is a string
        self.leftMotor = self.setupLeftMotor()
        self.rightMotor = self.setupRightMotor()
        self.sensors = []
        self.setupSensors(self.sensors, self.clientID)

    def setupLeftMotor(self):
        err_code, l_motor_handle = vrep.simxGetObjectHandle(self.clientID, "Pioneer_p3dx_leftMotor",
                                                            vrep.simx_opmode_blocking)
        if err_code != 0:
            print("ERR: could not get left motor")
        return l_motor_handle

    def setupRightMotor(self):
        err_code, r_motor_handle = vrep.simxGetObjectHandle(self.clientID, "Pioneer_p3dx_rightMotor",
                                                            vrep.simx_opmode_blocking)
        if err_code != 0:
            print("ERR: could not get right motor")
        return r_motor_handle

    def setupSensors(self):
        for x in range(0, 16):
            err_code, ps = vrep.simxGetObjectHandle(self.clientID, "Pioneer_p3dx_ultrasonicSensor{0}".format(x + 1),
                                                    vrep.simx_opmode_blocking)
            if err_code != 0:
                print("ERR: could not set up ultrasonic sensor {0}".format(x + 1))
            self.sensors.append(ps)

    def rotate(self, leftVel, rightVel, angle):
        """Runs both motors in opposite directions to pivot the bot in place"""
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.leftMotor, (-1) * leftVel / 2, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set leftmotor velocity")
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.rightMotor, rightVel / 2, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set rightmotor velocity")

    def forward(self):
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.leftMotor, 1, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set leftmotor velocity")
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.rightMotor, 1, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set rightmotor velocity")

    def stop(self):
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.leftMotor, 0, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set leftmotor velocity")
        if (vrep.simxSetJointTargetVelocity(self.clientID, self.rightMotor, 0, vrep.simx_opmode_streaming)) != 0:
            print("ERR: cannot set rightmotor velocity")


