try:
    import vrep
except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

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



# speed_start = 10#100
# speed_step = 5
# speed_end = 100
#
# kp_start = 10
# kp_step = 5
# kp_end = 100#15
#
# ki_start = 0
# ki_step = 0.5
# ki_end = 10#0
#
# kd_start = 0
# kd_step = 5
# kd_end = 100#0
#
#
# class TestDataGenerator:
#
#     def __init__(self):
#         self.speed_c = speed_start
#         self.kp_c = kp_start
#         self.ki_c = ki_start
#         self.kd_c = kd_start
#
#
#     def has_next(self):
#         return (self.speed_c <= speed_end and
#                 self.kp_c <= kp_end and
#                 self.ki_c <= ki_end and
#                 self.kd_c <= kd_end)
#
#     def get_test_case(self):
#         speed = self.speed_c
#         kp = self.kp_c
#         ki = self.ki_c
#         kd = self.kd_c
#
#         self.kd_c += kd_step
#
#         if self.kd_c > kd_end:
#             self.kd_c = kd_start
#             self.ki_c += ki_step
#
#         if self.ki_c > ki_end:
#             self.ki_c = ki_start
#             self.kp_c += kp_step
#
#         if self.kp_c > kp_end:
#             self.kp_c = kp_start
#             self.speed_c += speed_step
#
#         return [speed, kp, ki, kd]
