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
import csv
import LineFollower
import TestDataGenerator


def export_data(params):
    with open("results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(params)


def init_connection_scene(path):
    print('Program started')
    ### Connect to remote API server ###
    vrep.simxFinish(-1) # just in case, close all opened connections
    client_id = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    if client_id == -1:
        print('Failed connecting to remote API server')
        exit(-1)
    print('Connected to remote API server')
    ###-###
    ### Load scene ###
    err_code = vrep.simxLoadScene(client_id, path, 0xFF, vrep.simx_opmode_blocking)
    if err_code != vrep.simx_return_ok:
        print("Failed loading scene")
        exit(-2)
    ###-###
    return client_id


def close_connection_scene(client_id):
    ### Close scene ###
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxCloseScene(client_id, vrep.simx_opmode_blocking)
        time.sleep(1)
    ###-###
    ### Disconnect from remote API server ###
    # Now close the connection to V-REP:
    vrep.simxFinish(client_id)
    print('Program ended')
    ###-###


def run_test(client_id, speed, kp, ki, kd):
    ### Init & start simulation ###
    lf = LineFollower.LineFollower(client_id, speed, kp, ki, kd)
    err_code = vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot)
    # if err_code != vrep.simx_return_ok:
    #     print("Error starting simulation")
        # return
    ###-###

    ### Run simulation ###
    start_time = time.time()
    lf.runCar()
    sim_time = time.time() - start_time
    ###-###
    export_data([[speed, kp, ki, kd, sim_time]])

    ### Stop simulation ###
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot)
        time.sleep(1)
    ###-###
    return sim_time


def run_test_engine(client_id):
    # params = [] # [0] - speed, [1] - kp, [2] - ki, [3] - kd, [4] - sim_time
    test_gen = TestDataGenerator.TestDataGenerator(
        [ # [start_value, end_value, step_size]
            [10, 100, 5], # speed
            [10, 100, 5], # kp
            [0, 5, 0.5], # ki
            [0, 25, 5] # kd
        ])
    while test_gen.has_next():
        [t_speed, t_kp, t_ki, t_kd] = test_gen.get_test_case()
        t_time = run_test(client_id, t_speed, t_kp, t_ki, t_kd)
        # params.append([t_speed, t_kp, t_ki, t_kd, t_time])


def run_simple_test(client_id):
    run_test(client_id, speed=100, kp=10, ki=0.1, kd=1)


def run_program():
    client_id = init_connection_scene(path="..\\ackerman_car.ttt") # path to scene

    # export_data([["speed", "kp", "ki", "kd", "time"]])
    # run_simple_test(client_id)
    run_test_engine(client_id)

    close_connection_scene(client_id)

### Starting point ###
run_program()
###-###
