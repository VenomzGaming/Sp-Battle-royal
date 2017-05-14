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

    #
    # Match config
    #
    _config.section('Match')

    _configs['waiting_match_begin'] = _config.cvar(
        'waiting_match_begin', 30,
        description='Waiting moment before match begin.'
    )

    _configs['spawn_player_type'] = _config.cvar(
        'spawn_player_type', 1,
        description='0 - Spawn at random position one the ground | 1 - Spawn in sky with parachute | 1 - Spawn in helicopter.'
    )

    _configs['voice_proximity'] = _config.cvar(
        'voice_proximity', 1000,
        description='Distance max to allow player to hear another player.'
    )


    #
    # Parachute config
    #
    _config.section('Parachute')

    _configs['parachute_enable'] = _config.cvar(
        'parachute_enable', 1,
        description='Enable parachute feature.'
    )

    _configs['parachute_duration'] = _config.cvar(
        'parachute_duration', 30,
        description='Defines enable time to use parachute after round start.'
    )

    _configs['parachute_falling_speed'] = _config.cvar(
        'parachute_falling_speed', '10',
        description='Defines the falling speed of the parachute.'
    )


    #
    # Gas config
    #
    _config.section('Gas')

    _configs['time_before_spreading'] = _config.cvar(
        'time_before_spreading', 60,
        description='Waiting time before gas spreading after round start.'
    )

    _configs['time_between_spreading'] = _config.cvar(
        'time_between_spreading', 60,
        description='Waiting time before another gas spreading after gas spread.'
    )
    