## IMPORTS

from cvars import ConVar
from listeners.tick import Delay, Repeat, RepeatStatus
from entities.entity import Entity
from engines.precache import Model
from filters.players import PlayerIter
from messages import SayText2
from effects import TempEntity


## ALL DECLARATIONS

__all__ = (
    'Gas',
)

_gas_model = Model('sprites/laserbeam.vmt')

class Gas:
    '''
        Class which manage gas system on map.
        :param Vector location:
            Center point of gas circle.
        :param int radius:
            Radius of gas circle.
        :param int damage:
            Amount of damage deal by gas per tick.
        :param int tick_time:
            Tick time of damage.
        :param int duration (default=None):
            Duration of gas (Infini)
    '''

    def __init__(self, location, radius, damage=1, tick_time=5, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeater = Repeat(self._damage_player, cancel_on_level_end=True)
        self._location = location
        self._radius = radius
        self._damage = damage
        self._tick_time = tick_time
        self._duration = ConVar('mp_roundtime') if duration is None else duration
        self._effect = None

    def set_damage(self, damage):
        '''Set gas damage amount per tick.'''
        self._damage = damage

    def get_damage(self, damage):
        '''Get damage amount.'''
        return self._damage

    damage = property(get_damage, set_damage)

    def set_radius(self, radius):
        '''Set radius.'''
        self._radius = radius

    def get_radius(self, radius):
        '''Get radius.'''
        return self._radius

    radius = property(get_radius, set_radius)

    @property
    def effect(self):
        '''Return :class TempEntity object.'''
        return self._effect

    def _damage_player(self):
        '''Damage players which are in gas.'''
        for victim in PlayerIter('alive'):
            if victim.origin.get_distance(self._location) >= self._radius:
                victim.take_damage(self._damage)

    def _effect(self):
        '''Create gas effect.'''
        self._effect = TempEntity('BeamRingPoint', center=self._location, start_radius=self._radius,
            end_radius=self._radius+1, model_index=_gas_model.index, halo_index=_gas_model.index,
            life_time=self._duration, amplitude=0, red=0, green=255, blue=0, alpha=255, flags=0,
            start_width=10, end_width=10)
        self._effect.create()

    def spread(self, spread_in):
        '''Spread gas.'''
        Delay(spread_in, self._repeater.start, (self._tick_time, ))
        Delay(spread_in, self._effect)

    def stop(self):
        '''Stop spreading gas.'''
        self._repeater.stop()
        self._effect.remove()