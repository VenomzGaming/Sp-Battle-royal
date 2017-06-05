## IMPORTS

from .weapon import Weapon


class Ak47(Weapon):
    name = 'Ak47'
    classname = 'weapon_ak47'
    item_type = 'weapon'
    slot = 'primary'
    clip = 30
    ammo = 0
    weight = 10.0

    def __init__(self, entity, *args, **kwargs):
        'Setting the ammo and clip count of the weapon on pickup.'
        super().__init__(entity, *args, **kwargs)
        self.ammo = 0
        self.clip = 30
