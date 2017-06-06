## IMPORTS

from colors import Color
from messages import SayText2

from ..config import _configs


## ALL DECLARATION

__all__ = (
    'FAIL_JUMP_FORCE',
    'StaminaCost',
    'Stamina',
)

## GLOBALS

# Add config to enable or not Stamina

INITIAL_STAMINA = _configs['stamina_amount'].get_int()
STAMINA_RESTORATION_RATE = _configs['restoration_rate'].get_int()
FAIL_JUMP_FORCE = -64

OVERLAY_PATH = "overlays/battle_royal/stamina-{}"


## CLASS

class StaminaCost:
    '''
        Class which define all stamina cost.
    '''
    SPRINT = _configs['sprint_cost'].get_int()
    JUMP = _configs['jump_cost'].get_int()


class Stamina:
    '''
        Class which manage the stamina system.
        :param BattleRoyalPlayer player:
            A player.
    '''

    def __init__(self, player):
        self._player = player
        self.stamina = 0
        self.stamina_ratio = 0

    def has_stamina_for(self, consumer):
        '''Check if has enought stamina.'''
        return self.stamina >= consumer

    def consume(self, consumer):
        '''Consume stamina.'''
        self.stamina -= consumer

        self.hud_check()

    def empty(self):
        '''Emptying stamina amount.'''
        self.stamina = 0
        self.hud_check()

    def refill(self):
        '''Refill the stamina.'''
        self.stamina = INITIAL_STAMINA
        self.hud_check()

    def restore(self):
        '''Regain stamina.'''
        if self.stamina < INITIAL_STAMINA:
            self.stamina = min(
                INITIAL_STAMINA, self.stamina + STAMINA_RESTORATION_RATE
            )

            self.hud_check()

    def hud_check(self):
        '''Update stamina HUD.'''
        new_ratio = int((self.stamina / INITIAL_STAMINA) * 10)
        if new_ratio == self.stamina_ratio:
            return

        self.stamina_ratio = new_ratio
        self._player.client_command('r_screenoverlay {}'.format(OVERLAY_PATH.format(new_ratio)))

