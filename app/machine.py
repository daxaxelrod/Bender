import time
import logging
from app.constants.fsm import transitions, states
from .fsm import DrinkManufacturerFSM
from transitions import Machine
from app.models import Drink
from transitions.extensions.states import add_state_features, Timeout
from transitions.core import MachineError

logger = logging.getLogger(__name__)

@add_state_features(Timeout)
class TimeoutEnabledMachine(Machine):
    pass


class DrinkManufacturer(object):

    def __init__(self):
        self.drink_maker = DrinkManufacturerFSM()
        self.machine = TimeoutEnabledMachine(model=self.drink_maker, states=states, transitions=transitions, initial='idle')
        logger.info(f"Machine state: {self.drink_maker.state}" )

    def awaken(self):
        self.drink_maker.wake()

    def on_drink_selection(self, drink: Drink):
        self.drink_maker.prepare_drink(drink)
        try:
            self.drink_maker.present()
            self.drink_maker.reset()
        except MachineError:
            logger("machine couldnt transition to next state")