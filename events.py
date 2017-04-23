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

from .models.battleroyal import _battle_royal
from .models.player import Player as BrPlayer
from .items.item import Item

HIDEHUD_RADAR = 1 << 12
# HIDEHUD_RADAR = 1 << 8


@Event('round_announce_warmup')
def _on_warmup_start(event_data):
    SayText2('Warmup Begin').send()
    # _battle_royal.warmup()


@Event('round_start')
def _on_round_start(event_data):
    SayText2('Round Start').send()

    # ak = Ak47()
    # entity = ak.create(Vector(213.62831115722656, 799.6934204101562, 0.03125))
    # _battle_royal.add_item_ent(entity, ak)

    SayText2(str(Item.get_subclass_dict())).send()
    # for cls in Item.get_subclass_dict().values():
    #     SayText2(str(cls)).send()
    #     SayText2(str(cls.get_subclass_dict())).send()
    

    for player in PlayerIter('alive'):
        brPlayer = BrPlayer(player.index, 50)
        _battle_royal.add_player(brPlayer)
        # _battle_royal.spawn_item(brPlayer)

        # edict = edict_from_index(player.index)
        # # Hide ennemy on radar 
        # hidehud = edict.get_property_int('m_iHideHud')
        # if hidehud & HIDEHUD_RADAR:
        #     continue          
        # edict.set_property_int('m_iHideHud', hidehud | HIDEHUD_RADAR)

    _battle_royal.start()


@Event('round_end')
def _on_round_end(event_data):
    _battle_royal.end()
    SayText2('Round End').send()


@Event('player_death')
def _on_kill_events(event_data):
    if event_data['userid'] == 0:
        return

    attacker = _battle_royal.get_player(Player(index_from_userid(event_data['attacker'])))
    victim = _battle_royal.get_player(Player(index_from_userid(event_data['userid'])))

    # Add player to dead
    _battle_royal.remove_player(victim)
    _battle_royal.add_dead_player(victim)

    assister = None
    if event_data['assister']:
        assister = _battle_royal.get_player(Player(index_from_userid(event_data['assister'])))

    if assister:
        pass

    # Drop player backpack to be taken by another player
    victim.drop_inventory()

