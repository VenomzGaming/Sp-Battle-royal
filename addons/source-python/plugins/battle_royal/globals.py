## IMPORTS


## ALL DECLARATIONS

__all__ = (
    '_authorize_weapon',
    # '_match_hud',
    'items_spawn_manager',
    'players_spawn_manager',
)

## GLOBALS

# Weapon that can be given in 'bump_weapon' Hook
_authorize_weapon = []

# Items spawn manager
global items_spawn_manager
items_spawn_manager = None

# Players spawn manager
global players_spawn_manager
players_spawn_manager = None