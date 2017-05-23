## IMPORTS

from engines.trace import engine_trace
from engines.trace import ContentMasks
from engines.trace import GameTrace
from engines.trace import Ray
from engines.trace import TraceFilterSimple

from entities.constants import WORLD_ENTITY_INDEX
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.helpers import edict_from_index
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook

from events import Event

from filters.entities import BaseEntityIter, EntityIter
from filters.players import PlayerIter

from listeners import OnLevelInit
from listeners.tick import Delay

from mathlib import Vector

from memory import make_object

from messages import SayText2

from players import UserCmd
from players.entity import Player
from players.helpers import index_from_userid, userid_from_pointer


from . import globals
from .config import _configs

from .entity.battleroyal import _battle_royal
from .entity.player import BattleRoyalPlayer
from .entity.stamina import StaminaCost, FAIL_JUMP_FORCE
from .entity.score import Score

from .items.item import Item

from .utils.spawn_manager import SpawnManager
from .utils.utils import BattleRoyalHud, set_proximity_listening, get_map_height


## GLOBALS
info_map_parameters = None


## EVENTS

@OnLevelInit
def _on_level_init(map_name):
    #  Not sure about maybe just load it on level init
    # globals.items_spawn_manager = SpawnManager('item', map_name)
    # globals.players_spawn_manager = SpawnManager('player', map_name)
    globals.MAP_HEIGHT = get_map_height()


@Event('player_connect_full')
def _on_player_connect(event_data):
    if event_data['index'] == 0:
        return

    player = Player(event_data['index'])

    br_player = BattleRoyalPlayer(player.index, 50)
    if _battle_royal.match_begin:
        _battle_royal.add_dead_player(br_player)
    else:
        # Spawn player
        _battle_royal.add_player(br_player)
        

@Event('player_disconnect')
def _on_player_disconnect(event_data):
    br_player = _battle_royal.get_player(event_data['userid'])
    if br_player is None:
        br_player = _battle_royal.get_dead_player(event_data['userid'])

    if br_player is None:
        return

    # Remove player from group
    if hasattr(br_player, 'group') and br_player.group is not None:
        group = br_player.group
        br_player.group.remove_player(br_player)
        br_player.group = None

        if len(group.players) == 0 and group.name in _battle_royal.teams:
            _battle_royal.remove_team(group)
            del group

    BattleRoyalHud.remove_player(br_player)

    if br_player.dead:
        _battle_royal.remove_dead_player(br_player)
    else:
        _battle_royal.remove_player(br_player)


@Event('round_start')
def _on_round_start(event_data):
    # for player in PlayerIter('human'):
    #     br_player = BattleRoyalPlayer(player.index, 50)
    #     _battle_royal.add_player(br_player)
    
    info_map_parameters = Entity.find_or_create("info_map_parameters")

    _battle_royal.warmup()
    Delay(_configs['waiting_match_begin'].get_int(), _battle_royal.start)


@Event('round_end')
def _on_round_end(event_data):
    _battle_royal.end()
    for player in PlayerIter('alive'):
        for weapon in player.weapons():
            player.drop_weapon(weapon.pointer, None, None)
        player.primary = None
        player.secondary = None


@Event('player_spawn')
def _on_player_spawn(event_data):
    if event_data['userid'] == 0:
        return

    try:
        player = _battle_royal.get_player(event_data['userid'])
        if hasattr(player, 'stamina'):
            player.stamina.refill()
    except:
        pass


@Event('player_jump')
def on_player_jump(event_data):
    player = _battle_royal.get_player(event_data['userid'])
    
    if player is None:
        return

    if hasattr(player, 'stamina'):
        if player.stamina.has_stamina_for(StaminaCost.JUMP):
            player.stamina.consume(StaminaCost.JUMP)
        else:
            player.stamina.player.push(1, FAIL_JUMP_FORCE, vert_override=True)
            player.stamina.empty()


@Event('player_death')
def _on_player_death(event_data):
    attacker = None
    if event_data['attacker'] != 0:
        attacker = _battle_royal.get_player(event_data['attacker'])

    assister = None
    if event_data['assister']:
        assister = _battle_royal.get_player(event_data['assister'])

    victim = _battle_royal.get_player(event_data['userid'])
    if victim is None:
        return

    # Set score
    if assister is not None:
        assister.br_score.set_score(assist=True)

    if attacker is not None:
        attacker.br_score.set_score(headshot=event_data['headshot'])


    # Add player to dead
    _battle_royal.remove_player(victim)
    _battle_royal.add_dead_player(victim)

    # Update additionnal score
    Score.additional_score += _configs['additional_score'].get_int()

    # Ending match
    end = False
    if len(_battle_royal.teams) != 0:
        last_team = []
        for player in _battle_royal.players:
            if player.group not in last_team:
                last_team.append(player.group)

        if len(last_team) == 1:
            end = True
    else:
        if len(_battle_royal.players) == 1:
            end = True

    if end:
        # Check if round_end is fired
        BattleRoyalHud.winner()
