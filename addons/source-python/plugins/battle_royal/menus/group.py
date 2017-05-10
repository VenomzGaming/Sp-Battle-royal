## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer

__all__ = (
    'group_menu',
)


def _group_menu_build(menu, index):
    menu.clear()
    br_player = _battle_royal.get_player(Player(index))
    menu.append(Text('Join ' + menu.sender.name + ' group ?'))
    menu.append(SimpleOption(1, 'Yes', True))
    menu.append(SimpleOption(2, 'No', False))
    menu.append(Text(' '))
    menu.append(SimpleOption(9, 'Close', False, highlight=True))
    return menu


def _group_menu_select(menu, index, choice):
    accept = choice.value
    owner = menu.sender
    br_player = _battle_royal.get_player(Player(index))

    if accept:
        owner.group.add_player(br_player)
        SayText2('You are added to the group').send(br_player.index)
    else:
        SayText2(br_player.name + ' refused your inviation').send(owner.index)
    return 


group_menu = SimpleMenu(
    build_callback=_group_menu_build,
    select_callback=_group_menu_select
)