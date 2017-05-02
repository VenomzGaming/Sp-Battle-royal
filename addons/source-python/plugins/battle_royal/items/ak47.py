## IMPORTS

# from entities.entity import Entity
from weapons.entity import Weapon
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .weapon import WeaponItem
# from .globals import _authorize_weapon


class AK47(WeaponItem):
    name = 'AK47'
    item_type = 'weapon'
    slot = 'primary'
    clip = 30
    ammo = 0
    weight = 20
