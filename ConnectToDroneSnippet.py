"""This is a snippet of how to connect to the drone and then
run some of the simple API commands"""

#Import required library
from djitellopy import Tello

#Create drone object as an instance of a Tello drone
drone = Tello()

#Connect to your drone - you will need to be connected to your drone's access point
#for this to work, i.e. WiFi is connected to TELLO-941A77
drone.connect()

#Take off the drone - no other commands will run unless the drone is in the air
drone.takeoff()

#Some basic movement from the DJITelloPy Tello library
drone.move_forward(20)
drone.rotate_clockwise(180)
drone.move_forward(20)
drone.rotate_clockwise(180)

#Land the drone - please note that the drone will autoland after 15 seconds of 
#it receiving no requests/commands
drone.land()

