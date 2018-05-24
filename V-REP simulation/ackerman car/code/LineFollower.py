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
            self.log_errors and print("Can not find left motor")
        err_code, self.right_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right motor")
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.left_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init left motor")
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.right_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init right motor")

    def init_steering(self):
        err_code, self.left_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find left steering")
        err_code, self.right_steering = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_steeringRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right steering")

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.left_steering,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init left steering")

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.right_steering,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init right steering")

    def init_back_motors(self):
        err_code, self.left_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find left sensor")
            time.sleep(0.5)
        err_code, self.right_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right sensor")

        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.left_back_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init left back motor")

        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.right_back_motor,
            0,
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error init right back motor")

    def init_sensors(self):
        err_code, self.left_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'leftSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find left sensor")
        err_code, self.right_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'rightSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right sensor")
        err_code, self.middle_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'middleSensor',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find middle sensor")

    def __init__(self, client_id, params=[0, 0, 0, 0], log_errors=False, time_limit=-1):
        self.clientID = client_id
        self.speed = params[0]
        self.Kp = params[1]
        self.Ki = params[2]
        self.Kd = params[3]
        self.log_errors = log_errors
        self.time_limit = time_limit

        ### get scene, model objects ###
        self.init_motors()
        self.init_steering()
        self.init_back_motors()
        self.init_sensors()

    def read_vision_sensors(self, last_left, last_right):
        s_data_left, s_data_right = last_left, last_right
        result_r, state, data_right = vrep.simxReadVisionSensor(
            self.clientID,
            self.right_sensor,
            vrep.simx_opmode_streaming)
        if result_r != vrep.simx_return_ok:
            self.log_errors and print("Old data of right vision sensor are used")

        result_l, state, data_left = vrep.simxReadVisionSensor(
            self.clientID,
            self.left_sensor,
            vrep.simx_opmode_streaming)
        if result_l != vrep.simx_return_ok:
            self.log_errors and print("Old data of left vision sensor are used")

        if result_l == vrep.simx_return_ok:
            s_data_left = data_left[0][10]
        if result_r == vrep.simx_return_ok:
            s_data_right = data_right[0][10]

        return s_data_left, s_data_right

    def set_rotation_angle(self, base_angle):
        if base_angle > half_pi:
            base_angle = half_pi
        if base_angle < -half_pi:
            base_angle = -half_pi

        tan_correction_angle = math.tan(base_angle)

        steering_angle_right = 0
        steering_angle_left = 0
        if tan_correction_angle != 0:
            steering_angle_left = math.atan(l / (-half_t + l / tan_correction_angle))
            steering_angle_right = math.atan(l / (half_t + l / tan_correction_angle))

        # print("Angle: "),
        # print("\tleft=" + str(steering_angle_left)),
        # print("\tbase=" + str(base_angle)),
        # print("\tright=" + str(steering_angle_right)),

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.left_steering,
            steering_angle_left,
            vrep.simx_opmode_streaming)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error changing rotation angle at left steering")

        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            self.right_steering,
            steering_angle_right,
            vrep.simx_opmode_streaming)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error changing rotation angle at right steering")

    def set_speed(self, speed):
        # print("Speed: " + str(speed))
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.left_motor,
            speed,
            vrep.simx_opmode_streaming)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error setting base speed to left motor")

        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            self.right_motor,
            speed,
            vrep.simx_opmode_streaming)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error setting base speed to right motor")

    def set_initial_values(self):
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_middle = vrep.simxReadVisionSensor(
            self.clientID,
            self.left_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                self.log_errors and print("Error init middle sensor")
                time.sleep(1)
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_right = vrep.simxReadVisionSensor(
            self.clientID,
            self.right_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                self.log_errors and print("Error init right sensor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code, state, data_left = vrep.simxReadVisionSensor(
            self.clientID,
            self.left_sensor,
            vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                self.log_errors and print("Error init left sensor")

        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(
                self.clientID,
                self.left_motor,
                self.speed,
                vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                self.log_errors and print("Error setting base speed to left motor")
        err_code = -1
        while err_code != vrep.simx_return_ok:
            err_code = vrep.simxSetJointTargetVelocity(
                self.clientID,
                self.right_motor,
                self.speed,
                vrep.simx_opmode_blocking)
            if err_code != vrep.simx_return_ok:
                self.log_errors and print("Error setting base speed to right motor")

    def run_car(self):
        prev_error = 0
        error = 0
        integral = 0
        derivative = 0

        sensor_data_l = 0.5
        sensor_data_r = 0.5

        self.set_initial_values()

        sim_start_time = time.time()
        sim_in_timeline = True

        car_on_line = True
        while car_on_line and sim_in_timeline:
            cycle_start_time = time.time()

            sensor_data_l, sensor_data_r = self.read_vision_sensors(last_left=sensor_data_l, last_right=sensor_data_r)

            error = sensor_data_r - sensor_data_l
            integral = integral + error
            derivative = error - prev_error
            prev_error = error

            correction_angle = degToRadConst * (self.Kp * error + self.Ki * integral + self.Kd * derivative)

            self.set_rotation_angle(correction_angle)

            # Check if car still follows the line
            err_code, state, data_middle = vrep.simxReadVisionSensor(
                self.clientID,
                self.left_sensor,
                vrep.simx_opmode_streaming)
            if err_code == vrep.simx_return_ok:
                car_on_line = (data_middle[0][11] < 0.9)

            # Check if time limit for simulation is not exceeded
            if self.time_limit != -1:
                sim_in_timeline = (time.time() - sim_start_time) < self.time_limit

            time.sleep(cycleTime - (time.time() - cycle_start_time))

        return time.time() - sim_start_time

    def run_controlled_car(self, controller):

        sensor_data_l = 0.5
        sensor_data_r = 0.5

        self.set_initial_values()

        sim_start_time = time.time()
        sim_in_timeline = True

        car_on_line = True
        while car_on_line and sim_in_timeline:
            cycle_start_time = time.time()

            sensor_data_l, sensor_data_r = self.read_vision_sensors(last_left=sensor_data_l, last_right=sensor_data_r)

            [speed, correction_angle] = controller.get_controlled_params(sensor_data_l, sensor_data_r)

            self.set_rotation_angle(correction_angle)
            self.set_speed(speed)

            # Check if car still follows the line
            err_code, state, data_middle = vrep.simxReadVisionSensor(
                self.clientID,
                self.left_sensor,
                vrep.simx_opmode_streaming)
            if err_code == vrep.simx_return_ok:
                car_on_line = (data_middle[0][11] < 0.9)

            # Check if time limit for simulation is not exceeded
            if self.time_limit != -1:
                sim_in_timeline = (time.time() - sim_start_time) < self.time_limit

            time.sleep(cycleTime - (time.time() - cycle_start_time))

        return time.time() - sim_start_time
