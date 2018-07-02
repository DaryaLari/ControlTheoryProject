import time

import vrep
from car_controllers import sensor_type_vision, sensor_type_proximity


class UniversalController:

    cycle_time = 0.1
    speed = 0

    def __init__(self, sensor_type=sensor_type_vision, time_limit=-1):
        self.sensor_type = sensor_type
        self.time_limit = time_limit

        self.driven_car = None

    def set_driven_car(self, car):
        self.driven_car = car

    def get_car_state(self):
        state = []
        if self.sensor_type == sensor_type_proximity:
            state = self.driven_car.read_proximity_sensors()
        else:
            state = self.driven_car.read_vision_sensors_intensity()
        return state

    def set_params_to_car(self, correction_angle, speed):
        self.driven_car.set_rotation_angle(correction_angle)
        self.driven_car.set_speed(speed)

    def drive_car(self):
        sim_start_time = time.time()
        sim_in_timeline = True

        while self.is_car_on_line() and sim_in_timeline:
            cycle_start_time = time.time()

            correction_angle, speed = self.get_computed_params()
            self.set_params_to_car(correction_angle, speed)

            # Check if time limit for simulation is not exceeded
            if self.time_limit != -1:
                sim_in_timeline = (time.time() - sim_start_time) < self.time_limit

            time.sleep(self.cycle_time - (time.time() - cycle_start_time))

        return time.time() - sim_start_time

    def get_computed_params(self):
        sensors_data = self.get_car_state()

        if sensors_data[2] > sensors_data[0]:
            correction_angle = 0.2
        if sensors_data[2] < sensors_data[0]:
            correction_angle = -0.2
        if sensors_data[2] == sensors_data[0]:
            correction_angle = 0

        return correction_angle, self.speed

    def is_car_on_line(self): # Check if car still follows the line
        err_code, data_middle = self.driven_car.read_single_vision_sensor(self.driven_car.middle_sensor)
        if err_code == vrep.simx_return_ok:
            return data_middle[0][11] < 0.9
        return True