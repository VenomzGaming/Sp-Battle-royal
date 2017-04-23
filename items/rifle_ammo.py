## IMPORTS

from .ammo import Ammo

from messages import SayText2


class Rifle_Ammo(Ammo):
    name = 'Rifle Ammo'
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.classname).send()
