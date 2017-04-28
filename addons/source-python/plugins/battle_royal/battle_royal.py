## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from commands.typed import TypedSayCommand
from cvars import ConVar
from messages import SayText2
from players.entity import Player
from stringtables.downloads import Downloadables

from .entity.battleroyal import _battle_royal
from .entity.player import Player as BrPlayer
from .events import *
from .globals import _items_spawn_manager, _players_spawn_manager
from .hooks import *
from .info import info
from .menus import main_menu
from .menus.inventory import inventory_menu


def load():
    pass


def unload():
    pass


## DOWNLOAD

downloadables = Downloadables()
downloadables.add_directory('materials/overlays/battle_royal')


## MENUS

# MAIN MENU
@SayCommand(['battleroyal', 'br'])
def _open_main_menu(command, index, team_only=None):
    main_menu.send()

# INVENTORY MENU
@SayCommand(['inventory', 'inv'])
def _open_inventory_menu(command, index, team_only=None):
    inventory_menu.send()


## COMMANDS

# SPRINT COMMAND
@SayCommand('sprint')
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    player.speed = 1.2

# MAP COMMAND
@SayCommand('map')
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    SayText2('Show map').send()

# ADD SPAWN POINT ADMIN COMMAND
# @SayCommand('location')
# def _open_inventory(command, index, team_only=None):
#     player = Player(index)
#     SayText2(str(player.view_vector)).send()

@TypedSayCommand('location')
def typed_add_location(command_info, type_spawn:str, name:str):
    player = Player(command_info.index)
    vector = player.view_vector
    # if type_spawn == 'item':
    #     _items_spawn_manager.add(name, vector)
    # else:
    #     _players_spawn_manager.add(name, vector)
    SayText2(str(player.view_vector)).send()
