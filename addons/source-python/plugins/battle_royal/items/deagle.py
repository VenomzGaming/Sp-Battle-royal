## IMPORTS

from weapons.entity import Weapon
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .weapon import WeaponItem


class Deagle(WeaponItem):
    name = 'Deagle'
    item_type = 'weapon'
    slot = 'secondary'
    clip = 0
    ammo = 0
    weight = 5
