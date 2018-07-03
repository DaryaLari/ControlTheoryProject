class TestDataGenerator:

    def __init__(self, params_borders):
        self.borders = params_borders
        self.current_values = []
        self.params_amount = len(self.borders)
        for i in range(0, self.params_amount):
            self.current_values.append(self.borders[i][0])

    def has_next(self):
        res = True
        for i in range(0, self.params_amount):
            res = res and (self.current_values[i] <= self.borders[i][1])
        return res

    def get_test_case(self):
        return_vals = []
        for i in range(0, self.params_amount):
            return_vals.append(self.current_values[i])

        params_am = len(return_vals)
        self.current_values[params_am - 1] += self.borders[params_am - 1][2]

        for i in range(params_am - 1, 0, -1):
            if self.current_values[i] > self.borders[i][1]:
                self.current_values[i] = self.borders[i][0]
                self.current_values[i - 1] += self.borders[i - 1][2]

        return return_vals