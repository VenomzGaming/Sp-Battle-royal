## IMPORTS

from random import choice

from core import echo_console
from engines.precache import Model

from entities.constants import MoveType
from entities.entity import Entity

from filters.entities import BaseEntityIter
from filters.players import PlayerIter

from listeners import OnTick
from listeners.tick import Delay

from mathlib import Vector

from messages import SayText2

from players.constants import PlayerStates, PlayerButtons
from players.entity import Player


from .. import globals
from ..config import _configs


## DECLARATION

__all__ = (
    'Parachute',
    # 'parachute',
)

class Parachute:

    _models = [
        Model('models/parachute/parachute_blue.mdl'),
        Model('models/parachute/parachute_carbon.mdl'),
        Model('models/parachute/parachute_green_v2.mdl'),
        Model('models/parachute/parachute_ice_v2.mdl')
    ]

    def __init__(self):
        self._enable = False
        self._parachutes = {}

    def set_enable(self, state):
        self._enable = state

    def get_enable(self):
        return self._enable

    enable = property(get_enable, set_enable)

    @property
    def parachutes(self):
        return self._parachutes

    def open(self, player):
        entity = Entity.create('prop_dynamic_override')
        entity.model = choice(self._models)
        entity.teleport(player.origin, player.angles, None)
        entity.spawn()

        self._parachutes[player.userid] = (player, entity)

    def close(self, player):
        self._parachutes.pop(player.userid)[1].remove()

    def disable(self):
        for player, entity_parachute in self.parachutes.values():
            entity_parachute.remove()
        self._parachutes.clear()
        self._enable = False



globals.parachute = Parachute()

## TICK LISTENER

@OnTick
def _on_tick_listener():
    try:
        if not globals.parachute.enable:
            for player in PlayerIter('alive'):
                if player.stuck: 
                    for entity in BaseEntityIter('info_deathmatch_spawn'):
                        vector = entity.get_key_value_vector('origin')
                        break
                    player.origin = vector
            return

        # Teleport existing parachutes to their owners
        for player, entity_parachute in globals.parachute.parachutes.values():
            entity_parachute.teleport(player.origin, player.angles, None)

        for player in PlayerIter('alive'):
            velocity = player.fall_velocity 

            if (velocity < 1.0 or player.move_type & MoveType.LADDER or player.flags & PlayerStates.INWATER or player.buttons & PlayerButtons.JUMP):
                if player.userid in globals.parachute.parachutes:
                    globals.parachute.close(player)
                continue

            # Revert the falling velocity to slow down the player speed...
            player.base_velocity = Vector(0, 0, velocity + (_configs['parachute_falling_speed'].get_float() * -1))

            if player.userid not in globals.parachute.parachutes:
                globals.parachute.open(player)
    except Exception as e:
        echo_console(str(e))

