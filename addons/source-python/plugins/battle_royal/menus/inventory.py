## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text
from messages import SayText2
from players.entity import Player

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer
from ..menus.item import item_menu


__all__ = (
    'inventory_menu',
)


def _inventory_menu_build(menu, index):
    menu.clear()
    br_player = _battle_royal.get_player(Player(index))
    if br_player is None:
        return
        
    menu.append(Text('Inventory'))
    if len(br_player.inventory.items.values()) != 0:
        i = 1
        for item in br_player.inventory.items.values():
            menu.append(SimpleOption(i, item.name + ' (x'+str(item.amount)+')', (item_menu, item)))
            i += 1
    else:
        menu.append(Text('Empty inventory'))

    menu.append(Text(' '))
    if hasattr(menu, 'previous_menu'):
        menu.append(SimpleOption(7, 'Back', (menu.previous_menu, None), highlight=True))
    menu.append(SimpleOption(9, 'Close', highlight=True))


def _inventory_menu_select(menu, index, choice):
    next_menu, item = choice.value
    if next_menu is not None:
        next_menu.item = item
        next_menu.previous_menu = menu
        return next_menu


inventory_menu = SimpleMenu(
    build_callback=_inventory_menu_build,
    select_callback=_inventory_menu_select
)
