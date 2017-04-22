## IMPORTS

from . import Ammo

from messages import SayText2


class Pistol_Ammo(Ammo):
    name = 'Pistol Ammo'
    item_type = 'ammo'
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.__name__).send()
