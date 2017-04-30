## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .item import Item

class Care(Item):
    item_type = 'care'
    health = 0

    def _repeat(self):
        self._player.health += self.health // 5


    def use(self, player):
        self._player = player
        repeater = Repeat(self._repeat)
        repeater.start(1)
        Delay(6, repeater.stop)
        SayText2('Use care').send()
