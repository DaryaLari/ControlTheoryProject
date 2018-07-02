from car_controllers import sensor_type_vision, sensor_type_proximity
from car_controllers.UniversalController import UniversalController


class NeatController(UniversalController):

    params_borders = [
        [50, 100], # speed
        [-1, 1] # steering angle
    ]

    def __init__(self, net, sensor_type=sensor_type_vision, time_limit=-1):
        UniversalController.__init__(self, sensor_type, time_limit)
        self.net = net
        self.activations_count = 0
        self.avg_speed = 0
        self.states = []

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

    def denormalize_params(self, params):
        for i in range(0, len(params)):
            params[i] = self.params_borders[i][0] + params[i] * (self.params_borders[i][1] - self.params_borders[i][0])
        return params

    def get_computed_params(self):
        sensors_data = self.get_car_state()
        [speed, steering] = self.denormalize_params(self.net.activate(sensors_data))
        self.states.append([self.cycle_time, speed, steering, *sensors_data])
        self.avg_speed = (self.avg_speed * self.activations_count + speed) / (self.activations_count + 1)
        self.activations_count += 1
        return [steering, speed]
