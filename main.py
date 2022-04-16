"""
@author Nick Waggoner
Date Created: 3-27-2022
Python Version 3.9
0mappingTest.py
"""
# Imported Python packages
import matplotlib.pyplot as plt
import sim as vrep
import time
import threading

# Imported User packages
import legacyServerConnect
import robotClass
import getHandles


# Retrieve all obstacles from the coppelia scene
EXCLUDED_OBJECTS = ["Floor", "box", "visible", "element", "visibleElement", "Cuboid"]
FLOOR = "/Floor/element"
ROBOT = "/Pioneer_p3dx"
VERBOCITY = 1
simX = 5 # simulation scene width in meters
simY = 5 # simulation scene height in meters
GRIDW = simX * 3# subdivisions on X axis. Assume our scene is a square
subdivisions = simX/GRIDW # The distance between nodes in plot
clientID = legacyServerConnect.connectToServer() # checks for the connection

def plotNodes(sim, obstacles):
    x = +0.0000e00
    y = +0.0000e00
    for i in range(GRIDW):
        for j in range(GRIDW):
            plt.plot(x+(i*subdivisions),y+(j*subdivisions), '.r', markersize=5)

vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) # Initializes Streaming

err_code, obstacle = vrep.simxGetObjectHandle(clientID, "Cuboid", vrep.simx_opmode_blocking)
if err_code != 0:
    print("ERR: could not get obstacles")

vrep.getShapeBB()
plotNodes(clientID, obstacle)

def driver():
    """Program Loop"""
    getHandles.getAllSceneShapes(clientID)

    while True:

        time.sleep(0.2)

    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
    print("Done")
    return




