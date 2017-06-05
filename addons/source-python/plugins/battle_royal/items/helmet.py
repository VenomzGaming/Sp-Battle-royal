## IMPORTS

from messages import SayText2

from .armor import Armor
from .item import items


class Helmet(Armor):
    name = 'Helmet'
    weight = 2.0

    def can_be_used(self, player):
        'Check if item can be used.'
        return True if player.has_helmet else False

    def on_pickup(self, player):
        'Upon the item being picked up.'
        if not player.inventory.add(self):
            return
            
        if self.can_be_used(player):
            self.on_use(player)

        self.on_remove()

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

        player.has_helmet = True
        player.inventory.discard(self, 1)
        SayText2('Add Helmet').send()
        return True
