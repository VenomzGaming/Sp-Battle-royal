## IMPORTS

from engines.precache import Model
from entities.entity import Entity
from listeners.tick import Delay
from mathlib import Vector
from messages import SayText2
from players.entity import Player


from .inventory import Inventory
from .sprint import Sprint
from .stamina import Stamina
from .score import Score

from ..config import _configs

## ALL DECLARATIONS

__all__ = (
    'BattleRoyalPlayer',
)


class BattleRoyalPlayer(Player):
    '''
    BattleRoyalPlayer override Source-python Player
    class to manager battle royal features for the player.
    :param int index:
        A valid player index.
    :param Item backpack (default=None)
        Add item backpack to player
    '''

    def __init__(self, index, backpack=None, *args, **kwargs):
        super().__init__(index, *args, **kwargs)
        self.score = 0
        self._backpack = backpack
        self._group = None
        self._score = Score(self)

        if _configs['enable_stamina'].get_int():
            self._stamina = Stamina(self)

        self._sprint = Sprint(self)
        self._inventory = Inventory(self)


    def get_backpack(self):
        'Get player wear backpack.'
        return self._backpack

    def set_backpack(self, backpack):
        'Set player backpack.'
        self._backpack = backpack

    backpack = property(get_backpack, set_backpack)

    def get_group(self):
        'Get player group.'
        return self._group

    def set_group(self, group):
        'Set player group.'
        self._group = group

    group = property(get_group, set_group)

    @property
    def sprint(self):
        'Return :class Sprint object.'
        return self._sprint

    @property
    def stamina(self):
        'Return :class Stamina object.'
        return self._stamina

    @property
    def br_score(self):
        'Return :class Score object.'
        return self._score

    @property
    def inventory(self):
        'Return :class Iventory object.'
        return self._inventory
    
    def drop_inventory(self):
        'Create and spawn entity of inventory.'
        entity = Entity.create('prop_physics_override')
        entity.origin = self.origin
        entity.model = Model('models/props/props_crates/wooden_crate_32x64.mdl')
        entity.spawn_flags = 256
        entity.solid_flags = 152
        entity.collision_group = 11
        Delay(0.1, entity.spawn)
        return entity

    def drop(self, item, amount=None):
        'Drop item from inventory and create item entity.'
        self._inventory.discard(item, amount)           
        item = item.__class__.create(self.origin)
        if amount is not None:
            item.amount = amount
        SayText2(item.name + ' remove from inventory').send()

    def use(self, item):
        'Use item.'
        return item.on_use(self)
