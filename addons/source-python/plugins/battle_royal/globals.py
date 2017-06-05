## IMPORTS


## ALL DECLARATIONS

__all__ = (
    '_authorize_weapon',
    '_weapon_name',
    'items_spawn_manager',
    'players_spawn_manager',
    'air_drop_spawn_manager',
    'parachute',
    'info_map_parameters',
)

## GLOBALS

# Constants by map
MAP_HEIGHT = None

# Weapon that can be given in 'bump_weapon' Hook
_authorize_weapon = []

# Weapon dict weapon name
_weapon_name = {
	'Ak47' : 'AK47'
}

# Items spawn manager
items_spawn_manager = None

# Players spawn manager
players_spawn_manager = None

# Players spawn manager
air_drop_spawn_manager = None

# Parachute
parachute = None

# Info map parameters
info_map_parameters = None