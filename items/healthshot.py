## IMPORTS

from .weapon import Weapon

from messages import SayText2


class Healthshot(Weapon):
    name = 'Health shot'
    item_type = 'weapon'
    weight = 0
    models = ''


    def equip(self):
        SayText2('Equip ' + self.classname).send()
