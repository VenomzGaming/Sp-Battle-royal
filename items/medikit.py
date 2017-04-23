## IMPORTS

from . import Item

from messages import SayText2


class Medikit(Item):
    name = 'Medic Kit'
    heal = 50
    weight = 0
    models = ''


    def use(self):
        SayText2('Use ' + self.classname).send()
