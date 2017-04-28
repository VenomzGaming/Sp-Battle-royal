## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer

__all__ = (
    'backpack_menu'
)

## SHOW ENNEMY BACKPACK CONTENT

def _backpack_menu_build(menu, index):
    if hasattr(menu, 'backpack') and hasattr(menu, 'entity'):
        return

    menu.clear()
    brPlayer = _battle_royal.get_player(Player(index))

    menu.append(Text('Inventory'))
    if len(menu.items.values()) != 0:
        i = 1
        for item in menu.items.values():
            menu.append(SimpleOption(i, item.name + ' (x'+str(item.amount)+')', (item_backpack_menu, item)))
            i += 1
    else:
        menu.append(Text('Empty Backpack'))
        entity = _battle_royal.get_item_ent(menu.entity)
        entity.remove()
        # _battle_royal.remove_item_ent(entity)

    menu.append(Text(' '))
    menu.append(SimpleOption(9, 'Close', highlight=True))


def _backpack_menu_select(menu, index, choice):
    next_menu, item = choice.value
    if next_menu is not None:
        next_menu.item = item
        next_menu.previous_menu = menu
        return next_menu

## SHOW ITEM INFO

def _item_backpack_menu_build(menu, index):
    menu.clear()
    brPlayer = _battle_royal.get_player(Player(index))
    menu.append(Text('Item : ' + menu.item.name))
    menu.append(Text('Type : ' + menu.item.item_type))
    menu.append(Text('Amount : ' + str(menu.item.amount)))
    menu.append(Text('Total weight : ' + str(menu.item.weight * menu.item.amount) + ' Kg'))
    menu.append(Text(menu.item.description))
    menu.append(Text(' '))
    menu.append(SimpleOption(1, 'Take', menu.item))
    menu.append(Text(' '))
    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))


def _item_backpack_menu_select(menu, index, choice):
    brPlayer = _battle_royal.get_player(Player(index))
    item = choice.value
    brPlayer.pick_up(item)
    return menu.previous_menu


item_backpack_menu = SimpleMenu(
    build_callback=_item_backpack_menu_build,
    select_callback=_item_backpack_menu_select
)

backpack_menu = SimpleMenu(
    build_callback=_backpack_menu_build,
    select_callback=_backpack_menu_select
)
