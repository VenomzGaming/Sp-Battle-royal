## IMPORTS

from menus import SimpleMenu
from menus import SimpleOption
from menus import Text

from ..entity.battleroyal import _battle_royal
from ..entity.player import Player as BrPlayer
from .inventory import inventory_menu

__all__ = (
    'main_menu'
)


def _main_menu_build(menu, index):
    pass


def _main_menu_select(menu, index, choice):
    next_menu = choice.value
    if next_menu is not None:
        next_menu.previous_menu = menu
        return next_menu


main_menu = SimpleMenu(
    [
        Text('Battle Royal'),
        Text(' '),
        SimpleOption(1, 'Inventory', inventory_menu),
        SimpleOption(2, 'Rank', None),
        Text(' '),
        SimpleOption(9, 'Close', highlight=False),
    ],
    build_callback=_main_menu_build,
    select_callback=_main_menu_select
)
