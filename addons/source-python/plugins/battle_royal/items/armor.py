## IMPORTS

from messages import SayText2

from .item import Item, items

class Armor(Item):
    item_type = 'armor'
    armor = 0

    def can_be_used(self, player):
        'Check if item can be used.'
        return True if player.armor < self.armor else False

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

        player.armor = self.armor
        player.inventory.discard(self, 1)
        SayText2('Add armor').send()
        return True