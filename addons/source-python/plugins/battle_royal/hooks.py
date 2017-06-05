## IMPORTS

from commands import CommandReturn
from commands.client import ClientCommand

from engines.server import global_vars

from entities import TakeDamageInfo, CheckTransmitInfo
from entities.entity import Entity
from entities.constants import DamageTypes, INVALID_ENTITY_INTHANDLE
from entities.datamaps import InputData
from entities.helpers import edict_from_pointer, index_from_inthandle, index_from_pointer
from entities.hooks import EntityPreHook, EntityPostHook, EntityCondition

from filters.players import PlayerIter

from listeners import OnTick, OnEntityCreated, OnEntityDeleted

import memory
from memory import make_object
from memory.hooks import PreHook

from messages import SayText2

from players import UserCmd
from players.constants import PlayerButtons
from players.entity import Player
from players.helpers import index_from_userid, userid_from_index, userid_from_pointer, userid_from_edict


from weapons.entity import Weapon

from .entity.battleroyal import _battle_royal
from .entity.inventory import Inventory
from .entity.sprint import SPRINT_START_SOUND, LOW_STAMINA_SOUND, SPRINTING_PLAYER_SPEED, DEFAULT_PLAYER_SPEED
from .entity.stamina import StaminaCost

from .globals import _authorize_weapon

from .items.item import Item, items

from .menus.backpack import backpack_menu

from .utils.utils import BattleRoyalHud, set_proximity_listening

## MANAGE TEAM

@ClientCommand('joingame')
def _on_join_game(command, index):
    'Force join team'
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
    'Block join team command'
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
            br_player = _battle_royal.get_player(player.userid)
            br_player.stamina.restore()


# @OnEntityDeleted
# def _on_entity_delete(entity):
#     item = _battle_royal.get_item_ent(entity)
#     if item is None:
#         return

#     # if isinstance(item, Inventory):
#     #     SayText2(
#     #         'Entity {} Inventory of {} has been removed !'.format(entity.index, item.player.name)
#     #     ).send()
#     # else:
#     #     SayText2(
#     #         'Entity {} Item {} has been removed !'.format(entity.index, item.name.title())
#     #     ).send()

#     _battle_royal.remove_item_ent(entity)


# MANAGE HOOK

@EntityPreHook(EntityCondition.is_player, '_spawn')
def _on_spawn_players(stack):
    pass
    # if not _battle_royal.is_warmup or not _battle_royal.match_begin:
    #     return False


@EntityPreHook(EntityCondition.is_player, 'buy_internal')
def _on_buy(stack):
    'Block buy command.'
    return False


@EntityPreHook(EntityCondition.is_player, 'bump_weapon')
def _on_weapon_bump(stack):
    'Override default bump_weapon to used only <use> input to pick weapon.'
    player = make_object(Player, stack[0])
    weapon = make_object(Entity, stack[1])
    if weapon.index not in _authorize_weapon:
        return False
    
    _authorize_weapon.remove(weapon.index)  


@EntityPreHook(EntityCondition.is_player, 'drop_weapon')
def _on_weapon_drop(stack):
    'Manage dropped weapon from invenentory.'
    player = make_object(Player, stack[0])
    br_player = _battle_royal.get_player(player)

    try:
        entity = make_object(Entity, stack[1])
    except ValueError:
        return

    if entity.classname != 'weapon_healthshot':
        return False

    item = items.find_by_index(entity.index)
    if item:
        item.on_dropped(br_player)


@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'use')
@EntityPreHook(lambda entity: entity.classname.startswith('weapon_'), 'use')
def _on_pick_up_item(stack):
    'Add items to the inventory which have a <use> input.'
    entity = make_object(Entity, stack[0])
    input_data = make_object(InputData, stack[1])
    player = make_object(Player, input_data.activator)
    item = items.find_by_index(entity.index)

    if player is None or _battle_royal.match_begin != True or item is None:
        return

    br_player = _battle_royal.get_player(player)
    
    if isinstance(item, Inventory):
        backpack_menu.entity = entity
        backpack_menu.backpack = item
        backpack_menu.send(player.index)
    else:
        if item.on_pickup(br_player):
            SayText2(br_player.name + ' take item ' + item.name).send()
        else:
            SayText2(br_player.name + ' can\'t take item ' + item.name).send()


# @EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'set_transmit')
# @EntityPreHook(lambda entity: entity.classname.startswith('weapon_'), 'set_transmit')
# def _set_transmit(stack):
#     info = memory.make_object(CheckTransmitInfo, stack[1])
#     userid = userid_from_edict(info.client)
#     entity_index = index_from_pointer(stack[0])
#     item = items.find_by_index(entity_index)
#     if item is None and item.entity is None:
#         return

#     br_player = _battle_royal.get_player(userid)
#     if br_player is None:
#         return

#     if br_player.origin.get_distance(item.entity.origin) <= 50:
#         # Orage color
#         orange = 255*65536+165*256+0
#         item.entity.set_property_bool('m_bShouldGlow', True)
#         item.entity.set_property_int('m_clrGlow', orange)
#         item.entity.set_property_float('m_flGlowMaxDist', 50) 


@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_damage_events(stack_data):
    'Avoid damaging group member and override damage system.'
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

    # Maybe add destroy armor before damaging player if hitgroup is head or body
    # if victim.armor > 0:
    #     take_damage_info.damage = victim.armor - take_damage_info.damage
    
    if victim.health - take_damage_info.damage <= 0:
        entity = victim.drop_inventory()
        _battle_royal.add_item_ent(entity, victim.inventory)

    # Add hit marker on hit (maybe color in function of hit armor or health)
    BattleRoyalHud.hitmarker(attacker)


# @EntityPreHook(EntityCondition.is_human_player, 'run_command')
# def pre_player_run_command(stack_data):
#     if not _battle_royal.match_begin:
#         return

#     userid = userid_from_pointer(stack_data[0])
#     player = _battle_royal.get_player(userid)

#     if player is None or player.dead:
#         return

#     usercmd = make_object(UserCmd, stack_data[1])

#     if usercmd.buttons & PlayerButtons.SPEED and (usercmd.buttons & PlayerButtons.FORWARD or
#        usercmd.buttons & PlayerButtons.MOVELEFT or
#        usercmd.buttons & PlayerButtons.MOVERIGHT or
#        usercmd.buttons & PlayerButtons.LEFT or
#        usercmd.buttons & PlayerButtons.RIGHT):

#         # Cancel attacking
#         usercmd.buttons &= ~PlayerButtons.ATTACK
#         usercmd.buttons &= ~PlayerButtons.ATTACK2

#         if player.sprint.key_pressed and player.sprint.sprinting:
#             if hasattr(player, 'stamina'):
#                 if player.stamina.has_stamina_for(StaminaCost.SPRINT):
#                     player.stamina.consume(StaminaCost.SPRINT)

#                     player.sprint.ensure_speed(SPRINTING_PLAYER_SPEED)
#                     player.sprint.step()
#                 else:
#                     player.sprint.sprinting = False
#                     player.sprint.ensure_speed(DEFAULT_PLAYER_SPEED)
#                     LOW_STAMINA_SOUND.play(player.index)
#             else:
#                 player.sprint.ensure_speed(SPRINTING_PLAYER_SPEED)
#                 player.sprint.step()
#         elif not player.sprint.key_pressed and not player.sprint.sprinting:
#             player.sprint.sprinting = True
#             player.sprint.key_pressed = True
#             SPRINT_START_SOUND.play(player.sprint.player.index)
#     else:
#         player.sprint.key_pressed = False
#         player.sprint.sprinting = False
#         player.sprint.ensure_speed(DEFAULT_PLAYER_SPEED)
