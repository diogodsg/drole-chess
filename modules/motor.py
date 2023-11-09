import RPi.GPIO as GPIO
import time
import math

#motor moves 4cm or 3.97cm per turn 



class MotorModule:
    def __init__(self):
        self.CONTACTS = [5, 12]
        self.DIRECTION = [2, 4]
        self.STEP = [3, 17]
        self.MAGNET = 22

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.DIRECTION[0], GPIO.OUT)
        GPIO.setup(self.DIRECTION[1], GPIO.OUT)
        GPIO.setup(self.STEP[0], GPIO.OUT)
        GPIO.setup(self.STEP[1], GPIO.OUT)
        GPIO.setup(self.MAGNET, GPIO.OUT)

        GPIO.output(self.MAGNET, GPIO.LOW)
        GPIO.output(self.DIRECTION[0], GPIO.HIGH)
        GPIO.output(self.DIRECTION[1], GPIO.HIGH)

        self.DELAY = 0.005 / 8
        self.STEP_DISTANCE = 3.97/1600
        GPIO.setup(self.CONTACTS[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.CONTACTS[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def move(self, axis, direction, steps):
        print(f"moving {steps} in dir {direction}")
        GPIO.output(self.DIRECTION[axis], direction)
        for i in range(abs(math.floor(steps))):
            GPIO.output(self.STEP[axis], GPIO.HIGH)
            time.sleep(self.DELAY)
            GPIO.output(self.STEP[axis], GPIO.LOW)
            time.sleep(self.DELAY)

    def return_home(self):
        print("returning home x")
        while not GPIO.input(self.CONTACTS[0]):  # verificar gpio
            self.move(0, 0, 1)
        print("returning home y")
        while not GPIO.input(self.CONTACTS[1]):  # verificar gpio
            self.move(1, 0, 1)

    def follow_path(self, path):
        # array de tuplas: [(2,4), (-1,8), (-5,9)]
        for movement in path:
            print("following:")
            print(movement)
            direction_x = 1 if movement[0] < 0 else 0
            direction_y = 1 if movement[1] > 0 else 0
            self.move(0, direction_x, movement[0] / self.STEP_DISTANCE)
            self.move(1, direction_y, movement[1] / self.STEP_DISTANCE)

    def set_magnet(self, value):
        if value:
            GPIO.output(self.MAGNET, GPIO.HIGH)
        else:
            GPIO.output(self.MAGNET, GPIO.LOW)
