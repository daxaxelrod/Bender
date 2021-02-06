import RPi.GPIO as GPIO
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument("pin")
args = parser.parse_args()

pin = int(args.pin)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
try:
	while True:
		print(GPIO.input(pin))
		time.sleep(.1)

except KeyboardInterrupt:
	GPIO.cleanup()
