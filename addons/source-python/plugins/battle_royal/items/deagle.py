## IMPORTS

from .weapon import Weapon


class Deagle(Weapon):
    name = 'Deagle'
    classname = 'weapon_deagle'
    item_type = 'weapon'
    slot = 'secondary'
    clip = 10
    ammo = 0
    weight = 5
