## IMPORTS

from cvars import ConVar
from filters.players import PlayerIter
from messages import HudMsg, SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..globals import _match_hud


__all__ = (
    'BattleRoyalHud',
    'show_match_hud',
)

## BATTLE ROYAL HUD MANAGER

class BattleRoyalHud:

    _match_hud = None
    _player_hud = dict()

    @property
    def match_hud(cls):
        return cls._match_hud

    @classmethod
    def match_info(cls):
        alive_player = len(_battle_royal.players)
        last_teams = len(_battle_royal.teams)

        text = 'Remaining players {players}'.format(players=alive_player)
        if last_teams != 0:
            text += ' | Remaining teams {teams}'.format(teams=last_teams)

        SayText2(text).send()
        cls._match_hud = HudMsg(
            message=text,
            hold_time=1,
            x=-1,
            y=-0.7,
        )

    @classmethod
    def player_weight(cls, player):
        msg = 'Available weight {weight}'.format(weight=player.total_weight)

        cls._player_hud[player.userid] = HudMsg(
            message=text,
            hold_time=1,
            x=-1,
            y=-0.7,
        ).send()

    @classmethod
    def remove_player(cls, player):
        del cls._player_hud[player.userid]

    @staticmethod
    def hitmarker(player):
        _configs['hitmarker'] = 'overlays/battle_royal/hitmarker'
        player.client_command('r_screenoverlay {}'.format(_configs['hitmarker']))
        Delay(0.5, player.client_command, ('r_screenoverlay off',))


## OLD WAY

def show_match_hud():
    # Bug don't show HudMsg
    alive_player = len(_battle_royal.players)
    last_teams = len(_battle_royal.teams)

    text = 'Remaining players {players}'.format(players=alive_player)
    if last_teams != 0:
        text += ' | Remaining teams {teams}'.format(teams=last_teams)

    SayText2(text).send()
    _match_hud = HudMsg(
        message=text,
        hold_time=1,
        x=-1,
        y=-0.7,
    )