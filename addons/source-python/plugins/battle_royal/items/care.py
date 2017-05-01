## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .item import Item

class Care(Item):
    item_type = 'care'
    health = 0

    def _repeat(self):
        add_health = self.health // 5
        if self._player.health + add_health > 100:
            self._player.health = 100
            self._repeater.stop()
            return

        self._player.health += add_health

    def use(self, player):
        self._player = player
        self._repeater = Repeat(self._repeat)
        self._repeater.start(1)
        Delay(6, self._repeater.stop)
        SayText2('Use care').send()
        return True
