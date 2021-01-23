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

    def get_log_msg(self, msg):
        return f"GPIO-pin#{self.signal_pin} " + msg
    
    def get_time_millis(self):
        return time.time_ns() * 1000

    def any_stop_switches_hit(self):
        for switch in self.stop_switches:
            time.sleep(2)
            return True
            # if GPIO.input(switch):
            #     return True
        return False

    def drive(self, timeout=20000):
        self.logger.debug(self.get_log_msg("running"))
        timeout = self.get_time_millis() + timeout
        try:
            GPIO.output(self.signal_pin, GPIO.HIGH)
            while not self.any_stop_switches_hit() or self.get_time_millis() < timeout:
                time.sleep(SLEEP_INTERVAL)
            GPIO.output(self.signal_pin, GPIO.LOW)
        except Exception as e:
            self.logger.error(self.get_log_msg("error driving motor"))
            self.logger.error(e, exc_info=True)
            GPIO.output(self.signal_pin, GPIO.LOW)
        self.logger.debug(self.get_log_msg("Stoping!"))
        

