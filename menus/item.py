## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer

__all__ = (
    'item_menu'
)


def _item_menu_build(menu, index):
    menu.clear()
    brPlayer = _battle_royal.get_player(Player(index))
    menu.append(Text('Item : ' + menu.item.name))
    menu.append(Text('Type : ' + menu.item.item_type))
    menu.append(Text(menu.item.description))
    menu.append(Text(str(menu.item.weight) + ' Kg'))
    menu.append(Text(' '))
    menu.append(SimpleOption(1, 'Use', menu.item.use))
    menu.append(SimpleOption(2, 'Drop', 'drop'))
    # menu.append(SimpleOption(2, '2. Drop', drop_menu))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))
    return menu


def _item_menu_select(menu, index, choice):
    brPlayer = _battle_royal.get_player(Player(index))
    function = choice.value
    SayText2(str(function)).send()
    return menu


item_menu = SimpleMenu(
    build_callback=_item_menu_build,
    select_callback=_item_menu_select
)
