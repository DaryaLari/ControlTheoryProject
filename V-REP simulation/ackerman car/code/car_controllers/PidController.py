import math

from car_controllers import sensor_type_vision, sensor_type_proximity
from car_controllers.UniversalController import UniversalController


class PidController(UniversalController):

    def __init__(self, kp, ki, kd, base_speed=50, sensor_type=sensor_type_vision, cycle_time=0.1, time_limit=-1):
        UniversalController.__init__(self, base_speed, sensor_type, cycle_time, time_limit)
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.prev_error = 0
        self.integral = 0

    def get_computed_params(self):
        sensors_data = self.get_car_state()

        self.error = sensors_data[2] - sensors_data[0]
        self.integral = self.integral + self.error
        self.derivative = self.error - self.prev_error
        self.prev_error = self.error

        correction_angle = math.radians(self.Kp * self.error + self.Ki * self.integral + self.Kd * self.derivative)

        return [correction_angle, self.speed]
