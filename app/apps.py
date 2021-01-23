from django.apps import AppConfig
from machine import DrinkManufacturer

# the object that the view functions act on
machine = DrinkManufacturer()

class Conf(AppConfig):
    name = 'app'

        
        