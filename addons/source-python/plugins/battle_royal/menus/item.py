## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..items.item import Item
from ..entity.player import Player as BrPlayer

__all__ = (
    'item_menu'
)


def _item_menu_build(menu, index):
    menu.clear()
    br_player = _battle_royal.get_player(Player(index))
    menu.append(Text('Item : ' + menu.item.name))
    menu.append(Text('Type : ' + menu.item.item_type))
    menu.append(Text(menu.item.description))
    menu.append(Text(str(menu.item.weight) + ' Kg'))
    menu.append(Text(' '))
    menu.append(SimpleOption(1, 'Use', menu.item))
    menu.append(SimpleOption(2, 'Drop', 'drop'))
    # menu.append(SimpleOption(2, '2. Drop', drop_menu))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))
    return menu


def _item_menu_select(menu, index, choice):
    br_player = _battle_royal.get_player(Player(index))
    param = choice.value

    SayText2(str(param)).send()
    if isinstance(param, SimpleMenu):
        return param

    if isinstance(param, Item):
        br_player.use(param)
        # param.use(br_player)

    return menu.previous_menu


item_menu = SimpleMenu(
    build_callback=_item_menu_build,
    select_callback=_item_menu_select
)
