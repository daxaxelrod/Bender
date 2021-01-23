import time
from app.constants.fsm import transitions, states
from .fsm import DrinkManufacturerFSM
from transitions import Machine
from app.models import Drink


class DrinkManufacturer(object):

    def __init__(self):
        self.model = DrinkManufacturerFSM()
        self.machine = Machine(model=self.model, states=states, transitions=transitions, initial='idle')

    def awaken(self):
        self.machine.wake()

        # if after 2 minutes no selection has been made, revert back to idle
        now = time.time() 
        timeout = now + 120 # seconds
        while now < timeout:
            time.sleep(1)
        if self.machine.state == "selecting":
            self.machine.sleep()
            

    def on_drink_selection(self, drink: Drink):
        self.machine.prepare_drink(drink)
        self.machine.present()
        self.machine.reset()