## IMPORTS

import json

from mathlib import Vector
from path import PLUGIN_DATA_PATH


class SpawnManager(dict):

    def __init__(self, name, path):
        self._name = name
        self.load_location(path)
    
    def __setitem__(self, name, location):
        if name in self:
            raise KeyError(
                'Cannot assign a new {type} to {name}.'.format(
                    type=self._name,
                    name=name,
                )
            )

        if isinstance(location, str):
            location = eval('Vector(' + location + ')')

        super().__setitem__(name, location)

    @property
    def get_locations(self):
        return list(self.values())

    def load_location(self, path):
        if path.find('.json') == -1:
            raise ValueError(
                'Path of location must be an Json file.'
            )

        with open(PLUGIN_DATA_PATH / path) as data_json:    
            data = json.load(data_json)

        for name, location in data:
            self.add_location(name, location)

    def add(self, name, value):
        self[name] = value

    def remove(self, name=None, value=None):
        if value is not None:
            for key, val in self.items():
                if val == value:
                   del self[key]
        else:
            del self[name]
