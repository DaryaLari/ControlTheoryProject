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

import time
from simulationEnvironment import AckermannCar

clientId = -1
remote_api_port = 19997


def init_connection_scene(path):
    global clientId
    print('Program started')
    # Connect to remote API server
    vrep.simxFinish(-1) # just in case, close all opened connections
    clientId = vrep.simxStart('127.0.0.1', remote_api_port, True, True, 5000, 5)
    if clientId == -1:
        print('Failed connecting to remote API server')
        return -1
    print('Connected to remote API server')
    # Load scene
    err_code = vrep.simxLoadScene(clientId, path, 0xFF, vrep.simx_opmode_blocking)
    if err_code != vrep.simx_return_ok:
        print('Failed loading scene')
        vrep.simxFinish(clientId)
        return -1

    return clientId


def close_connection_scene():
    # Close scene
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxCloseScene(clientId, vrep.simx_opmode_blocking)
        time.sleep(1)
    # Disconnect from remote API server
    vrep.simxFinish(clientId)
    print('Closed connection')


def run_test(controller, log_errors=False):
    # Init & start simulation
    lf = AckermannCar.AckermannCar(clientId, controller, log_errors=log_errors)
    vrep.simxStartSimulation(clientId, vrep.simx_opmode_oneshot)

    # Run simulation
    lf.init_states()
    sim_time = controller.drive_car()
    # Stop simulation
    err_code = -1
    while err_code != vrep.simx_return_ok:
        err_code = vrep.simxStopSimulation(clientId, vrep.simx_opmode_oneshot)
        time.sleep(1)

    return sim_time