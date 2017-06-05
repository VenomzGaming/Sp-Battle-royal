## IMPORTS

from .weapon import Weapon


class M4A1(Weapon):
    name = 'M4A1'
    classname = 'weapon_m4a1'
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

