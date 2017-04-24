## IMPORTS

from cvars import ConVar
from filters.players import PlayerIter
from messages import HudMsg, SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal


__all__ = (
    'show_match_hud',
    'show_weight_hud',
)

# HUD PLAYER AND TEAMS

def show_match_hud():
    # Bug don't show HudMsg
    alive_player = len(_battle_royal.players)
    last_teams = len(_battle_royal.teams)
    hud_display_time = ConVar('mp_roundtime').get_int() * 60

    text = 'Remaining players {players}'.format(players=alive_player)
    if last_teams != 0:
        text += ' | Remaining teams {teams}'.format(teams=last_teams)

    SayText2(text).send()
    HudMsg(
        message=text,
        hold_time=hud_display_time,
        x=-1,
        y=-0.7,
    ).send()

def show_weight_hud():
    pass