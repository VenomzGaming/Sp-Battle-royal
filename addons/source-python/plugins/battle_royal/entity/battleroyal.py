## IMPORTS

import random

from engines.server import global_vars
from entities.entity import BaseEntity, Entity
from filters.entities import BaseEntityIter, EntityIter
from filters.players import PlayerIter
from listeners.tick import Delay
from mathlib import Vector
from messages import SayText2
from players.constants import LifeState


from .player import BattleRoyalPlayer
from .gas import Gas
from .. import globals
from ..config import _configs
from ..items.item import Item
from ..utils.spawn_manager import SpawnManager
from ..utils.parachute import parachute

## ALL DECLARATIONS

__all__ = (
    'BattleRoyal',
    '_battle_royal'
)


class BattleRoyal:

    def __init__(self):
        self.is_warmup = False
        self.match_begin = False
        self._items_ents = dict()
        self._players = dict()
        self._dead_players = dict()
        self._teams = dict()

    @property
    def teams(self):
        return self._teams

    def get_team(self, team):
        return self._teams[team.name] if team.name in self._teams else None

    def add_team(self, team):
        self._teams[team.name] = team

    def remove_team(self, team):
        del self._teams[team.name] 

    @property
    def items_ents(self):
        return self._items_ents   

    def get_item_ent(self, entity):
        return self._items_ents[entity.index] if entity.index in self._items_ents else None

    def add_item_ent(self, entity, item):
        self._items_ents[entity.index] = item

    def remove_item_ent(self, entity):
        del self._items_ents[entity.index]

    @property
    def players(self):
        return self._players   

    def get_player(self, player):
        return self._players[player.userid] if player.userid in self._players else None

    def add_player(self, player):
        self._players[player.userid] = player

    def remove_player(self, player):
        del self._players[player.userid]

    @property
    def deads(self):
        return self._dead_players   

    def get_dead_player(self, player):
        return self._dead_players[player.userid] if player.userid in self.deads else None

    def add_dead_player(self, player):
        self._dead_players[player.userid] = player

    def _god_mode_noblock(self, enable):
        for br_player in self._players.values():
            br_player.godmode = enable
            br_player.noblock = enable

    def spawn_item(self):
        # Get all location of item in file maybe, random spawn item. Number of items depend on player and rarity of item add this attribute to item
        globals.items_spawn_manager = SpawnManager('item', global_vars.map_name)
        locations = globals.items_spawn_manager.locations
        if len(locations) != 0:
            for classname, cls in Item.get_subclass_dict().items():
                if len(locations) == 0:
                    break
                if classname in ['WeaponItem', 'Ammo', 'Armor', 'Care']:
                    continue

                item = cls()
                vector = random.choice(locations)
                entity = item.create(vector)
                locations.remove(vector)
                _battle_royal.add_item_ent(entity, item)
        else:
            SayText2('Any spawn point on this map.').send()
    
    def spawn_players(self):
        self._random_spawn(1)
        # pass
        # spawn_type = _configs['spawn_player_type'].get_int()
        # if spawn_type == 0 or spawn_type == 1:
        #     self._random_spawn(spawn_type)     
        # else:
        #     if not parachute.enable:
        #         parachute.enable = True
        #     self._spawn_in_heli() 

    def _respawn_all_player(self, locations, type_spawn):
        for player in self._players.values():
            # Add check if player is in group and spawn his mate near him
            vector = random.choice(locations)
            SayText2(str(vector)).send()

            if type_spawn == 1:
                player.origin = Vector(vector.x, vector.y, (globals.MAP_HEIGHT-200))
            else:
                player.origin = vector

            player.player_state = 0
            player.life_state = LifeState.ALIVE
            player.health = 100
            player.spawn()
            locations.remove(vector) 

            if type_spawn == 1:
                parachute.open(player)

    def _spawn_in_heli(self):
        pass

    def _random_spawn(self, type_spawn):
        # Check if mp_randomspawn is set to 1
        locations = None
        if type_spawn == 1:
            globals.players_spawn_manager = SpawnManager('player', global_vars.map_name)
            locations = globals.players_spawn_manager.locations

            if not parachute.enable:
                parachute.enable = True

            if len(locations) == 0:
                locations = [
                    entity.get_key_value_vector('origin') for entity in BaseEntityIter('info_deathmatch_spawn')
                ]
        else:
            locations = [
                entity.get_key_value_vector('origin') for entity in BaseEntityIter('info_deathmatch_spawn')
            ]

            self._respawn_all_player(locations, type_spawn)

    def spread_gas(self):
        # Get random radius and gas the rest (Wave of gas depend on map maybe, 3 mini)
        # Maybe create a listener to start another gas spreading after the end of the following
        start = _configs['time_before_spreading'].get_int()
        waiting = _configs['time_between_spreading'].get_int()

        wave_one = Gas()
        wave_one.spread(start)

    def warmup(self):
        SayText2('Here').send()
        self.is_warmup = True
        self._random_spawn(0)
        self._god_mode_noblock(True)

    def start(self):
        SayText2('Match start !').send()
        self.is_warmup = False
        self.match_begin = True
        self._god_mode_noblock(False)

        if bool(_configs['parachute_enable'].get_int()):
            parachute.enable = True
            Delay(_configs['parachute_duration'].get_int(), parachute.disable)
        else:
            parachute.enable = False

        self.spawn_item()
        self.spawn_players()

        # Add repeater to spread gas
        # self.spread_gas()

    def end(self):
        self.match_begin = False
        self.is_warmup = False
        parachute.enable = False

        # Remove all spawned entities
        Delay(1, self._remove_items)

        # Clear dict and list
        self._players.clear()
        self._teams.clear()
        self._dead_players.clear()

    def _remove_items(self):
        all_entities = self._items_ents.copy()
        for index, item in all_entities.items():
            Entity(index).remove()

        self._items_ents.clear()

        
## GLOBALS

_battle_royal = BattleRoyal()
