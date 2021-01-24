import RPi.GPIO as GPIO
import logging
import time

SLEEP_INTERVAL = 1

class AxisMotor:
    
    def __init__(self, pin_number, stop_switches):
        self.signal_pin = pin_number
        self.logger = logging.getLogger(__name__)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        self.stop_switches = stop_switches # order matters
        for stop_switch in self.stop_switches:
            GPIO.setup(stop_switch, GPIO.IN)

    def get_log_msg(self, msg):
        return f"GPIO-pin#{self.signal_pin} " + msg
    
    def get_time_millis(self):
        return time.time_ns() * 1000

    def any_stop_switches_hit(self):

        # important that sleep happens first so that the motors have a chance to release
        # the old switches
        time.sleep(SLEEP_INTERVAL)
        self.logger.debug(self.get_log_msg("Checking stop switches"))
        for switch in self.stop_switches:
            if GPIO.input(switch):
                 return True
        return False

    def drive(self, timeout=20000):
        self.logger.debug(self.get_log_msg("running"))
        timeout = self.get_time_millis() + timeout
        try:
            GPIO.output(self.signal_pin, GPIO.HIGH)
            while self.get_time_millis() < timeout:
                if self.any_stop_switches_hit():
                    break
            GPIO.output(self.signal_pin, GPIO.LOW)
        except Exception as e:
            self.logger.error(self.get_log_msg("error driving motor"))
            self.logger.error(e, exc_info=True)
            GPIO.output(self.signal_pin, GPIO.LOW)
        self.logger.debug(self.get_log_msg("Stoping!"))
        

