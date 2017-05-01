## IMPORTS

from weapons.entity import Weapon
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .weapon import WeaponItem


class M4A1(WeaponItem):
    name = 'M4A1'
    item_type = 'weapon'
    slot = 'primary'
    clip = 0
    ammo = 0
    weight = 20
