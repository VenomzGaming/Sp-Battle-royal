## IMPORTS

from .item import Item, items

from messages import SayText2


class Small_Backpack(Item):
    name = 'Small Backpack'
    item_type = 'backpack'
    add_weight = 25
    weight = 0.0

    def can_be_used(self, player):
        'Check if item can be used.'
        return True if player.backpack is None or self.add_weight > player.backpack.add_weight else False

    def on_pickup(self, player):
        'Upon the item being picked up.'
        if not player.inventory.add(self):
            return False

        if self.can_be_used(player):
            self.on_use(player)

        self.on_remove()
        return True

    def on_remove(self):
        'Called upon the wanted removal of the entity.'
        if self.entity is None:
            return

        if self in items:
            items.remove(self)
        self.entity.remove()

    def on_use(self, player):
        'Called upon the item being used.'
        if not self.can_be_used(player):
            return False

        player.backpack = self
        player.inventory.max_weight += self.add_weight
        SayText2('Equip ' + self.__class__.__name__).send()
        player.inventory.discard(self)
        return True
