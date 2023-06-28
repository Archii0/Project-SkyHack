from pynput import keyboard

def on_key_press(self, key):
    # Handle the key press event
    print(f"Key {key} pressed")  

def on_key_release(self, key):
    # Handle the key release event
    print(f"Key {key} released")

def start(self):
    with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
        #Join listener to main thread
        listener.join()