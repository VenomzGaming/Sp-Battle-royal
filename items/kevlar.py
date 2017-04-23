## IMPORTS

from .armor import Armor

from messages import SayText2


class Kevlar(Armor):
    name = 'Kevlar'
    armor = 100
    weight = 0
    models = ''


    def equip(self):
        SayText2('Equip ' + self.classname).send()
