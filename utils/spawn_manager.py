## IMPORTS

import json
import os

from mathlib import Vector
from path import Path, PLUGIN_DATA_PATH


class SpawnManager(dict):

    def __init__(self, name, path):
        super().__init__()
        self._name = name
        self._path = Path(path)
        self._load_location()
    
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

    def _load_location(self):
        self[self._name].clear()

        if self._path.find('.json') == -1:
            raise ValueError(
                'Path of location must be an Json file.'
            )

        if not self._path.exists():
            with self._path.open('w') as file:
                json.dump({}, file)

        with open(PLUGIN_DATA_PATH / self._path) as data_json:    
            for name, value in json.load(data_json).items():
                self[name] = value

    def _save_location(self):
        with self._path.open('w') as data_json:
            temp_dict = {}
            for name, location in self.items():
                temp_dict[name] = location

            json.dump(temp_dict, data_json, indent=4, sort_keys=True)

    def add(self, name, value):
        self[name] = value
        self._save_location()

    def remove(self, name=None, value=None):
        if value is not None:
            for key, val in self.items():
                if val == value:
                   del self[key]
        else:
            del self[name]
