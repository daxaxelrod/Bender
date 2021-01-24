import logging
from pprint import pformat
import time
import RPi.GPIO as GPIO
# from pygame import mixer
from app.motors.AxisMotor import AxisMotor
from app.constants.fsm import states, transitions
from collections import Counter
from app.models import Drink, Resevoir

logger = logging.getLogger(__name__)
# mixer.init()

"""
    There are two places for setting GPIO pin numbers
    in the __init__ fn here for the axis motors
    
    and IN the database table 'resevoir'
"""

class DrinkManufacturerFSM(object):
    
    def set_global_direction(self, value: bool):
        # take a second to reverse polarity.
        # We dont want a motor acting as a genorator for a second due to inertial 
        time.sleep(1)
        
        if value:
            pin_value = GPIO.HIGH
        else:
            pin_value = GPIO.LOW
            
        GPIO.output(self.global_direction_pin, pin_value)
        self.MOTOR_DIRECTION = value

    def __init__(self):
        self.global_direction_pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.global_direction_pin, GPIO.OUT)
        self.set_global_direction(True)
        

        # initialize screw motors
        self.horizontal_patter_motor = AxisMotor(6, [14, 15])
        self.shaker_motor = AxisMotor(17, [18, 24])
        self.vertical_platter_motor = AxisMotor(27, [25, 8])

        # pump motors are setup in execute pour
        # enabling them to be modified between runs
                

        # setup miscellanious switches
        self.drink_presentation_switch = 13
        GPIO.setup(self.drink_presentation_switch, GPIO.IN)


    def on_enter_idle(self):
        logger.info("entering idle")

    def on_exit_idle(self):
        logger.info("exiting idle")
        
    def on_enter_selecting(self):
        logger.info("moving platter outward")
        self.horizontal_patter_motor.drive()

    def on_exit_selecting(self, *args):
        logger.info("Exiting selecting selected")
        
        self.set_global_direction(False)
        self.horizontal_patter_motor.drive()
        self.set_global_direction(True)
        
    def wait_until_cup_provided_to_machine(self, *args):
        # condition required to enter preparing state
        # no timeout here, a risk
        while GPIO.input(self.drink_presentation_switch) == 0:
            logger.info("Waiting for drink to be placed on the platter")
            time.sleep(1)
        
        time.sleep(2)
        # playsounds "thank you"
        logger.info("Drink glass detected")
        return True

    def is_drink_unavailable(self, drink: Drink):
        # condition required to enter preparing state
        unavailable = drink.instructions.all().filter(ingredient__resevoir__isnull=True)
        result = unavailable.exists()
        if result:
            missing_ingredients = [x.ingredient.name for x in unavailable]
            logger.warn(f"Unable to make drink, ${drink.name}. Ingredients missing: {*missing_ingredients, }")
        return result

    def on_enter_preparing(self, drink: Drink):
        #if drink.start_sound:
        #    mixer.music.load(drink.start_sound)
        #    mixer.music.play()
        self.shaker_motor.drive()
 
        # actually prepare the drinks
        instructions = drink.instructions.all()

        # ingredient.resevoir_pin: instruction.pour_duration
        pour_map = {}
        for instruction in instructions:
            ingredient = instruction.ingredient
            pour_map[ingredient.resevoir.gpio_pin] = (instruction.pour_duration / 1000)
        logger.info(f"POUR MAP <pin: duration> {pformat(pour_map)}")
        self.execute_pour(pour_map)

    POUR_SLEEP_TIME = 0.3
    def execute_pour(self, pour_map):

        pins_switched_off = [] # verification that all pins were turned off
        start_time = time.time()
        # turn on all the pins, progressively turn them off based on the pour duration
        for pin in pour_map.keys():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        
        timeout = 5
        while self.is_pour_still_valid(pour_map, start_time, pin, timeout):
            time.sleep(self.POUR_SLEEP_TIME)
            # check if any pins overstayed their welcome. shut them off
            now = time.time()
            for pin, duration in pour_map.items():
                if now > start_time + duration:
                    GPIO.output(pin, GPIO.LOW)
                    pins_switched_off.append(pin)
                    pass
        
        # sanity check
        requested_pins = pour_map.keys()
        if len(pins_switched_off) != len(requested_pins):
            pins = Counter(requested_pins)
            off = Counter(pins_switched_off)
            left_on = (pins - off).elements()
            for err in left_on:
                logger.error(f"DRINK PIN LEFT ON: {err}")
                GPIO.output(err, GPIO.LOW)
                pass
        time.sleep(2) # let pour settle
        logger.info("Pour complete!")


    def on_exit_preparing(self, *args):
        #if drink.end_sound:
        #    mixer.music.load(drink.end_sound)
        #    mixer.music.play()
        
        # move the shaker back
        self.set_global_direction(False)
        self.shaker_motor.drive()
        self.set_global_direction(True)

    def is_pour_still_valid(self, pour_map, start_time, pin, timeout):
        return (any(time.time() < start_time + duration for pin, duration in pour_map.items()) or time.time() < start_time + timeout) 

    def on_enter_presenting(self):
        # drink is assumed complete
        self.vertical_platter_motor.drive()
        #FIXME
        import pdb; pdb.set_trace()
        while GPIO.input(self.drink_presentation_switch):
            time.sleep(1)
        logger.info("presenting drink")
    
    def on_exit_presenting(self):
        self.set_global_direction(False)
        self.vertical_platter_motor.drive()
        self.set_global_direction(True)