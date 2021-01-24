import RPi.GPIO as GPIO
import logging
import time

SLEEP_INTERVAL = 1

class AxisMotor:
    
    def __init__(self, pin_number, stop_switches):
        self.signal_pin = pin_number
        self.logger = logging.getLogger(__name__)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        GPIO.output(self.signal_pin, GPIO.LOW)
        
        self.stop_switches = stop_switches # order matters
        for stop_switch in self.stop_switches:
            GPIO.setup(stop_switch, GPIO.IN)
        
        self.last_hit_switch = -1

    def get_log_msg(self, msg):
        return f"GPIO-pin#{self.signal_pin} " + msg
    

    def any_stop_switches_hit(self):

        for switch in self.stop_switches:
            if switch == self.last_hit_switch:
                continue
            if GPIO.input(switch):
                self.last_hit_switch = switch
                self.logger.debug(self.get_log_msg(f"Switch pin {switch} hit!"))
                return True
        return False

    def drive(self, timeout=20):
        self.logger.debug(self.get_log_msg("running"))
        timeout = time.time() + timeout
        try:
            GPIO.output(self.signal_pin, GPIO.HIGH)
            while time.time() < timeout:
                if self.any_stop_switches_hit():
                    break
            GPIO.output(self.signal_pin, GPIO.LOW)
        except Exception as e:
            self.logger.error(self.get_log_msg("error driving motor"))
            self.logger.error(e, exc_info=True)
            GPIO.output(self.signal_pin, GPIO.LOW)
        self.logger.debug(self.get_log_msg("Stoping!"))
        

