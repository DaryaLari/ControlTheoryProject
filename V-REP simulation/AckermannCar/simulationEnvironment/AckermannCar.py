import numpy as np

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


class AckermannCar:
    steeringBaseAngle = 0
    left_right_wheels_distance = 0.0755 # distance between left and right wheels
    front_back_wheels_distance = 0.1289  # distance between front and back wheels

    def __init__(self, client_id, controller, log_errors=False):
        self.clientID = client_id
        self.controller = controller
        controller.set_driven_car(self)
        self.log_errors = log_errors

        ### get scene, model objects ###
        self.init_front_motors()
        self.init_steering()
        self.init_back_motors()
        self.init_vision_sensors()
        self.init_proximity_sensors()

    def read_single_vision_sensor(self, sensor, mode=vrep.simx_opmode_streaming):
        err_code, state, data = vrep.simxReadVisionSensor(
            self.clientID,
            sensor,
            mode)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error while reading vision sensor")
        return err_code, data

    def set_single_steering_angle(self, steering, angle=0, mode=vrep.simx_opmode_streaming):
        err_code = vrep.simxSetJointTargetPosition(
            self.clientID,
            steering,
            angle,
            mode)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error while setting steering angle")
        return err_code

    def set_single_motor_speed(self, motor, speed=0, mode=vrep.simx_opmode_streaming):
        err_code = vrep.simxSetJointTargetVelocity(
            self.clientID,
            motor,
            speed,
            mode)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error while setting speed to a motor")
        return err_code

    def read_single_proximity_sensor(self, sensor, mode=vrep.simx_opmode_buffer):
        err_code, detection_state, detected_point, detected_object_handle, detected_surface_normal_vector = vrep.simxReadProximitySensor(
            self.clientID,
            sensor,
            mode)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Error while reading proximity sensor")
            return err_code, 0
        return err_code, np.linalg.norm(detected_point)

    def init_front_motors(self):
        err_code, self.left_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find front left motor")
        err_code, self.right_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_motorRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find front right motor")

        self.set_speed(0, vrep.simx_opmode_blocking)

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

        self.set_rotation_angle(0, vrep.simx_opmode_blocking)

    def init_back_motors(self):
        err_code, self.left_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisLeft',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find left sensor")
        err_code, self.right_back_motor = vrep.simxGetObjectHandle(
            self.clientID,
            'nakedCar_freeAxisRight',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right sensor")

        self.set_single_motor_speed(self.left_back_motor, 0, vrep.simx_opmode_blocking)
        self.set_single_motor_speed(self.right_back_motor, 0, vrep.simx_opmode_blocking)

    def init_vision_sensors(self):
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

    def init_proximity_sensors(self):
        err_code, self.left_prox_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'Proximity_sensor_left',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find left proximity sensor")
        err_code, self.right_prox_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'Proximity_sensor_right',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find right proximity sensor")
        err_code, self.middle_prox_sensor = vrep.simxGetObjectHandle(
            self.clientID,
            'Proximity_sensor_middle',
            vrep.simx_opmode_blocking)
        if err_code != vrep.simx_return_ok:
            self.log_errors and print("Can not find middle proximity sensor")

    def read_vision_sensors_intensity(self, mode=vrep.simx_opmode_streaming):
        intensity_l, intensity_r, intensity_m = 1, 1, 1
        err_code, data_right = self.read_single_vision_sensor(self.right_sensor, mode)
        if err_code == vrep.simx_return_ok:
            intensity_r = data_right[0][10]

        err_code, data_left = self.read_single_vision_sensor(self.left_sensor, mode)
        if err_code == vrep.simx_return_ok:
            intensity_l = data_left[0][10]

        err_code, data_middle = self.read_single_vision_sensor(self.middle_sensor, mode)
        if err_code == vrep.simx_return_ok:
            intensity_m = data_middle[0][10]

        return intensity_l, intensity_m, intensity_r

    def read_proximity_sensors(self, mode=vrep.simx_opmode_buffer):
        err_code, distance_r = self.read_single_proximity_sensor(self.right_prox_sensor, mode)
        err_code, distance_l = self.read_single_proximity_sensor(self.left_prox_sensor, mode)
        err_code, distance_m = self.read_single_proximity_sensor(self.middle_prox_sensor, mode)

        return distance_r, distance_m, distance_l

    def set_rotation_angle(self, base_angle=0, mode=vrep.simx_opmode_streaming):
        if base_angle > 1:
            base_angle = 1
        if base_angle < -1:
            base_angle = -1

        tan_correction_angle = math.tan(base_angle)

        steering_angle_right = 0
        steering_angle_left = 0
        if tan_correction_angle != 0:
            steering_angle_left = math.atan(self.front_back_wheels_distance / (-self.left_right_wheels_distance / 2 + self.front_back_wheels_distance / tan_correction_angle))
            steering_angle_right = math.atan(self.front_back_wheels_distance / (self.left_right_wheels_distance / 2 + self.front_back_wheels_distance / tan_correction_angle))

        self.set_single_steering_angle(self.left_steering, steering_angle_left, mode)
        self.set_single_steering_angle(self.right_steering, steering_angle_right, mode)

    def set_speed(self, speed, mode=vrep.simx_opmode_streaming):
        self.set_single_motor_speed(self.left_motor, speed, mode)
        self.set_single_motor_speed(self.right_motor, speed, mode)

    def init_states(self):
        self.log_errors and print("--- Init start ---")
        time.sleep(1) # pause for avoiding errors in initializing objects states
        # perform first test readings
        self.read_vision_sensors_intensity(vrep.simx_opmode_blocking)
        self.read_vision_sensors_intensity()
        self.read_single_proximity_sensor(self.right_prox_sensor, vrep.simx_opmode_streaming)
        self.read_single_proximity_sensor(self.left_prox_sensor, vrep.simx_opmode_streaming)
        self.read_single_proximity_sensor(self.middle_prox_sensor, vrep.simx_opmode_streaming)

        self.set_rotation_angle(0)
        self.set_speed(0, vrep.simx_opmode_blocking)

        self.log_errors and print("--- Init end ---")
