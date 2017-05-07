## IMPORTS

import json
import os

from mathlib import Vector
from paths import PLUGIN_DATA_PATH


LOCATION_PATH = {
    'item' : 'battle_royal/items_spawn',
    'player' : 'battle_royal/players_spawn'
}


class SpawnManager(dict):

    def __init__(self, name, map_name):
        super().__init__()
        self._name = name
        self._path = PLUGIN_DATA_PATH / LOCATION_PATH[name] / map_name + '.json'
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
            location = Vector(*map(float, location.replace(' ', '').split(',')))
            location.z+32

        super().__setitem__(name, location)

    @property
    def locations(self):
        return list(self.values())

    def _load_location(self):
        self.clear()

        if self._path.find('.json') == -1:
            raise ValueError(
                'Path of location must be an Json file.'
            )

        if not self._path.exists():
            with open(self._path, 'w+') as file:
                json.dump({}, file)
        else:
            with open(self._path) as data_json: 
                try:
                    for name, value in json.load(data_json).items():
                        self[name] = value
                except:
                    raise ValueError(
                        'Json file incorrect.'
                        )

    def _save_location(self):
        temp_dict = {}
        for key, location in self.items():
            temp_dict[key] = str(location.x) + ',' + str(location.y) + ',' + str(location.z)

        with open(self._path, 'w') as data_json:
            json.dump(temp_dict, data_json, indent=4, sort_keys=True)

    def add(self, name, value):
        self[name] = value
        self._save_location()

    # Useless for the moment
    def remove(self, name=None, value=None):
        if value is not None:
            for key, val in self.items():
                if val == value:
                   del self[key]
        else:
            del self[name]
