## IMPORTS


## ALL DECLARATION

__all__ = (
    'Inventory', 
)

## INVENTORY CLASS

class Inventory(set):
    '''
    Inventory is bound to client on the server
    and allows us to manage a "backpack" which
    can only store a maximum weight.
    :param Player player:
        Player to bind this inventory too.
    '''

    def __init__(self, owner, *args, **kwargs):
        'Specify the owner to bind this inventory too. Also can supply extra <list> args.'
        super(Inventory, self).__init__(*args, **kwargs)

        self.owner = owner
        self.max_weight = 20

    def add(self, item):
        'Overriden <set.add> to check if a inventory is too full.'
        if not self.can_pickup(item):
            return False

        super(Inventory, self).add(item)
        return True

    def discard(self, item, amount=None):
        'Overriden <set.discard> to check item amount.'
        if item.amount == 1:
            super(Inventory, self).discard(item)
        else:
            super(Inventory, self).discard(item)
            item.amount -= amount
            self.add(item)


    def can_pickup(self, item):
        'Checks if a inventory can pick up an item by calculating space available.'
        if item.weight > self.space:
            return False
        return True

    @property
    def weight(self):
        'Returns the current weight of the inventory.'
        return sum((item.weight * item.amount) for item in self)

    @property
    def space(self):
        'Returns the amount of space left in the inventory.'
        return self.max_weight - self.weight

    ## HELPERS

    def find_by_name(self, name):
        'Finds each item in the inventory by a name and iterates over them.'
        for item in self:
            if item.name == name:
                yield item
