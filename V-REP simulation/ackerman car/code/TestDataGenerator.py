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

speed_start = 10#100
speed_step = 5
speed_end = 100

kp_start = 10
kp_step = 5
kp_end = 100#15

ki_start = 0
ki_step = 0.5
ki_end = 10#0

kd_start = 0
kd_step = 5
kd_end = 100#0


class TestDataGenerator:

    def __init__(self):
        self.speed_c = speed_start
        self.kp_c = kp_start
        self.ki_c = ki_start
        self.kd_c = kd_start


    def has_next(self):
        return (self.speed_c <= speed_end and
                self.kp_c <= kp_end and
                self.ki_c <= ki_end and
                self.kd_c <= kd_end)

    def get_test_case(self):
        speed = self.speed_c
        kp = self.kp_c
        ki = self.ki_c
        kd = self.kd_c

        self.kd_c += kd_step

        if self.kd_c > kd_end:
            self.kd_c = kd_start
            self.ki_c += ki_step

        if self.ki_c > ki_end:
            self.ki_c = ki_start
            self.kp_c += kp_step

        if self.kp_c > kp_end:
            self.kp_c = kp_start
            self.speed_c += speed_step

        return [speed, kp, ki, kd]

    # try:
    #     import vrep
    # except:
    #     print('--------------------------------------------------------------')
    #     print('"vrep.py" could not be imported. This means very probably that')
    #     print('either "vrep.py" or the remoteApi library could not be found.')
    #     print('Make sure both are in the same folder as this file,')
    #     print('or appropriately adjust the file "vrep.py"')
    #     print('--------------------------------------------------------------')
    #     print('')
    #
    # import time
    # import math
    #
    #
    # class TestDataGenerator:
    #
    #     def __init__(self):
    #         self.current_values = []
    #         for i in borders:
    #             self.current_values[i] = borders[i][0]
    #
    #     def has_next(self):
    #         res = True
    #         for i in borders:
    #             res = res and (self.current_values[i] <= borders[i][1])
    #
    #     def get_test_case(self):
    #         return_vals = []
    #         for i in borders:
    #             return_vals[i] = self.current_values[i]
    #
    #         params_am = len(return_vals)
    #         self.current_values[params_am - 1] += borders[params_am - 1][2]
    #
    #         for i in range(params_am - 1, 1, -1):
    #             if self.current_values[i] > borders[i][1]:
    #                 self.current_values[i] = borders[i][0]
    #                 self.current_values[i - 1] += borders[i - 1][2]
    #
    #         return return_vals