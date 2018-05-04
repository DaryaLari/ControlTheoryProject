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
cycleTime = 0.1


class LineFollower:

    def init_motors(self):
        err_code, self.left_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find left motor")
        err_code, self.right_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find right motor")
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.left_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init left motor")
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.right_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init right motor")

    def init_steering(self):
        err_code, self.left_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find left steering")
        err_code, self.right_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find right steering")

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.left_steering,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init left steering")

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.right_steering,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init right steering")

    def init_back_motors(self):
        err_code, self.left_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find left sensor")
            time.sleep(0.5)
        err_code, self.right_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find right sensor")

        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.left_back_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init left back motor")

        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.right_back_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Error init right back motor")

    def init_sensors(self):
        err_code, self.left_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'leftSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find left sensor")
        err_code, self.right_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'rightSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find right sensor")
        err_code, self.middle_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'middleSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            print("Can not find middle sensor")

    def __init__(self, client_id, speed, kp, ki, kd):
        self.clientID = client_id
        self.speed = speed
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        ### get scene, model objects ###
        self.init_motors()
        self.init_steering()
        self.init_back_motors()
        self.init_sensors()

        # # get car
        # err_code, self.car = vrep.simxGetObjectHandle(
        #     self.clientID,
        #     'modAckermannSteeringCar',
        #     vrep.simx_opmode_oneshot_wait)
        # if err_code != vrep.simx_return_ok:
        #     print("Can not find car")
        # # get path
        # err_code, self.path = vrep.simxGetObjectHandle(
        #     self.clientID,
        #     'Path',
        #     vrep.simx_opmode_oneshot_wait)
        # if err_code != vrep.simx_return_ok:
        #     print("Can not find path")
        # ### - ###


    def runCar(self):
        prev_error = 0
        error = 0
        integral = 0
        derivative = 0
        print("Speed: " + str(self.speed)
              + "\nKp: " + str(self.Kp)
              + "\nKi: " + str(self.Ki)
              + "\nKd: " + str(self.Kd))

        sensor_data_l = 0.5
        sensor_data_r = 0.5
        sensor_data_m = 0.0

        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_middle = vrep.simxReadVisionSensor(
            self.clientID,
            self.left_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                print("Error init middle sensor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_right = vrep.simxReadVisionSensor(
            self.clientID,
            self.right_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                print("Error init right sensor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_left = vrep.simxReadVisionSensor(
            self.clientID,
            self.left_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                print("Error init left sensor")

        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(
                self.clientID,
                self.left_motor,
                self.speed,
                vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                print("Error setting base speed to left motor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(
                self.clientID,
                self.right_motor,
                self.speed,
                vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                print("Error setting base speed to right motor")

        car_on_line = True
        while car_on_line:
            cycle_start_time = time.time()

            result_r, state, data_right = vrep.simxReadVisionSensor(
                self.clientID,
                self.right_sensor,
                vrep.simx_opmode_streaming)
            if result_r != vrep.simx_return_ok:
                print("Old data of right vision sensor are used")

            result_l, state, data_left = vrep.simxReadVisionSensor(
                self.clientID,
                self.left_sensor,
                vrep.simx_opmode_streaming)
            if result_l != vrep.simx_return_ok:
                print("Old data of left vision sensor are used")

            if result_l == vrep.simx_return_ok:
                sensor_data_l = data_left[0][10]
            if result_r == vrep.simx_return_ok:
                sensor_data_r = data_right[0][10]
            error = sensor_data_r - sensor_data_l
            integral = integral + error
            derivative = error - prev_error
            prev_error = error

            correction_angle = degToRadConst * (self.Kp * error + self.Ki * integral + self.Kd * derivative)

            if correction_angle > half_pi:
                correction_angle = half_pi
            if correction_angle < -half_pi:
                correction_angle = -half_pi

            tan_correction_angle = math.tan(correction_angle)

            steering_angle_right = 0
            steering_angle_left = 0
            if tan_correction_angle != 0:
                steering_angle_left = math.atan(l / (-half_t + l / tan_correction_angle))
                steering_angle_right = math.atan(l / (half_t + l / tan_correction_angle))

            err_code = vrep.simxSetJointTargetPosition(
                self.clientID,
                self.left_steering,
                steering_angle_left,
                vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error changing rotation angle at left steering")

            err_code = vrep.simxSetJointTargetPosition(
                self.clientID,
                self.right_steering,
                steering_angle_right,
                vrep.simx_opmode_streaming)
            if err_code != vrep.simx_return_ok:
                print("Error changing rotation angle at right steering")

            # print(time.time() - cycle_start_time)
            time.sleep(cycleTime - (time.time() - cycle_start_time))

            err_code, state, data_middle = vrep.simxReadVisionSensor(
                self.clientID,
                self.left_sensor,
                vrep.simx_opmode_streaming)

            if err_code == vrep.simx_return_ok:
                # sensor_data_l = data_middle[0][12]
                # _0.append(data_middle[0][0])
                # _1.append(data_middle[0][1])
                # _2.append(data_middle[0][2])
                # _3.append(data_middle[0][3])
                # _4.append(data_middle[0][4])
                # _5.append(data_middle[0][5])
                # _6.append(data_middle[0][6])
                # _7.append(data_middle[0][7])
                # _8.append(data_middle[0][8])
                # _9.append(data_middle[0][9])
                # _10.append(data_middle[0][10])
                # _11.append(data_middle[0][11])
                # _12.append(data_middle[0][12])
                # _13.append(data_middle[0][13])
                # _14.append(data_middle[0][14])
                # _t.append(_t[-1] + cycleTime)
                #
                # plt.plot(_t, _0, color=(0, 0, 0))
                # plt.plot(_t, _1, color=(0, 0, 0.5))
                # plt.plot(_t, _2, color=(0, 0, 1))
                # plt.plot(_t, _3, color=(0, 0.5, 0))
                # plt.plot(_t, _4, color=(0, 0.5, 0.5))
                # plt.plot(_t, _5, color=(0, 0.5, 1))
                # plt.plot(_t, _6, color=(0, 1, 0))
                # plt.plot(_t, _7, color=(0, 1, 0.5))
                # plt.plot(_t, _8, color=(0, 1, 1))
                # plt.plot(_t, _12, color=(1, 0, 0))
                # plt.plot(_t, _13, color=(1, 0, 0.5))
                # plt.plot(_t, _14, color=(1, 0, 1))
                # plt.plot(_t, _9, color=(1, 0.5, 0))
                # plt.plot(_t, _10, color=(1, 0.5, 0.5))
                # plt.plot(_t, _11, color=(1, 0.5, 1))

                # plt.figure(1).draw()
                print(data_middle[0][11])
                car_on_line = (data_middle[0][11] < 0.9)