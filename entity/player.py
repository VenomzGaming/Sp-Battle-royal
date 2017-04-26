## IMPORTS

from messages import SayText2
from players.entity import Player as SourcePythonPlayer


from .entity.battleroyal import _battle_royal
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
        entity = Entity.create('prop_backpack')
        entity.spawn()
        entity.world_model_index = Model('backapack').index
        entity.teleport(self.origin)
        _battle_royal.add_item_ent(entity, self._inventory)

    def pick_up(self, item):
        add = self._inventory.add(item)
        if not add:
            return False
            
        return True      

    def drop(self, item, amount=None):
        self._inventory.remove(item, amount)
        # Re create and store entity
        entity = item.create(self.origin)
        _battle_royal.add_item_ent(entity, item)
        SayText2(item.name + ' remove from inventory').send()
        