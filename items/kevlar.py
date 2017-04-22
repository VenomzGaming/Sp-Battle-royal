## IMPORTS

from . import Item

from messages import SayText2


class Kevlar(Item):
    name = 'Kevlar'
    item_type = 'armor'
    armor = 100
    weight = 0
    models = ''


    def equip(self):
        SayText2('Equip ' + self.classname).send()
