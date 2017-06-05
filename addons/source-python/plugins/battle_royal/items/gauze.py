## IMPORTS

from engines.precache import Model
from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .care import Care


class Gauze(Care):
    name = 'Gauze'
    health = 10
    weight = 0.1
    model = Model('models/props/de_inferno/hr_i/concrete_bag_a/concrete_bag_a.mdl')


    def on_use(self, player):
        'Called upon the item being used.'
        self._player = player

        if not self.can_be_used():
            return False

        self._repeater = Repeat(self._repeat)
        self._repeater.start(0.5)
        Delay(3, self._repeater.stop)
        player.inventory.discard(self, 1)
        SayText2('Use care').send()
        
        return True
