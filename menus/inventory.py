## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer


__all__ = (
	'inventory_menu'
)


def _inventory_menu_build(menu, index):
    menu.clear()
    menu.title = 'Inventory'
	brPlayer = _battle_royal[Player(index).userid]
    i = 1
    for item in brPlayer.inventory.items:
        menu.append(SimpleOption(i, item.name, (item_menu, item)))
        i += 1

    menu.append(SimpleOption(7, 'Back', menu.previous_menu, highlight=False))
    menu.append(SimpleOption(9, 'Close', highlight=False))


def _inventory_menu_select(menu, index, choice):
    next_menu, item = choice.value
    if next_menu is not None:
        next_menu.item = item
        next_menu.title = item.name
        next_menu.previous_menu = menu
        return next_menu


inventory_menu = SimpleMenu(
    build_callback=_main_menu_build,
    select_callback=_main_menu_select
)
