## IMPORTS

import random

from engines.server import global_vars
from entities.entity import Entity
from filters.players import PlayerIter
from listeners.tick import Delay
from messages import SayText2
from mathlib import Vector

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
        self._players_backpack_ents = dict()
        self._players = dict()
        self._dead_players = dict()
        self._teams = dict()
        self._gas_wave = []

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
    def players_backpack_ents(self):
        return self._players_backpack_ents   

    def get_player_backpack_ent(self, entity):
        return self._players_backpack_ents[entity.index] if entity.index in self._players_backpack_ents else None

    def add_player_backpack_ent(self, entity):
        self._players_backpack_ents[entity.index] = entity

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

    @property
    def gas(self):
        return self._gas_wave  


    def _god_mode(self, enable):
        for br_player in self._players.values():
            br_player.godmode = enable

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
        # For the moment spawn player in random spawn on map (After spawn user with parachute)
        pass
        # globals.players_spawn_manager = SpawnManager('player', global_vars.map_name)
        # locations = globals.players_spawn_manager.locations
        # for player in self._players.values():
        #     parachute.open(player)
        #     vector = random.choice(locations)
        #     player.origin = vector
        #     locations.remove(vector)

    def spread_gas(self):
        # Get random radius and gas the rest (Wave of gas depend on map maybe, 3 mini)
        # Maybe create a listener 
        start = _configs['time_before_spreading'].get_int()
        waiting = _configs['time_between_spreading'].get_int()

        wave_one = Gas()
        wave_one.spread(start)
        self._gas_wave.append(wave_one)
        start += waiting

        wave_two = Gas()
        wave_two.spread(start)
        self._gas_wave.append(wave_two)
        start += waiting

        wave_three = Gas()
        wave_three.spread(start)
        self._gas_wave.append(wave_three)

    def warmup(self):
        self.is_warmup = True
        self._god_mode(True)
        # from engines.precache import Model
        # heli = Entity.create('prop_dynamic')
        # location = Vector(637.66650390625, 322.892578125, 256.03125)
        # heli.origin = location
        # heli.model = Model('models/props_vehicles/helicopter_rescue.mdl')
        # heli.solid_type = 6
        # heli.spawn()

    def start(self):
        SayText2('Match start !').send()
        self.is_warmup = False
        self.match_begin = True
        self._god_mode(False)

        self.spawn_item()
        self.spawn_players()

        if bool(_configs['parachute_enable'].get_int()):
            parachute.enable = True
            Delay(_configs['parachute_duration'].get_int(), parachute.disable)
        else:
            parachute.enable = False

        # Add repeater to spread gas
        # self.spread_gas()

    def end(self):
        self.match_begin = False
        self.is_warmup = False
        parachute.enable = False

        # Remove all spawned entities
        SayText2('SPAWNED ENT : ' + str(self._items_ents)).send()
        all_entities = self._items_ents.copy()
        for index, item in all_entities.items():
            SayText2('Index : ' + str(index)).send()
            Entity(index).remove()

        # self._items_ents.clear()

        # Remove all spawned backpack entities
        # SayText2(str(self._players_backpack_ents)).send()
        for index, item in self._players_backpack_ents.items():
            Entity(index).remove()

        self._players_backpack_ents.clear()

        # Remove gas
        for gas in self._gas_wave:
            gas.stop()

        # Clear dict and list
        self._players.clear()
        self._teams.clear()
        self._dead_players.clear()
        self._gas_wave.clear()
        
## GLOBALS

_battle_royal = BattleRoyal()
