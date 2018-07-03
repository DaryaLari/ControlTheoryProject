import math

from car_controllers import sensor_type_vision, sensor_type_proximity
from car_controllers.UniversalController import UniversalController


class PidController(UniversalController):

    def __init__(self, kp, ki, kd, speed=50, sensor_type=sensor_type_vision, time_limit=-1):
        UniversalController.__init__(self, sensor_type, time_limit)
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.speed = speed
        self.prev_error = 0
        self.integral = 0

    def get_car_state(self):
        state = []
        if self.sensor_type == sensor_type_proximity:
            state = self.driven_car.read_proximity_sensors()
        else:
            state = self.driven_car.read_vision_sensors_intensity()
        return state

    def get_computed_params(self):
        sensors_data = self.get_car_state()

        self.error = sensors_data[2] - sensors_data[0]
        self.integral = self.integral + self.error
        self.derivative = self.error - self.prev_error
        self.prev_error = self.error

        correction_angle = math.radians(self.Kp * self.error + self.Ki * self.integral + self.Kd * self.derivative)

        return correction_angle, self.speed
