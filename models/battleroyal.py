## IMPORTS

from entities.entity import Entity
from filters.players import PlayerIter

from .player import Player
from ..items import Item

## ALL DECLARATIONS

__all__ = (
    'BattleRoyal',
    '_battle_royal',
)


class BattleRoyal:

    def __init__(self):
        self.status = False
        self._items_ents = dict()
        self._players_backpack_ents = dict()
        self._players = dict()
        self._teams = dict()
        self._dead_players = dict()

    @property
    def teams(self):
        return self._teams   

    @property
    def items_ents(self):
        return self._items_ents   

    def get_item_ent(self, entity):
        return self._items_ents[entity.index] if entity.index in self._items_ents else None

    def add_item_ent(self, entity, item):
        self._items_ents[entity.index] = item

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


    def spawn_item(self):
        # Get all location of item in file maybe, random spawn item. Number of items depend on player and rarity of item add this attribute to item
        # for index, item in self._items_ents.items():
        #     entity = item.create(location)
        #     self.add_item_ent(entity)
        pass

    def spawn_players(self):
        # For the moment spawn player in random spawn on map (After spawn user with parachute)
        pass

    def spread_gas(self):
        # Get random radius and gas the rest (Wave of gas depend on map maybe, 3 min)
        pass

    def warmup(self):
        # Maybe implement the warmup directly in map. A waiting for 30s (god mod player) before begining of the round
        self.status = False
        pass

    def start(self):
        self.spawn_item()
        self.spawn_players()
        self.status = True
        # Add repeater to spread gas

    def end(self):
        self.status = False

        # Remove all spawned entities
        for index, item in self._items_ents.items():
            Entity(index).remove()

        self._items_ents.clear()

        # Remove all spawned backpack entities
        for index, item in self._players_backpack_ents.items():
            Entity(index).remove()

        self._players_backpack_ents.clear()

        # Clear dict
        self._players.clear()
        self._teams.clear()
        self._dead_players.clear()
        

## GLOBALS

_battle_royal = BattleRoyal()