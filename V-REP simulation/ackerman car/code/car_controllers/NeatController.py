from car_controllers import sensor_type_vision, sensor_type_proximity
from car_controllers.UniversalController import UniversalController


class NeatController(UniversalController):

    def __init__(self, net, sensor_type=sensor_type_vision, cycle_time=0.1, time_limit=-1):
        UniversalController.__init__(self, 50, sensor_type, cycle_time, time_limit)
        self.net = net
        self.activations_count = 0
        self.avg_speed = 0

    params_borders = [
        [50, 100], # speed
        [-1, 1] # steering angle
    ]

    # def normalize_params(self, params):
    #     for i in range(0, len(params)):
    #         params[i] = (params[i] - self.params_borders[i][0]) / (self.params_borders[i][1] - self.params_borders[i][0])
    #     return params

    def denormalize_params(self, params):
        for i in range(0, len(params)):
            params[i] = self.params_borders[i][0] + params[i] * (self.params_borders[i][1] - self.params_borders[i][0])
        return params

    def get_computed_params(self):
        sensors_data = self.get_car_state()
        [speed, steering] = self.denormalize_params(self.net.activate(sensors_data))
        self.avg_speed = (self.avg_speed * self.activations_count + speed) / (self.activations_count + 1)
        self.activations_count += 1
        return [steering, speed]