## IMPORTS

from .weapon import WeaponItem

from messages import SayText2


class Healthshot(WeaponItem):
    name = 'Health shot'
    item_type = 'weapon'
    weight = 0
