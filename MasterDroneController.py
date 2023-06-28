"""Archie's master copy of the drone controller

To change: get rid of key hold functionality as it does not work given the
way that the drone has to receive a request, then send back a response before
processing the next request that we give it"""


from pynput import keyboard
from djitellopy import Tello

class DroneController:
    def __init__(self):
        self.drone = Tello()
        self.pressed_keys = set()
        self.emergency_stop_key = keyboard.KeyCode.from_char('x')
        self.distance = 200 # the distance to move the drone with each command
        self.verticalDistance = 30
        self.smallDistance = 50
        self.rotateDegrees = 45 # the amount of degrees to rotate the drone with rotation commands
        
        # Connect to the Tello drone
        self.drone.connect()
        # Set speed of the Tello drone 
        self.drone.set_speed(100)

        print("Drone battery: {0}%".format(self.drone.get_battery()))

        if self.drone.get_battery() <= 7:  
            print("Drone will not take off due to low battery")
                
         
        # Set the keyboard control mapping
        self.key_mapping = {
            keyboard.Key.up: (self.drone.move_up, [self.verticalDistance]),
            keyboard.Key.down: (self.drone.move_down, [self.verticalDistance]),
            keyboard.KeyCode.from_char('w'): (self.drone.move_forward, [self.distance]),
            keyboard.KeyCode.from_char('s'): (self.drone.move_back, [self.distance]),
            keyboard.KeyCode.from_char('a'): (self.drone.move_left, [self.distance]),
            keyboard.KeyCode.from_char('d'): (self.drone.move_right, [self.distance]),
            keyboard.KeyCode.from_char('q'): (self.drone.rotate_counter_clockwise, [self.rotateDegrees]),
            keyboard.KeyCode.from_char('e'): (self.drone.rotate_clockwise, [self.rotateDegrees]),
            keyboard.KeyCode.from_char('i'): (self.drone.move_forward, [self.smallDistance]),
            keyboard.KeyCode.from_char('k'): (self.drone.move_back, [self.smallDistance]),
            keyboard.KeyCode.from_char('j'): (self.drone.move_left, [self.smallDistance]),
            keyboard.KeyCode.from_char('l'): (self.drone.move_right, [self.smallDistance]),
            keyboard.KeyCode.from_char(','): (self.drone.flip_left, None),
            keyboard.KeyCode.from_char('.'): (self.drone.flip_right, None),
            keyboard.Key.space: (self.drone.takeoff, None),
            keyboard.Key.esc: (self.drone.land, None),
            self.emergency_stop_key: (self.emergency_stop, None)
        }


    def on_key_press(self, key):
        print("Key press: {0}".format(key))
        if key in self.key_mapping:
            if key not in self.pressed_keys:
                # Execute the corresponding drone control function
                func, parameters = self.key_mapping[key]
                self.execute_function(func, params=parameters) 
                self.pressed_keys.add(key)

    def on_key_release(self, key):
        if key in self.key_mapping:
            if key in self.pressed_keys:
                # Stop the corresponding drone control function
                # self.key_mapping[key]
                self.pressed_keys.remove(key)

    def on_key_hold(self):
        print(self.pressed_keys)
        for key in self.pressed_keys:
            # Execute the drone control function for each held key
            self.key_mapping[key]

    def execute_function(self, func, params):
        # Execute the drone control function with or without parameters
        if params is not None:
            try:
                func(*params)
            except:
                print("Error running command")
        else:
            try:
                func()
            except: 
                print("Error running command")

    def emergency_stop(self):
        # Stop all drone movement and land immediately
        for key in self.pressed_keys:
            if key != self.emergency_stop_key:
                #self.key_mapping[key](0)
                self.pressed_keys.remove(key)
        self.drone.land()

    def start(self):
        # Create an instance of the KeyboardListener class
        with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            # Start listening to keyboard events
            listener.join()

            # Start a timer to call on_key_hold() periodically
            # Adjust the interval as needed
            interval = 0.5  # 1000 milliseconds
            timer = keyboard.Controller()
            timer.schedule(self.on_key_hold, interval)

            # Keep the main thread running
            while True:
                pass

# Create an instance of DroneController
droneController = DroneController()
droneController.start()