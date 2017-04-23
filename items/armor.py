## IMPORTS

from messages import SayText2

from . import Item

class Armor(Item):
    item_type = 'armor'
    armor = 0

    def use(self):
        SayText2('Can\'t use').send()