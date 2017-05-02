## IMPORTS

from entities import TakeDamageInfo
from entities.entity import Entity
from entities.helpers import edict_from_index
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from events import Event
from filters.players import PlayerIter
from mathlib import Vector
from memory import make_object
from messages import SayText2
from players import UserCmd
from players.entity import Player
from players.helpers import index_from_userid, userid_from_pointer

from .entity.battleroyal import _battle_royal
from .entity.player import BattleRoyalPlayer
from .items.item import Item
from .utils.utils import BattleRoyalHud


# HIDEHUD_RADAR = 1 << 12


@Event('round_announce_warmup')
def _on_warmup_start(event_data):
    SayText2('Warmup Begin').send()
    # _battle_royal.warmup()


@Event('round_start')
def _on_round_start(event_data):
    SayText2('Round Start').send()

    for player in PlayerIter('alive'):
        br_player = BattleRoyalPlayer(player.index, 50)
        _battle_royal.add_player(br_player)

        # Hide entierly the radar 
        # hidehud = player.hidden_huds
        # if hidehud & HIDEHUD_RADAR:
        #     continue          
        # player.hidden_huds =  hidehud | HIDEHUD_RADAR

    _battle_royal.start()


@Event('round_end')
def _on_round_end(event_data):
    _battle_royal.end()
    SayText2('Round End').send()


@Event('player_spawn')
def _on_player_spawn(event_data):
    player = Player(index_from_userid(event_data['userid']))


@Event('player_death')
def _on_kill_events(event_data):
    if event_data['attacker'] != 0:
        attacker = _battle_royal.get_player(Player(index_from_userid(event_data['attacker'])))
        # SayText2('Attacker : ' + str(attacker.userid)).send()

    victim = _battle_royal.get_player(Player(index_from_userid(event_data['userid'])))
    SayText2('Victim : ' + str(victim.userid)).send()

    # Add player to dead
    _battle_royal.remove_player(victim)
    _battle_royal.add_dead_player(victim)

    # assister = None
    # if event_data['assister']:
    #     assister = _battle_royal.get_player(Player(index_from_userid(event_data['assister'])))

    # if assister:
    #     pass

    # Drop player backpack to be taken by another player
    entity = victim.drop_inventory()
    _battle_royal.add_item_ent(entity, victim.inventory)

@Event('player_disconnect')
def _on_player_disconnect(event_data):
    player = Player(index_from_userid(event_data['userid']))
    _battle_royal.remove_player(player)
    BattleRoyalHud.remove_player(player)
