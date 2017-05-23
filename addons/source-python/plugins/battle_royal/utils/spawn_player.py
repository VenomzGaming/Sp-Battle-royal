## IMPORTS

import random


from mathlib import Vector

from players.constants import LifeState


from .. import globals

from ..config import _configs

## ALL DECLARATION

__all__ = (
    'SpawnType',
    'SpawnPlayer',
)


## CLASS


class SpawnType:
    ON_GOUND = 0
    IN_SKY = 1
    IN_HELI = 2
    

class SpawnPlayer:

    def __init__(self, players, locations, spawn_type):
        self._players = players
        self._locations = locations
        self._spawn_type = spawn_type

    def spawn(self):
        if self._spawn_type == SpawnType.IN_HELI:
            if not globals.parachute.enable:
                globals.parachute.enable = True
            self._spawn_in_heli()              
        else:
            self._random_spawn() 
        
        
    def _respawn_all_player(self, all_locations):
        for player in self._players.values():
            # Add check if player is in group and spawn his mate near him
            vector = random.choice(all_locations)

            if self._spawn_type == SpawnType.IN_SKY:
                player.origin = Vector(vector.x, vector.y, (globals.MAP_HEIGHT-150))
            else:
                player.origin = vector

            player.player_state = 0
            player.life_state = LifeState.ALIVE
            player.health = 100
            player.spawn()
            all_locations.remove(vector) 

            if self._spawn_type == SpawnType.IN_SKY:
                globals.parachute.open(player)

    def _spawn_in_heli(self):
        pass

    def _random_spawn(self):
        if self._spawn_type == SpawnType.IN_SKY:
            if not globals.parachute.enable:
                globals.parachute.enable = True
        else:
            globals.parachute.enable = False
        
        self._respawn_all_player(self._locations)