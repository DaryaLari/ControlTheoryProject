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


def run_test(client_id, speed, kp, ki, kd):
    lf = LineFollower.LineFollower(client_id, speed, kp, ki, kd)
    err_code = vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot)
    if err_code != vrep.simx_return_ok:
        print("Error starting simulation")
        return

    lf.runCar()

    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot)
        time.sleep(1)


def init():
    path = "..\\ackerman_car.ttt"
    print('Program started')
    vrep.simxFinish(-1) # just in case, close all opened connections
    client_id = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    if client_id == -1:
        print('Failed connecting to remote API server')
        exit(-1)
    print('Connected to remote API server')

    err_code = vrep.simxLoadScene(client_id, path, 0xFF, vrep.simx_opmode_blocking)
    if err_code != vrep.simx_return_ok:
        print("Failed loading scene")
        exit(-2)

    s = 0
    while s < 5:
        run_test(client_id, speed=100, kp=10, ki=0, kd=0)
        s += 1

    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxCloseScene(client_id, vrep.simx_opmode_blocking)
        time.sleep(1)
    # Now close the connection to V-REP:
    vrep.simxFinish(client_id)
    print('Program ended')


init()
