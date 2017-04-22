## IMPORTS

from . import Ammo

from messages import SayText2


class Rifle_Ammo(Ammo):
    name = 'Rifle Ammo'
    item_type = 'ammo'
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.classname).send()
