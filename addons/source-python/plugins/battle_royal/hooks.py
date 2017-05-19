## IMPORTS

from commands import CommandReturn
from commands.client import ClientCommand

from engines.server import global_vars

from entities import TakeDamageInfo
from entities.entity import Entity
from entities.constants import DamageTypes
from entities.datamaps import InputData
from entities.helpers import edict_from_pointer
from entities.hooks import EntityPreHook, EntityPostHook, EntityCondition

from filters.players import PlayerIter

from listeners import OnTick, OnEntityCreated, OnEntityDeleted

import memory
from memory import make_object
from memory.hooks import PreHook

from messages import SayText2

from players.entity import Player
from players.helpers import index_from_userid, userid_from_index, userid_from_pointer

from weapons.entity import Weapon

from .entity.battleroyal import _battle_royal
from .entity.inventory import Inventory
from .globals import _authorize_weapon
from .items.item import Item
from .menus.backpack import backpack_menu
from .utils.utils import BattleRoyalHud, set_proximity_listening

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
    return CommandReturn.BLOCK


# TICK LISTENER

@OnTick
def _on_tick():
    if _battle_royal.is_warmup:
        BattleRoyalHud.warmup()

    if _battle_royal.match_begin: 
        BattleRoyalHud.match_info()

        # Find a way to hide question mark on radar
        for player in PlayerIter('alive'):
            set_proximity_listening(player)
            player.set_property_bool("m_bSpotted", False)
            BattleRoyalHud.player_weight(player)
    


@OnEntityDeleted
def _on_entity_delete(entity):
    item = _battle_royal.get_item_ent(entity)
    if item is None:
        return

    if isinstance(item, Inventory):
        SayText2(
            'Entity {} Inventory of {} has been removed !'.format(entity.index, item.player.name)
        ).send()
    else:
        SayText2(
            'Entity {} Item {} has been removed !'.format(entity.index, item.name.title())
        ).send()

    _battle_royal.remove_item_ent(entity)


# MANAGE HOOK

@EntityPreHook(EntityCondition.is_player, '_spawn')
def _on_spawn_players(stack):
    # pass
    if not _battle_royal.is_warmup or not _battle_royal.match_begin:
        return False

@EntityPreHook(EntityCondition.is_player, 'buy_internal')
def _on_buy(stack):
    return False

@EntityPreHook(EntityCondition.is_player, 'bump_weapon')
def _on_weapon_bump(stack):
    player = make_object(Player, stack[0])
    weapon = make_object(Entity, stack[1])
    if weapon.index not in _authorize_weapon:
        return False
    
    _authorize_weapon.remove(weapon.index)  


@EntityPreHook(EntityCondition.is_player, 'drop_weapon')
def _on_weapon_drop(stack):
    player = make_object(Player, stack[0])
    br_player = _battle_royal.get_player(player)
    try:
        entity = make_object(Entity, stack[1])
    except ValueError:
        return
    weapon_name = str(entity.classname).split('_')[1]
    if weapon_name == 'healthshot':
        item = Item.get_subclass_dict()[weapon_name.title()]()
        br_player.inventory.remove(item, 1)
        _battle_royal.add_player(br_player)
    else:
        return False


@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'use')
@EntityPreHook(lambda entity: entity.classname.startswith('weapon_'), 'use')
def _on_pick_up_item(stack):
    entity = make_object(Entity, stack[0])
    input_data = make_object(InputData, stack[1])
    player = make_object(Player, input_data.activator)

    if player is None or _battle_royal.match_begin != True or entity.index not in _battle_royal.items_ents:
        return

    br_player = _battle_royal.get_player(player)
    item = _battle_royal.get_item_ent(entity)
    
    if isinstance(item, Inventory):
        backpack_menu.entity = entity
        backpack_menu.backpack = item
        backpack_menu.send(player.index)
    else:
        SayText2('1 ' + str(br_player.total_weight)).send()
        success = br_player.pick_up(item)
        if success:
            SayText2('3 ' + str(br_player.total_weight)).send()
            entity.remove()

            if item.item_type == 'weapon':
                # Second param is used to set weapon ammo
                br_player.equip(item, True)
            elif item.item_type in ['ammo', 'armor', 'backpack']:
                br_player.equip(item)

            SayText2('4 ' + str(br_player.total_weight)).send()
            _battle_royal.add_player(br_player)
            SayText2('5 ' + str(br_player.total_weight)).send()
            SayText2(br_player.name + ' take item ' + item.name).send()


@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_damage_events(stack_data):
    take_damage_info = make_object(TakeDamageInfo, stack_data[1])

    if not take_damage_info.attacker:
        return

    if not _battle_royal.match_begin or _battle_royal.is_warmup:
        take_damage_info.damage = 0
        return

    entity = Entity(take_damage_info.attacker)
    attacker = _battle_royal.get_player(Player(entity.index)) if entity.is_player() else None
    victim = _battle_royal.get_player(make_object(Player, stack_data[0]))

    if attacker.group is not None and attacker.group == victim.group:
        take_damage_info.damage = 0
        SayText2('In your group !').send()
        return

    # Maybe add destroy armor before damaging player if sht is in head or body
    # if victim.armor > 0:
    #     take_damage_info.damage = victim.armor - take_damage_info.damage
    
    if victim.health - take_damage_info.damage <= 0:
        # Drop player backpack to be taken by another player
        entity = victim.drop_inventory()
        _battle_royal.add_item_ent(entity, victim.inventory)

    # Add hit marker on hit (maybe color in function of hit armor or health)
    BattleRoyalHud.hitmarker(attacker)
