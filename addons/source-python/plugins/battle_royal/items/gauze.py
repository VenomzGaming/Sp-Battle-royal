## IMPORTS

from listeners.tick import Delay, Repeat, RepeatStatus
from messages import SayText2

from .care import Care


class Gauze(Care):
    name = 'Gauze'
    health = 10
    weight = 1
    # models = 'models/props/props_crates/wooden_crate_32x64.mdl'
    models = 'models/props/de_inferno/hr_i/concrete_bag_a/concrete_bag_a.mdl'

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
        self._repeater.start(0.5)
        Delay(3, self._repeater.stop)
        # Add config for tick repeat heal ?
        SayText2('Use care').send()
        return True
