## IMPORTS

from .ammo import Ammo

from messages import SayText2


class Pistol_Ammo(Ammo):
    name = 'Pistol Ammo'
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.__name__).send()
