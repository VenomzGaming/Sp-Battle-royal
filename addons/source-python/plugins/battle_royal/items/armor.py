## IMPORTS

from messages import SayText2

from .item import Item

class Armor(Item):
    item_type = 'armor'
    armor = 0

    def equip(self, player):
        if player.armor < self.armor:
            self.use(player)

    def use(self, player):
        player.armor = self.armor
        SayText2('Add armor').send()