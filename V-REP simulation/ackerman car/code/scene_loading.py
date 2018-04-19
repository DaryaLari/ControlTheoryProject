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
import lineFollower

def runTest(speed, kp, ki, kd):
    lf = lineFollower.lineFollower(clientID, speed, kp, ki, kd)
    res = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

    lf.runCar()

    while res != vrep.simx_return_ok:
        res = vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
        time.sleep(1)
    res = -1

path = "..\\ackerman_car.ttt"
print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)

if clientID==-1:
    print('Failed connecting to remote API server')
    exit(-1)
print ('Connected to remote API server')

res = vrep.simxLoadScene(clientID, path, 0xFF, vrep.simx_opmode_blocking)
if res != vrep.simx_return_ok:
    print("Failed loading scene")
    exit(-2)

s = 0
while s < 10:
    runTest(100, 30, 0, 0)
    s += 1

while res != vrep.simx_return_ok:
    res = vrep.simxCloseScene(clientID, vrep.simx_opmode_blocking)
    time.sleep(1)
# Now close the connection to V-REP:
vrep.simxFinish(clientID)
print ('Program ended')
