## IMPORTS

import math
import random

from engines.precache import Model
from engines.server import global_vars
from entities.entity import Entity
from filters.entities import EntityIter
from mathlib import Vector
from messages import SayText2

from .. import globals
from .spawn_manager import SpawnManager


class Helicopter:
    
    def __init__(self, model, speed=40.0, air_drop=False):
        self._model = model
        self._speed = speed
        self._air_drop = air_drop
        self._entity = None
        self._start_point = None
        self._end_point = None

    def create(self):
        self._entity = Entity.create('prop_dynamic')
        location = Vector(637.66650390625, 322.892578125, 256.03125)
        self._entity.origin = location
        self._entity.model = Model(self._model)
        self._entity.solid_type = 6
        self._entity.spawn()

    def _reference_point(self):
        if self._air_drop:
            return self._air_drop_point()
        else:
            return self._center_point()

    def _air_drop_point(self):
        globals.air_drop_spawn_manager = SpawnManager('air_drop', global_vars.map_name)
        locations = globals.air_drop_spawn_manager.locations
        air_drop_point = random.choice(locations)

        # Check if air drop point is in gas zone. If it's get another spawn point
        return air_drop_point
        
    def _center_point(self):
        for worldspawn in EntityIter('worldspawn'):
            map_center = (worldspawn.maxs - worldspawn.mins) / 2
            SayText2(str(map_center)).send()
            break
        else:
            raise NotImplementedError('No world on round start ~ wut?')

    def _trace_line(self):
        point = self._reference_point()
        direction_one = random.randrange(360)
        direction_two = (direction_one - 180) if direction_one >= 180 else (direction_one + 180)

        self._start_point = None
        self._end_point = None

    def move(self):
        if self._start_point is None or self._end_point is None:
            raise ValueError('Cannot move entity without start or end point.')

        entity = Entity.create('func_movelinear')
        entity.set_key_value_vector('movedir', self._vector_to_angle(self._end_point - self._start_point))
        entity.set_key_value_float('blockdamage', 0.0)
        entity.set_key_value_float('startposition', 0.0)
        entity.set_key_value_float('movedistance', (self._end_point - self._start_point).length)
        entity.set_property_float('m_flSpeed', self._speed)
        entity.spawnflags = 8
        entity.teleport(self._start_point, None, None)
        entity.spawn()
        self._entity.set_parent(entity, -1)

    def _vector_to_angle(vector):
        atan = math.degrees(math.atan(vector.y / vector.x))
        if vector.x < 0:
            y_angle = atan + 180
        elif vector.y < 0:
            y_angle = atan + 360
        else:
            y_angle = atan

        # Calculate the x angle value
        x_angle = 0 - math.degrees(math.atan(vector.z / math.sqrt(
            vector.y ** 2 + vector.x ** 2)))

        return Vector(x_angle, y_angle, 0)
