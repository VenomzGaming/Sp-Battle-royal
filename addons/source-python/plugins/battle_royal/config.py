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

    _configs['parachute_button'] = _config.cvar(
        'parachute_button', 'SPEED',
        description='Defines the button to use the parachute.'
    )

    _configs['parachute_button'] = _config.cvar(
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
    