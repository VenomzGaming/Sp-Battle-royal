## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .care import Care


class Gauze(Care):
    name = 'Gauze'
    health = 10
    weight = 1
    models = 'models/props/props_crates/wooden_crate_32x64.mdl'

    def _repeat(self):
        self._player.health += self.health // 5

    def use(self, player):
        self._player = player
        repeater = Repeat(self._repeat)
        repeater.start(0.5)
        Delay(3, repeater.stop)
        # Add config for tick repeat heal ?
        SayText2('Use care').send()
