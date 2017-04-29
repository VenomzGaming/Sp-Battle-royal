## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .item import Item

class Care(Item):
    item_type = 'care'
    health = 0

    def _repeat(self):
        SayText2(str(self.health)).send()
        self._player.health += (self.health / 5)
        SayText2('+' + str(self.health / 5)).send()


    def use(self, player):
        self._player = player
        repeater = Repeat(self._repeat)
        repeater.start(1)
        Delay(5, repeater.stop)
        # Add config for tick repeat heal ?
        SayText2('Use care').send()