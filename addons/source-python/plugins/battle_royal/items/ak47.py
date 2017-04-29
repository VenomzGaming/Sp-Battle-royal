## IMPORTS

from entities.entity import Entity
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .weapon import Weapon
# from .globals import _authorize_weapon


class Ak47(Weapon):
    name = 'Ak47'
    item_type = 'weapon'
    slot = 'primary'
    clip = 0
    ammo = 0
    weight = 20
