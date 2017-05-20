## IMPORTS

from colors import Color
from messages import SayText2


## ALL DECLARATION

__all__ = (
    'FAIL_JUMP_FORCE',
    'StaminaCost',
    'Stamina',
)

## GLOBALS

# Add config to enable or not Stamina

INITIAL_STAMINA = 500 # Switch to config
STAMINA_RESTORATION_RATE = 1
FAIL_JUMP_FORCE = -64

OVERLAY_PATH = "overlays/battle_royal/stamina-{}"


## CLASS

class StaminaCost:
    SPRINT = 2
    JUMP = 100


class Stamina:
    def __init__(self, player):
        self.player = player
        self.stamina = 0
        self.stamina_ratio = 0

    def has_stamina_for(self, consumer):
        return self.stamina >= consumer

    def consume(self, consumer):
        self.stamina -= consumer

        self.hud_check()

    def empty(self):
        self.stamina = 0
        self.hud_check()

    def refill(self):
        self.stamina = INITIAL_STAMINA
        self.hud_check()

    def restore(self):
        if self.stamina < INITIAL_STAMINA:
            self.stamina = min(
                INITIAL_STAMINA, self.stamina + STAMINA_RESTORATION_RATE
            )

            self.hud_check()

    def hud_check(self):
        new_ratio = int((self.stamina / INITIAL_STAMINA) * 10)
        if new_ratio == self.stamina_ratio:
            return

        self.stamina_ratio = new_ratio
        self.player.client_command('r_screenoverlay {}'.format(OVERLAY_PATH.format(new_ratio)))

