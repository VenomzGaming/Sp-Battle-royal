## IMPORTS

from engines.precache import Model
from entities.entity import Entity
from mathlib import Vector
from messages import SayText2
from players.entity import Player


from .inventory import Inventory

## ALL DECLARATIONS

__all__ = (
    'BattleRoyalPlayer',
)


class BattleRoyalPlayer(Player):

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
        entity = Entity.create('prop_physics_override')
        location = self.origin
        entity.origin = Vector(location.x+32, location.y, location.z)
        entity.model = Model('models/props/props_crates/wooden_crate_32x64.mdl')
        entity.spawn_flags = 265
        entity.spawn()

        return entity

    def pick_up(self, item):
        add = self._inventory.add(item)
        if not add:
            return False     
        return True      

    def drop(self, item, amount=None):
        self._inventory.remove(item, amount)
        if item.item_type == 'weapon':
            weapon = self.get_weapon('weapon_' + item.__class__.__name__.lower())
            if weapon is not None:
                weapon.remove()
                
        entity = item.create(self.origin)
        SayText2(item.name + ' remove from inventory').send()
        return entity

    def use(self, item):
        can_used = item.use(self)
        if can_used:
            if item.item_type == 'ammo':
                self._inventory.remove(item) 
            else:
                self._inventory.remove(item, 1) 

    def equip(self, item, loot=False):
        if item.item_type == 'weapon':
            item.equip(self, loot)    
        else:
            item.equip(self)
        