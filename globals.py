## IMPORTS

from .utils.spawn_manager import SpawnManager

__all__ = (
    '_authorize_weapon',
    '_match_hud',
    '_items_spawn_manager',
    '_players_spawn_manager',
)

## GLOBALS

# Weapon that can be given in 'bump_weapon' Hook
_authorize_weapon = []

# Contain HudMsg for remaining players and teams
_match_hud = None

# Items spawn manager
_items_spawn_manager = None

# Players spawn manager
_players_spawn_manager = None