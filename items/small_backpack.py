## IMPORTS

from .item import Item

from messages import SayText2


class Small_Backpack(Item):
    name = 'Small Backpack'
    item_type = 'backpack'
    weight = 0
    models = ''


    def use(self):
        SayText2('Equipe ' + self.classname).send()
