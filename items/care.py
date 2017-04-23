## IMPORTS

from messages import SayText2

from .item import Item

class Care(Item):
    item_type = 'care'
    health = 0

    def use(self):
        SayText2('Can\'t use').send()