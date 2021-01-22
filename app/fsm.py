import logging
import time
from transitions import Machine

from constants.states import states

class DrinkManufacturer(Machine):
    
    states = states
    self.resevoirs = {}
    self.drink_selection: [Drink] = [] # db op
    self.drinks_completed = self.init_drink_map()

    def init_drink_map(self):
        result = {}
        for drink in self.drink_selection:
            result[drink]