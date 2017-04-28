## IMPORTS

from .care import Care

from messages import SayText2


class Gauze(Care):
    name = 'Gauze'
    heal = 10
    weight = 0
    models = 'models/props/props_crates/wooden_crate_32x64.mdl'
