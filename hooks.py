## IMPORTS

from commands import CommandReturn
from commands.client import ClientCommand
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.datamaps import InputData
from entities.helpers import edict_from_pointer
from entities.hooks import EntityPreHook, EntityPostHook, EntityCondition
from filters.players import PlayerIter
from memory import make_object
from messages import SayText2
from players.entity import Player
from players.helpers import index_from_userid, userid_from_index, userid_from_pointer

from .models.battleroyal import _battle_royal
from .items import Item

## GLOBALS

_authorize_weapon = []

## MANAGE TEAM

@ClientCommand('joingame')
def _on_join_game(command, index):
    player = Player(index)
    team_t = len(PlayerIter('t'))
    team_ct = len(PlayerIter('ct'))

    if team_t > team_ct:
        player.team = 3
    else:
        player.team = 2
    return CommandReturn.BLOCK


@ClientCommand('jointeam')
def _on_join_team(command, index):
    SayText2('Can\'t Switch').send()
    return CommandReturn.BLOCK


# MANAGE HOOK

@EntityPreHook(EntityCondition.is_human_player, 'bump_weapon')
def _on_weapon_bump(stack):
    weapon = make_object(Entity, stack[1])
    if weapon.index not in _authorize_weapon:
        return False
    
    _authorize_weapon.remove(weapon.index)     


@EntityPreHook(EntityCondition.is_human_player, 'drop_weapon')
def _on_weapon_drop(stack):
    pass
    # player = make_object(Player, stack[0])
    # entity = make_object(Entity, stack[1])
    # brPlayer = _battle_royal.get_player[player.userid]
    # SayText2(str(entity.classname)).send()
    # item = _battle_royal.get_item_ent[entity.index]
    # brPlayer.drop(item)


def on_item_given(player, item):
    SayText2('Player {} has got {} !'.format(player.name, item.classname)).send()

@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'use')
@EntityPreHook(lambda entity: entity.classname.startswith('weapon_'), 'use')
def _on_pick_up_item(stack):
    entity = make_object(Entity, stack[0])
    input_data = make_object(InputData, stack[1])
    player = make_object(Player, input_data.activator)

    if player is None or _battle_royal.status != True or entity.index not in _battle_royal.items_ents:
        return

    br_player = _battle_royal.get_player(player)
    item = _battle_royal.get_item_ent(entity)
    success = br_player.pick_up(item)
    SayText2(str(success)).send()

    if success:
        entity.remove()
        # Refactor item code to make all items call by one function
        item.equip(br_player, on_item_given)
        SayText2('Take ' + br_player.name).send()


@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_damage_events(stack_data):
    # Add hit marker on hit
    pass
            