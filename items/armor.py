## IMPORTS

from messages import SayText2

from .item import Item

class Armor(Item):
    item_type = 'armor'
    armor = 0

    def use(self, player):
        player.armor = self.armor
        SayText2('Add armor').send()