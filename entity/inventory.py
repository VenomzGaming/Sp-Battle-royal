## IMPORTS

from messages import SayText2

from ..items.item import Item

## ALL DECLARATIONS

__all__ = (
    'Inventory',
)


class Inventory:

    def __init__(self, player):
        self.player = player
        self._items = dict()

    @property
    def items(self):
        return self._items

    def _can_add(self, item):
        return True if (self.player.total_weight - item.weight) > 0 else False

    def _add_weight(self, item):
        self.player.total_weight -= item.weight

    def _remove_weight(self, item):
        self.player.total_weight += item.weight

    def add(self, item):
        if not isinstance(item, Item):
            raise ValueError('Argument must be an Item')

        if not self._can_add(item):
            SayText2('Weight exceed').send()
            return False

        if item.name not in self._items:
            item.amount = 1
            self._items[item.name] = item
        else:
            item = self._items[item.name]
            item.amount += 1
            self._items[item.name] = item

        self._add_weight(item)
        return True

    def remove(self, item, amount=None):
        if not isinstance(item, Item):
            raise ValueError('Argument must be an Item')

        if item.name not in self._items:
            return False

        if amount is not None:
            if amount > item.amount:
                del self._items[item.name]
                SayText2('Remove').send()
            else:
                item.amount -= amount
                self._items[item.name] = item
                SayText2('Remove Amount').send()
        else:
            del self._items[item.name]
            SayText2('Remove').send()

        self._remove_weight(item) 
              
    def show(self):
        for item in self._items.values():
            SayText2(item.name).send()
        else:
            SayText2('Any').send()
