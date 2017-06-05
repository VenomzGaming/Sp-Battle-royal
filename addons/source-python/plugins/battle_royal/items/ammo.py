## IMPORTS

from engines.precache import Model
from messages import SayText2

from .item import Item, items


class Ammo(Item):
    name = 'Ammo (10 Primary Bullets)'
    item_type = 'ammo'
    weapon = ''
    ammo = 10
    weight = 0.0
    model = Model('models/props/coop_cementplant/coop_ammo_stash/coop_ammo_stash_full.mdl')

    def can_be_used(self, player):
        'Check if item can be used.'
        weapon = player.get_weapon(self.weapon)
        return bool(weapon is not None)

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

        weapon = player.get_weapon(self.weapon)
        weapon.ammo += self.ammo

        player.inventory.discard(self)
        return True

