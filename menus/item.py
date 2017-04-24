## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer

__all__ = (
	'item_menu'
)


def _item_menu_build(menu, index):
	brPlayer = _battle_royal[Player(index).userid]
    menu.append(Text(menu.item.name))
    menu.append(Text(menu.item.type))
    menu.append(Text(menu.item.description))
    menu.append(Text(str(menu.item.weight)))
    menu.append(Text(' '))
    menu.append(SimpleOption(1, '1. Use', menu.item.use))
    menu.append(SimpleOption(2, '2. Drop', menu.item.drop))
    # menu.append(SimpleOption(2, '2. Drop', drop_menu))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=False))
    menu.append(SimpleOption(9, 'Close', highlight=False))


def _item_menu_select(menu, index, choice):
    action = choice.value
    SayText2(str(action)).send()


item_menu = SimpleMenu(
    build_callback=_main_menu_build,
    select_callback=_main_menu_select
)
