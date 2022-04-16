"""
@author Nick Waggoner
Date Created: 4-16-22
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
    simRemoteApi.start(23000)
end
"""

from zmqRemoteApi import RemoteAPIClient
import sys

def serverConnect():
    """Not sure how to get this running yet. Would help with better functionality"""
    sim = RemoteAPIClient('localhost', 23000)

    if sim != -1:
        print("Connected to remote API server")
        # Checking connections and existence to the Pioneer motors
        res, objs = sim.GetObjects(sim,sim.handle_all, sim.opmode_blocking)
        if res == sim.return_ok:
            print('Number of objects in the scene: ', len(objs))
        else:
            print('Remote API function call returned with error: ', res)
    else:
        print("Could not connect to remote API server")
        sys.exit("Failed to connect")

    return sim
