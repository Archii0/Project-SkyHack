#Script to be tested for basic use
"""This is an example of a student that has filled out the starter template 


Changes to make: test if you can create a listener with no on_release function
"""


from pynput import keyboard
from djitellopy import Tello

class DroneController:
    def __init__(self):
        self.drone = Tello() 
        self.drone.connect()
        self.distance = 30  # Adjust the distance as needed
      

    def on_key_press(self, key):
        if key == keyboard.Key.space:
            self.drone.takeoff()
        elif key == keyboard.Key.esc:
            self.drone.land()
        elif key == keyboard.KeyCode.from_char('w'):
            self.drone.move_forward(self.distance)
        elif key == keyboard.KeyCode.from_char('s'):
            self.drone.move_back(self.distance)
        elif key == keyboard.KeyCode.from_char('a'):
            self.drone.move_left(self.distance)
        elif key == keyboard.KeyCode.from_char('d'):
            self.drone.move_right(self.distance)
        elif key == keyboard.Key.up:
            self.drone.move_up(self.distance)
        elif key == keyboard.Key.down:
            self.drone.move_down(self.distance)

    def on_key_release(self, key):
        #This function has no useage in the requirements of the program
        #Check if you can define a listener without an on_release function?
        print('Key released')


    def start(self):
        with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()

# Create an instance of DroneController
controller = DroneController()
controller.start()
