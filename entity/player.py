## IMPORTS

from messages import SayText2
from players.entity import Player as SourcePythonPlayer


from .inventory import Inventory

## ALL DECLARATIONS

__all__ = (
    'Player',
)


class Player(SourcePythonPlayer):

    def __init__(self, index, weight, backpack=None):
        super().__init__(index)
        self.score = 0
        self._total_weight = weight
        self._backpack = backpack
        self._inventory = Inventory(self)

    def get_total_weight(self):
        return self._total_weight

    def set_total_weight(self, total_weight):
        self._total_weight = total_weight

    total_weight = property(get_total_weight, set_total_weight)

    def get_backpack(self):
        return self._backpack

    def set_backpack(self, backpack):
        self._backpack = backpack

    backpack = property(get_backpack, set_backpack)

    @property
    def inventory(self):
        return self._inventory


    def drop_inventory(self):
        SayText2('Drop inventory').send()

    def pick_up(self, item):
        add = self._inventory.add(item)
        if not add:
            return False
            
        return True      

    def drop(self, item):
        self._inventory.drop(item)
        # Re create and store entity
        SayText2(item.name + ' remove from inventory').send()

    def equip(self, item):
        SayText2('Equip').send()

    def use(self, item):
        SayText2('Use').send()

    def destroy(self, item):
        SayText2('Destroy').send()
        