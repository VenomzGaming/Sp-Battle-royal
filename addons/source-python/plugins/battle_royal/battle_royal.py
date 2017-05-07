## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from commands.typed import TypedSayCommand
from cvars import ConVar
from messages import SayText2
from players.entity import Player
from stringtables.downloads import Downloadables

from . import globals
from .commands.group_command import *
from .entity.battleroyal import _battle_royal
from .entity.player import BattleRoyalPlayer
from .entity.group import BattleRoyalGroup
from .events import *
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

# ITEMS
downloadables.add_directory('models/battle_royal')
downloadables.add_directory('materials/models/battle_royal')

# PARACHUTE
downloadables.add_directory('models/parachute')
downloadables.add_directory('materials/models/parachute')

# VEHICULES
downloadables.add_directory('models/props_vehicules')
downloadables.add_directory('materials/models/props_vehicules')


## MENUS

# MAIN MENU
@SayCommand(['!battleroyal', '!br', '/battleroyal', '/br'])
def _open_main_menu(command, index, team_only=None):
    main_menu.send(index)
    return CommandReturn.BLOCK


# INVENTORY MENU
@SayCommand(['!inventory', '!inv', '/inventory', '/inv'])
def _open_inventory_menu(command, index, team_only=None):
    inventory_menu.send(index)
    return CommandReturn.BLOCK


## COMMANDS


# SPRINT COMMAND
@SayCommand(['!sprint', '/sprint'])
def _activ_sprint(command, index, team_only=None):
    player = Player(index)
    player.speed = 1.2
    return CommandReturn.BLOCK


# MAP COMMAND
@SayCommand(['!map', '/map'])
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    SayText2('Show map').send()
    return CommandReturn.BLOCK


# Test
@SayCommand('!position')
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    vector = player.view_coordinates
    SayText2(str(vector)).send()
    return CommandReturn.BLOCK

## ADMIN

# ADD SPAWN POINT ADMIN COMMAND
@TypedSayCommand('location')
def _add_location(command_info, type_spawn:str, name:str):
    player = Player(command_info.index)
    vector = player.view_coordinates
    if type_spawn == 'item':
        globals.items_spawn_manager.add(name, vector)
    else:
        globals.players_spawn_manager.add(name, vector)
    SayText2(str(vector)).send()
    return CommandReturn.BLOCK
