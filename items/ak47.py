## IMPORTS

from entities.entity import Entity
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from . import Item
from ..hooks import _authorize_weapon


class Ak47(Item):
    name = 'Ak47'
    item_type = 'weapon'
    clip = 0
    ammo = 0
    weight = 20


    # def create(self, location):
    #     entity = Entity.create('weapon_ak47')
    #     entity.spawn()
    #     entity.teleport(location)
    #     return entity
     
    # def equip(self, player, callback):
    #     def delay_callback():
    #         weapon_pointer = player.give_named_item('weapon_ak47', 0, None, True)
    #         weapon = Entity(index_from_pointer(weapon_pointer))
    #         # Empty clip and ammo
    #         _authorize_weapon.append(index_from_pointer(weapon_pointer))
    #         callback(player, weapon)
     
    #     player.delay(0, delay_callback)
