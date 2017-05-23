## IMPORTS

import memory

from cvars import ConVar

from entities.entity import Entity
from entities.constants import WORLD_ENTITY_INDEX

from engines.trace import engine_trace
from engines.trace import ContentMasks
from engines.trace import GameTrace
from engines.trace import Ray
from engines.trace import TraceFilterSimple

from filters.players import PlayerIter

from messages import HudMsg, SayText2

from mathlib import Vector

from players.entity import Player
from players.voice import voice_server

from listeners.tick import Delay

from .. import globals

from ..entity.battleroyal import _battle_royal

from ..config import _configs


__all__ = (
    'BattleRoyalHud',
    'set_proximity_listening',
    'get_map_height',
)

## BATTLE ROYAL HUD MANAGER

class BattleRoyalHud:

    # _timer_match_begin = _configs['waiting_match_begin'].get_int()
    warmup_hud = None
    match_hud = None
    _player_hud = dict()

    @classmethod
    def warmup(cls):
        # text = 'Match started in {}'.format(cls._timer_match_begin) 
        text = 'Are you prepared ?!'

        cls.match_hud = HudMsg(
            message=text,
            hold_time=1,
            x=-1,
            y=-0.7,
        ).send()
        # cls._timer_match_begin -= 1

    @classmethod
    def match_info(cls):
        alive_player = len(_battle_royal.players)
        last_teams = len(_battle_royal.teams)

        text = 'Remaining players {players}'.format(players=alive_player)
        if last_teams != 0:
            text += ' | Remaining teams {teams}'.format(teams=last_teams)

        cls.match_hud = HudMsg(
            message=text,
            hold_time=1,
            x=-1,
            y=-0.7,
        ).send()

    @classmethod
    def player_weight(cls, player):
        br_player = _battle_royal.get_player(player)
        if br_player is None:
            return

        msg = 'Available weight {weight} Kg'.format(weight=br_player.total_weight)

        cls._player_hud[br_player.userid] = HudMsg(
            message=msg,
            hold_time=1,
            channel=1,
            x=-1,
            y=1,
        ).send()

    @classmethod
    def winner(cls):
        duration = ConVar('mp_match_restart_delay').get_int()
        msg = None
        if len(_battle_royal.teams) != 0:
            for player in _battle_royal.players.values():
                msg = 'The winner group is {name} !'.format(name=player.group.name)
        else:
            for player in _battle_royal.players.values():
                msg = 'The winner is {name} !'.format(name=player.name)
                break

        HudMsg(
            message=msg,
            hold_time=duration,
            x=-1,
            y=-0.7,
        ).send()

        # End match
        Delay(duration, globals.info_map_parameters.fire_win_condition, (2,))

    @classmethod
    def remove_player(cls, player):
        if player.userid in cls._player_hud:
            del cls._player_hud[player.userid]

    @staticmethod
    def hitmarker(player):
        if player.steamid == 'BOT':
            return
            
        _configs = {}
        _configs['hitmarker'] = 'overlays/battle_royal/hitmarker'
        player.client_command('r_screenoverlay {}'.format(_configs['hitmarker']))
        Delay(0.5, player.client_command, ('r_screenoverlay off',))


## VOICE PROXIMITY

def set_proximity_listening(player):
    for other_player in PlayerIter('alive'):
        if other_player.origin.get_distance(player.origin) <= _configs['voice_proximity'].get_int():
            voice_server.set_client_listening(player.index, other_player.index, True)
        else:
            voice_server.set_client_listening(player.index, other_player.index, False)

## MAP

def get_map_height():
    worldspawn = Entity(WORLD_ENTITY_INDEX)
    height = worldspawn.world_mins.z + worldspawn.world_maxs.z
    origin_vector = (worldspawn.world_maxs - worldspawn.world_mins) / 2
    end_point = Vector(origin_vector.x, origin_vector.y, height)

    trace = GameTrace()
    engine_trace.trace_ray(
        Ray(origin_vector, end_point), ContentMasks.SOLID_BRUSH_ONLY, None, trace
    )

    find_height = height if trace.end_position.z > height else trace.end_position.z
    return find_height
