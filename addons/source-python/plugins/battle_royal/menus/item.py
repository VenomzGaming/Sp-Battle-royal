## IMPORTS

from mathlib import Vector
from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..items.item import Item
from ..entity.player import Player as BrPlayer

__all__ = (
    'item_menu',
)


def _item_remove_menu_build(menu, index):
    menu.clear()
    br_player = _battle_royal.get_player(Player(index))
    menu.append(Text('Remove : ' + menu.item.name))
    menu.append(Text('Amount : '))
    menu.append(SimpleOption(1, '1', 1))
    menu.append(SimpleOption(2, '5', 5))
    menu.append(SimpleOption(3, '10', 10))
    menu.append(SimpleOption(4, '15', 15))
    menu.append(SimpleOption(5, '20', 20))
    menu.append(SimpleOption(6, 'All', None))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))
    return menu


def _item_remove_menu_select(menu, index, choice):
    br_player = _battle_royal.get_player(Player(index))

    if isinstance(choice.value, SimpleMenu):
        return choice.value

    item = menu.item
    amount = choice.value
    br_player.drop(item, amount)

    return menu.previous_menu


item_remove_menu = SimpleMenu(
    build_callback=_item_remove_menu_build,
    select_callback=_item_remove_menu_select
)


def _item_menu_build(menu, index):
    menu.clear()
    br_player = _battle_royal.get_player(Player(index))
    menu.append(Text('Item : ' + menu.item.name))
    menu.append(Text('Type : ' + menu.item.item_type))
    menu.append(Text(menu.item.description))
    menu.append(Text(str(menu.item.weight) + ' Kg'))
    menu.append(Text(' '))
    menu.append(SimpleOption(1, 'Use', ('use', menu.item)))
    if menu.item.amount == 1:
        menu.append(SimpleOption(2, 'Drop', ('drop', menu.item)))
    else:
        menu.append(SimpleOption(2, 'Drop', (item_remove_menu, menu.item)))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', (menu.previous_menu, None), highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))
    return menu


def _item_menu_select(menu, index, choice):
    br_player = _battle_royal.get_player(Player(index))
    action, item = choice.value

    if action == 'use':
        br_player.use(item)
    elif action == 'drop':
        br_player.drop(item)
    elif action is not None:
        if item is not None:
            action.previous_menu = menu.previous_menu
            action.item = item
        return action

    return menu.previous_menu

item_menu = SimpleMenu(
    build_callback=_item_menu_build,
    select_callback=_item_menu_select
)
