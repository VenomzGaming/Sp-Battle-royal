## IMPORTS

from entities import TakeDamageInfo
from entities.entity import Entity
from entities.helpers import edict_from_index
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from events import Event
from filters.players import PlayerIter
from listeners.tick import Delay
from mathlib import Vector
from memory import make_object
from messages import SayText2
from players import UserCmd
from players.entity import Player
from players.helpers import index_from_userid, userid_from_pointer

from .config import _configs
from .entity.battleroyal import _battle_royal
from .entity.player import BattleRoyalPlayer
from .items.item import Item
from .utils.utils import BattleRoyalHud


# HIDEHUD_RADAR = 1 << 12


@Event('round_start')
def _on_round_start(event_data):
    SayText2('Round Start').send()
    _battle_royal.is_warmup = True
    for player in PlayerIter('alive'):
        br_player = BattleRoyalPlayer(player.index, 50)
        _battle_royal.add_player(br_player)

        # Hide entierly the radar 
        # hidehud = player.hidden_huds
        # if hidehud & HIDEHUD_RADAR:
        #     continue          
        # player.hidden_huds = hidehud | HIDEHUD_RADAR
    _battle_royal.warmup()
    Delay(_configs['waiting_match_begin'].get_int(), _battle_royal.start)


@Event('round_end')
def _on_round_end(event_data):
    _battle_royal.end()
    for player in PlayerIter('alive'):
        for weapon in player.weapons():
            player.drop_weapon(weapon.pointer, None, None)
    SayText2('Round End').send()


@Event('player_spawn')
def _on_player_spawn(event_data):
    player = Player(index_from_userid(event_data['userid']))


@Event('player_death')
def _on_kill_events(event_data):
    if event_data['attacker'] != 0:
        attacker = _battle_royal.get_player(Player(index_from_userid(event_data['attacker'])))

    victim = _battle_royal.get_player(Player(index_from_userid(event_data['userid'])))
    if victim is None:
        return

    # Add player to dead
    _battle_royal.remove_player(victim)
    _battle_royal.add_dead_player(victim)


@Event('player_connect')
def _on_player_connect(event_data):
    player = Player(index_from_userid(event_data['userid']))

    br_player = BattleRoyalPlayer(player.index, 50)
    if _battle_royal.match_begin:
        _battle_royal.add_dead_player(br_player)
    else:
        # Spawn player
        _battle_royal.add_player(br_player)

        

@Event('player_disconnect')
def _on_player_disconnect(event_data):
    player = Player(index_from_userid(event_data['userid']))
    br_player = _battle_royal.get_player(player)

    # Remove player from group
    if br_player.group is not None:
        group = br_player.group
        br_player.group.remove_player(br_player)
        br_player.group = None

        if len(group.players) == 0 and group.name in _battle_royal.teams:
            _battle_royal.remove_team(group)
            del group

    _battle_royal.remove_player(player)
    BattleRoyalHud.remove_player(player)
