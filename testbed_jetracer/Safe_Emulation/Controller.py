from jetracer.nvidia_racecar import NvidiaRacecar
import time

class JetRacerController:
    def __init__(self):
        self.valid_directions = ["forward", "backward", "left", "right"]
        self.interface_enabled = True
        self.car = NvidiaRacecar()

    def is_valid_move(self, direction, intensity):
        # Replace with actual implementation
        return direction in self.valid_directions and 0 <= intensity <= 100

    def move_forward(self, intensity):
        if self.interface_enabled and self.is_valid_move("forward", intensity):
            print(f"Moving forward with intensity {intensity}")
            self.car.throttle = (intensity/100)
            time.sleep(3)
        else:
            print("Invalid move or interface disabled")
            self.car.throttle = 0
            self.car.steering = 0

    def move_backward(self, intensity):
        if self.interface_enabled and self.is_valid_move("backward", intensity):
            print(f"Moving backward with intensity {intensity}")
            self.car.throttle = -(intensity/100)
            time.sleep(3)
        else:
            print("Invalid move or interface disabled")
            self.car.throttle = 0
            self.car.steering = 0

    def move_left(self, intensity):
        if self.interface_enabled and self.is_valid_move("left", intensity):
            print(f"Moving left with intensity {intensity}")
            self.car.steering = -(intensity/100)
            time.sleep(3)
        else:
            print("Invalid move or interface disabled")
            self.car.throttle = 0
            self.car.steering = 0

    def move_right(self, intensity):
        if self.interface_enabled and self.is_valid_move("right", intensity):
            print(f"Moving right with intensity {intensity}")
            self.car.steering = (intensity/100)
            time.sleep(3)
        else:
            print("Invalid move or interface disabled")
            self.car.throttle = 0
            self.car.steering = 0

    def disable_interface(self):
        self.interface_enabled = False

    def enable_interface(self):
        self.interface_enabled = True



# Example Usage

controller = JetRacerController()

user_inputs = [ # Simulate user inputs
    ("forward", 50),
    ("backward", 110),  # Invalid intensity
    ("left", 30),
    ("right", -10),     # Invalid intensity
    ("forward", 70)
]

for direction, intensity in user_inputs:
    if direction == "forward":
        controller.move_forward(intensity)
    elif direction == "backward":
        controller.move_backward(intensity)
    elif direction == "left":
        controller.move_left(intensity)
    elif direction == "right":
        controller.move_right(intensity)
