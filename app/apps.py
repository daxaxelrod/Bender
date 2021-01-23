from django.apps import AppConfig
from app.machine import DrinkManufacturer

# the object that the view functions act on
machine = DrinkManufacturer()

class Conf(AppConfig):
    name = 'app'

        
        