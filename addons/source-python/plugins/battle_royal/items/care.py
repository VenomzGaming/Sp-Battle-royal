## IMPORTS

from .item import Item, items


class Care(Item):
    item_type = 'care'
    health = 0

    def _repeat(self):
        add_health = self.health // 5
        if not self.can_be_used(add_health):
            self._player.health = 100
            self._repeater.stop()
            return

        self._player.health += add_health

    def can_be_used(self, add_health=0):
        'Check if item can be used.'
        if self._player.health == 100 or self._player.health + add_health > 100:
            return False
        return True

    def on_pickup(self, player):
        'Upon the item being picked up.'
        if not player.inventory.add(self):
            return False
        self.on_remove()
        return True

    def on_remove(self):
        'Called upon the wanted removal of the entity.'
        if self.entity is None:
            return

        if self in items:
            items.remove(self)
        self.entity.remove()  

    def on_dropped(self, player):  
        self.entity.origin = player.origin
        self.entity.spawn_flags = 256
        self.entity.solid_flags = 152
        self.entity.collision_group = 11
        self.entity.spawn()
