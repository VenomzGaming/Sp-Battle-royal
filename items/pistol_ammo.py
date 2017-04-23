## IMPORTS

from . import Item

from messages import SayText2


class Pistol_Ammo(Item):
    name = 'Pistol Ammo'
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.__name__).send()
