## IMPORTS

from .item import Item

from messages import SayText2


class Small_Backpack(Item):
    name = 'Small Backpack'
    item_type = 'backpack'
    add_weight = 25
    weight = 0


    def use(self, player):
    	player.backpack = self
    	playaer.total_weight += self.add_weight
        SayText2('Equip ' + self.classname).send()
