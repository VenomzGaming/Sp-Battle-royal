## IMPORTS

from commands import CommandReturn
from commands.say import SayCommand
from cvars import ConVar
from messages import SayText2
from players.entity import Player

from .events import *
from .hooks import *
from .info import info
from .models.battleroyal import _battle_royal
from .models.player import Player as BrPlayer

def load():
    pass


def unload():
    pass

## COMMANDS


# INVENTORY COMMAND

@SayCommand(['inventory', 'inv'])
def _open_inventory(command, index, team_only=None):
    player = Player(index)
    brPlayer = _battle_royal[player.userid]
    brPlayer.inventory.show()

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