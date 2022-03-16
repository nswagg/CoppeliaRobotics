"""
@author Nick Waggoner

"""
import sys, time, zmqRemoteApi
from zmqRemoteApi.clients.python.zmqRemoteApi import RemoteAPIClient


client = RemoteAPIClient()

# Get a remote object
sim = client.getObject('sim')

# Call API Function
APPFUNC = sim.getObject('/Floor')
print(APPFUNC)

# clientId = simulation.stopSimulation()