import logging
import time
from transitions import Machine

from constants.fsm import states, transitions

class DrinkManufacturer(object):
    
    states = states

    def __init__(self, name):
        self.machine = Machine(model=self, states=states, initial=states[0])

        self.machine.add_transitions(transitions)
        