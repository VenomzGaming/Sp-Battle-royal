## IMPORTS

from config.manager import ConfigManager

from .info import info

## ALL DECLARATION

__all__ = (
    '_configs',
)

## GLOBALS

_configs = dict()

with ConfigManager(info.name) as _config:
    # Add config for example default player weight
    pass
    