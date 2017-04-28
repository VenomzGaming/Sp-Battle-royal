## IMPORTS

from .ammo import Ammo

from messages import SayText2


class Pistol_Ammo(Ammo):
    name = 'Pistol Ammo'
    slot = 'secondary'
    tag = 'pistol'
    weight = 0
