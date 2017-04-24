## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from cvars import ConVar
from messages import SayText2
from players.entity import Player

from .entity.battleroyal import _battle_royal
from .entity.player import Player as BrPlayer
from .events import *
from .hooks import *
from .info import info
from .menus import main_menu
from .menus.inventory import inventory_menu

def load():
    pass


def unload():
    pass


## MENUS

# MAIN MENU
@SayCommand(['battleroyal', 'br'])
def _open_main_menu(command, index, team_only=None):
    brPlayer = _battle_royal[Player(index).userid]
    brPlayer.inventory.show()

# INVENTORY MENU
@SayCommand(['inventory', 'inv'])
def _open_inventory_menu(command, index, team_only=None):
    player = Player(index)
    brPlayer = _battle_royal[player.userid]
    brPlayer.inventory.show()


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
@SayCommand('location')
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    SayText2(str(player.view_vector)).send()
