from enum import Enum

class WheelType(Enum):
    ALLOY = "ALLOY"
    STEEL = "STEEL"
    WOOD = "WOOD"

class Wheel:
    def __init__(self, wheel_type: WheelType):
        self.wheel_type = wheel_type

    def get_wheel_type(self):
        return self.wheel_type

class Car:
    # sample of dependency injection
    def __init__(self, wheel : Wheel = Wheel(WheelType.ALLOY)):
        self.wheel = wheel

    def get_wheel_type(self):
        return self.wheel.get_wheel_type()  
    
sample_car = Car()
print(sample_car.get_wheel_type())