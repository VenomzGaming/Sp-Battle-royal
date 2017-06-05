## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .care import Care


class Medikit(Care):
    name = 'Medic Kit'
    health = 50
    weight = 0.5


    def on_use(self, player):
        'Called upon the item being used.'
        self._player = player

        if not self.can_be_used():
            return False

        self._repeater = Repeat(self._repeat)
        self._repeater.start(1)
        Delay(6, self._repeater.stop)
        player.inventory.discard(self, 1)
        SayText2('Use care').send()
        
        return True
