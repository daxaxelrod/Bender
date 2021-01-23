import logging
from pprint import pformat
import time
from playsound import playsound
from app.motors.AxisMotor import AxisMotor
from constants.fsm import states, transitions
from collections import Counter
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
        self.global_direction_pin = 31
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(global_direction_pin, GPIO.OUT)
        self.set_global_direction(True)
        

        # initialize screw motors
        self.horizontal_patter_motor = AxisMotor(3, [24, 25])
        self.shaker_motor = AxisMotor(4, [18, 19, 20])
        self.vertical_platter_motor = AxisMotor(5, [16, 17])

        # and the pump motors
        # resevoirs


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

    def is_drink_unavailable(self, drink: Drink):
        # condition required to enter preparing state
        unavailable = drink.instructions.all().filter(ingredient__resevoir__isnull=True)
        result = unavailable.exists()
        if result:
            missing_ingredients = [x.ingredient.name for x in unavailable]
            logger.warn(f"Unable to make drink, ${drink.name}. Ingredients missing: {*missing_ingredients, }")
        return result

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

    POUR_SLEEP_TIME = 300
    def execute_pour(self, pour_map):
        # GPIO.setmode(GPIO.BCM)

        pins_switched_off = [] # verification that all pins were turned off
        start_time = time.time_ns() * 1000
        # turn on all the pins, progressively turn them off based on the pour duration
        for pin in pour_map.keys():
            pass
            # GPIO.setup(pin, GPIO.OUT)
            # GPIO.output(GPIO_PIN, GPIO.HIGH)
        
        timeout = 20000
        while self.is_pour_still_valid(pour_map, start_time, pin, timeout):
            time.sleep(self.POUR_SLEEP_TIME)
            # check if any pins overstayed their welcome. shut them off
            now = time.time_ns() * 1000
            for pin, duration in pour_map.items():
                if now > start_time + duration:
                    # GPIO.output(GPIO_PIN, GPIO.LOW)
                    pins_switched_off.append(pin)
                    pass
        
        # sanity check
        requested_pins = pour_map.keys()
        if len(pins_switched_off) != len(requested_pins):
            pins = Counter(requested_pins)
            off = Counter(pins_switched_off)
            left_on = (pins - off).elements()
            for err in left_on:
                pass
                # GPIO.output(GPIO_PIN, GPIO.LOW)
            logger.error("a pin has not been turned off!") 
        
        logger.info("Pour complete!")

    
    def is_pour_still_valid(self, pour_map, start_time, pin, timeout):
        return (any(time.time_ns() * 1000 < start_time + duration for pin, duration in pour_map.items()) or time.time_ns() * 1000 < start_time + timeout) 