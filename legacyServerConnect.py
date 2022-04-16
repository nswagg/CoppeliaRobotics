"""
@author Nick Waggoner
Date Created: 3-25-2022
Python Version 3.9

# The following is the associated Lua script needed to connect to the simulation. Place the script on a scene object
# I prefer the FLOOR object personally. Do not append to main scene script.
function sysCall_init()
    corout=coroutine.create(coroutineMain)
end

function sysCall_actuation()
    if coroutine.status(corout)~='dead' then
        local ok,errorMsg=coroutine.resume(corout)
        if errorMsg then
            error(debug.traceback(corout,errorMsg),2)
        end
    end
end

function sysCall_cleanup()
    -- do some clean-up here
end

function coroutineMain()
    simRemoteApi.start(19999)
end
"""

import sim as vrep #This installs the legacy version
import sys

def connectToServer():
    """Create and check the Connection"""
    vrep.simxFinish(-1)  # To close all connections that may be running
    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Starts the connection

    if clientID != -1:
        print("Connected to remote API server")
        # Checking connections and existence to the Pioneer motors
        res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking)
        if res == vrep.simx_return_ok:
            print('Number of objects in the scene: ', len(objs))
        else:
            print('Remote API function call returned with error: ', res)
    else:
        print("Could not connect to remote API server")
        sys.exit("Failed to connect")

    return clientID