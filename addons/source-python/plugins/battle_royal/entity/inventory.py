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
        return True if (self.player.total_weight - (item.weight * item.amount)) > 0 else False

    def _add_weight(self, item):
        self.player.total_weight -= (item.weight * item.amount)
        SayText2('2 ' + str(self.player.total_weight)).send()

    def _remove_weight(self, item):
        self.player.total_weight += (item.weight * item.amount)

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
            player_item = self._items[item.name]
            player_item.amount += item.amount
            self._items[item.name] = player_item

        self._add_weight(item)
        return True

    def _remove_item(self, item):
        del self._items[item.name]
        SayText2('Remove').send()

    def remove(self, item, amount=None):
        if not isinstance(item, Item):
            raise ValueError('Argument must be an Item')

        if item.name not in self._items:
            return False

        if amount is not None:
            if amount > item.amount:
                self._remove_item(item)
            else:
                item.amount -= amount
                if item.amount == 0:
                    self._remove_item(item)
                else:
                    self._items[item.name] = item
                    SayText2('Remove Amount').send()
        else:
            self._remove_item(item)

        self._remove_weight(item) 
