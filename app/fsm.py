import logging
from pprint import pformat
import time
from playsound import playsound
from app.motors.AxisMotor import AxisMotor
from constants.fsm import states, transitions
from app.models import Drink, Resevoir

logger = logging.getLogger(__name__)

"""
    There are two places for setting GPIO pin numbers
    in the __init__ fn here for the axis motors
    
    and IN the database table 'resevoir'
"""

class DrinkManufacturer(object):
    
    #GLOBAL
    def set_global_direction(self, value: bool):
        # GPIO.output(self.global_direction_pin, GPIO.HIGH)
        self.MOTOR_DIRECTION = value

    def __init__(self):
        global_direction_pin = 31
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(global_direction_pin, GPIO.OUT)
        self.set_global_direction(True)
        

        # initialize screw motors
        self.horizontal_patter_motor = AxisMotor(3, [24, 25])
        self.shaker_motor = AxisMotor(4, [18, 19, 20])
        self.vertical_platter_motor = AxisMotor(5, [16, 17])

        # and the pump motors
        resevoirs


    def on_enter_idle(self):
        print("entering idle")

    def on_exit_idle(self):
        print("exiting idle, user selecting their drink")
        
    def on_enter_selecting(self):
        self.vertical_platter_motor.drive()

    def on_exit_selecting(self):
        print("drink selected")
        self.set_global_direction(False)
        self.horizontal_patter_motor.drive()
        self.set_global_direction(True)

    def on_enter_preparing(self, drink: Drink):
        playsound(drink.start_sound)
    
        # actually prepare the drinks
        instructions = drink.instructions.all()

        # ingredient.resevoir_pin: instruction.pour_duration
        pour_map = {}
        for instruction in instructions:
            ingredient = instruction.ingredient
            pour_map[ingredient.resevoir.gpio_pin] = instruction.pour_duration
        logger.info(pformat(pour_map))

        self.execute_pour(pour_map)

    def on_exit_preparing(self, drink: Drink):
        playsound(drink.ending_sound)