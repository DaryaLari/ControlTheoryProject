class CarController:
    params_borders = [
        [50, 150],
        [-1, 1]
    ]

    def normalize_params(self, params):
        for i in range(0, len(params)):
            params[i] = (params[i] - self.params_borders[i][0]) / (self.params_borders[i][1] - self.params_borders[i][0])
        return params

    def denormalize_params(self, params):
        for i in range(0, len(params)):
            params[i] = self.params_borders[i][0] + params[i] * (self.params_borders[i][1] - self.params_borders[i][0])
        return params

    def __init__(self, net):
        self.net = net
        self.activations_count = 0
        self.avg_speed = 0

    def get_controlled_params(self, sensor_data_l, sensor_data_r):
        [speed, steering] = self.denormalize_params(self.net.activate([sensor_data_l, sensor_data_r]))
        self.avg_speed = (self.avg_speed * self.activations_count + speed) / (self.activations_count + 1)
        self.activations_count += 1
        return [speed, steering]