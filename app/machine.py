import time
from app.constants.fsm import transitions, states
from .fsm import DrinkManufacturerFSM
from transitions import Machine
from app.models import Drink
from transitions.extensions.states import add_state_features, Timeout


@add_state_features(Timeout)
class TimeoutEnabledMachine(Machine):
    pass


class DrinkManufacturer(object):

    def __init__(self):
        self.model = DrinkManufacturerFSM()
        self.machine = TimeoutEnabledMachine(model=self.model, states=states, transitions=transitions, initial='idle')

    def awaken(self):
        self.machine.wake()

        # if after 2 minutes no selection has been made, revert back to idle
        

    def on_drink_selection(self, drink: Drink):
        self.machine.prepare_drink(drink)
        self.machine.present()
        self.machine.reset()