## IMPORTS

from config.manager import ConfigManager

from .info import info

## ALL DECLARATION

__all__ = (
    'g_configs',
)

## GLOBALS

g_configs = dict()

with ConfigManager(info.name) as _config:
    #
    #   Displaying message
    #
    _config.section('Display')

    g_configs['display_type'] = _config.cvar(
        'display_type', 2,
        '1 - Display in chat | 2 - Display in hint text', 0)

    #
    #   Displaying informations
    #
    _config.section('Informations')

    g_configs['show_hit_member'] = _config.cvar(
        'show_hit_member', 1,
        '1 - Enable touch member display | 0 - Disable touch member display', 0) 

    g_configs['show_armor_hit'] = _config.cvar(
        'show_armor_hit', 1,
        '1 - Enable armor informations | 0 - Disable armor informations', 0)
    