## IMPORTS

from .ammo import Ammo

from messages import SayText2


class Rifle_Ammo(Ammo):
    name = 'Rifle Ammo'
    slot = 'primary'
    tag = 'rifle'
    weight = 2
