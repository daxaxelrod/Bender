from django.apps import AppConfig
import RPi.GPIO as GPIO

class Conf(AppConfig):
    name = 'app'

    def ready(self):
        from app.models import Resevoir
        # set all resevoirs to low to trigger relays
        # high is relay open aka pump off
        GPIO.setmode(GPIO.BCM)
        resevoirs = Resevoir.objects.all()
        for res in resevoirs:
            GPIO.setup(res.gpio_pin, GPIO.OUT)
            GPIO.output(res.gpio_pin, GPIO.HIGH)
