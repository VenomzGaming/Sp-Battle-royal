## IMPORTS

from messages import SayText2

from . import Item

class Ammo(Item):
    item_type = 'ammo'
    clip = 0
    ammo = 10


    def use(self):
        SayText2('Can\'t use').send()
