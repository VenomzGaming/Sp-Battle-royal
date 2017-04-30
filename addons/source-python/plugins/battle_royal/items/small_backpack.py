## IMPORTS

from .item import Item

from messages import SayText2


class Small_Backpack(Item):
    name = 'Small Backpack'
    item_type = 'backpack'
    add_weight = 25
    weight = 0


    def equip(self, player):
        if  player.backpack is None or self.add_weight > player.backpack.add_weight:
            self.use(player)
            player.inventory.remove(self)

    def use(self, player):
        player.backpack = self
        player.total_weight += self.add_weight
        SayText2('Equip ' + self.__class__.__name__).send()
