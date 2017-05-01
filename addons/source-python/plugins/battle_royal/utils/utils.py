## IMPORTS

from cvars import ConVar
from filters.players import PlayerIter
from messages import HudMsg, SayText2
from players.entity import Player
from listeners.tick import Delay

from ..entity.battleroyal import _battle_royal
# from ..globals import _match_hud


__all__ = (
    'BattleRoyalHud',
    'show_match_hud',
)

## BATTLE ROYAL HUD MANAGER

class BattleRoyalHud:

    match_hud = None
    _player_hud = dict()

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
    def remove_player(cls, player):
        del cls._player_hud[player.userid]

    @staticmethod
    def hitmarker(player):
        if player.steamid == 'BOT':
            return
            
        _configs = {}
        _configs['hitmarker'] = 'overlays/battle_royal/hitmarker.vmt'
        player.client_command('r_screenoverlay {}'.format(_configs['hitmarker']))
        Delay(0.5, player.client_command, ('r_screenoverlay off',))
