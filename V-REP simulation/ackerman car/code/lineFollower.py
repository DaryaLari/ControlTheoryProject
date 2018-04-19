try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')


import time
import math

steeringBaseAngle = 0
half_pi = math.pi / 2
degToRadConst = math.pi / 180
half_t = 0.0755 / 2  # t = 0.0755 = distance between left and right wheels
l = 0.1289  # l = distance between front and back wheels
cycleTime = 0.5

class lineFollower:

    left_motor = None
    right_motor = None

    def initMotors(self):
        errorCode, self.left_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorLeft',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find left motor")
        errorCode, self.right_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorRight',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find right motor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.left_motor, 0,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error left motor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.right_motor, 0,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error right motor")
                err_code = -1

    def initSteering(self):
        errorCode, self.left_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringLeft',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find left steering")
        errorCode, self.right_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringRight',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find right steering")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetPosition(self.clientID, self.left_steering, 0,
                                                   vrep.simx_opmode_streaming)
            print("Error init left steering")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetPosition(self.clientID, self.right_steering, 0,
                                                   vrep.simx_opmode_streaming)
            print("Error init right steering")

    def initBackMotors(self):
        errorCode, self.left_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisLeft',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find left sensor")
        errorCode, self.right_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisRight',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find right sensor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.left_back_motor, 0,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error left back motor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.right_back_motor, 0,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error right back motor")
                err_code = -1

    def initSensors(self):
        errorCode, self.left_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'leftSensor',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find left sensor")
        errorCode, self.right_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'rightSensor',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find right sensor")


    def __init__(self, clientID, speed, kp, ki, kd):
        self.clientID = clientID
        self.speed = speed
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        ### get scene, model objects ###
        self.initMotors()
        self.initSteering()
        self.initBackMotors()
        self.initSensors()

        # get car
        errorCode, self.car = vrep.simxGetObjectHandle(
            self.clientID,
            'modAckermannSteeringCar',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find car")
        # get path
        errorCode, self.path = vrep.simxGetObjectHandle(
            self.clientID,
            'Path',
            vrep.simx_opmode_oneshot_wait)
        if errorCode != vrep.simx_return_ok:
            print("Can not find path")
        ### - ###


    def runCar(self):
        prevError = 0
        error = 0
        integral = 0
        derivative = 0
        print("Speed: " + str(self.speed)
              + "\nKp: " + str(self.Kp)
              + "\nKi: " + str(self.Ki)
              + "\nKd: " + str(self.Kd))

        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, dataRight = vrep.simxReadVisionSensor(self.clientID, self.right_sensor,
                                                                   vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error init right sensor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, dataLeft = vrep.simxReadVisionSensor(self.clientID, self.left_sensor,
                                                                  vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error init left sensor")

        sensorDataL = 0.5
        sensorDataR = 0.5

        actualSpeed = self.speed
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.left_motor, actualSpeed,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error setting base speed to left motor")
                time.sleep(1)
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.right_motor, actualSpeed,
                                                       vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error setting base speed to right motor")
                time.sleep(1)

        carOnFloor = True
        while carOnFloor:
            cycleStartTime = time.time()

            resultL = -1
            resultR = -1
            while resultR != vrep.simx_return_ok:
                resultR, state, dataRight = vrep.simxReadVisionSensor(self.clientID, self.right_sensor,
                                                        vrep.simx_opmode_streaming)
            while resultL != vrep.simx_return_ok:
                resultL, state, dataLeft = vrep.simxReadVisionSensor(self.clientID, self.left_sensor,
                                                        vrep.simx_opmode_streaming)

            if resultL == vrep.simx_return_ok:
                sensorDataL = dataLeft[0][11]
            if resultR == vrep.simx_return_ok:
                sensorDataR = dataRight[0][11]
            error = sensorDataR - sensorDataL
            print(error)
            integral = integral + error
            derivative = error - prevError
            prevError = error

            correctionAngle = degToRadConst * (self.Kp * error + self.Ki * integral + self.Kd * derivative)

            if (correctionAngle > half_pi) :
                correctionAngle = half_pi
            if (correctionAngle < -half_pi) :
                correctionAngle = -half_pi

            print(correctionAngle)

            tanCorAngle = math.tan(correctionAngle)

            steeringAngleLeft = math.atan(l / (-half_t + l * tanCorAngle))
            steeringAngleRight = math.atan(l / (half_t + l * tanCorAngle))

            print (str(steeringAngleLeft) + " " + str(steeringAngleRight))

            # err_code = vrep.simxSetJointTargetPosition(self.clientID, self.left_steering, steeringAngleLeft,
            #                                            vrep.simx_opmode_streaming)
            # if err_code != vrep.simx_return_ok:
            #     print("Error changing rotation angle at left steering")
            #
            # err_code = vrep.simxSetJointTargetPosition(self.clientID, self.right_steering, steeringAngleRight,
            #                                            vrep.simx_opmode_streaming)
            # if err_code != vrep.simx_return_ok:
            #     print("Error changing rotation angle at right steering")

            # print(time.time() - cycleStartTime)
            # time.sleep(cycleTime - (time.time() - cycleStartTime))

            err_code = -1
            while err_code != vrep.simx_return_ok:
                err_code, position = vrep.simxGetObjectPosition(self.clientID, self.path, self.left_motor, vrep.simx_opmode_blocking)
            print(position)
            if position[0] > 0.2:
                carOnFloor = False