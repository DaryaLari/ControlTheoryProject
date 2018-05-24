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
import LineFollower


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
    vrep.simxFinish(client_id)
    print('Program ended')
    ###-###


def run_test(client_id, speed, kp, ki, kd, log_errors=False, time_limit=-1):
    print("\n-------------------------"
          + "\n| Speed: " + str(speed)
          + "\n| Kp: " + str(kp)
          + "\n| Ki: " + str(ki)
          + "\n| Kd: " + str(kd)
          + "\n---")
    ### Init & start simulation ###
    lf = LineFollower.LineFollower(client_id, [speed, kp, ki, kd], log_errors=log_errors, time_limit=time_limit)
    vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot)
    ###-###

    ### Run simulation ###
    sim_time = lf.run_car()
    ###-###

    ### Stop simulation ###
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot)
        time.sleep(1)
    ###-###

    print("---"
          + "\n| Sim. time: " + str(sim_time)
          + "\n-------------------------")

    return sim_time


def run_controlled_test(client_id, controller, log_errors=False, time_limit=-1):
    ### Init & start simulation ###
    lf = LineFollower.LineFollower(client_id, [0, 0, 0, 0], log_errors=log_errors, time_limit=time_limit)
    vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot)
    ###-###

    ### Run simulation ###
    sim_time = lf.run_controlled_car(controller)
    ###-###

    ### Stop simulation ###
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot)
        time.sleep(1)
    ###-###
    return sim_time
