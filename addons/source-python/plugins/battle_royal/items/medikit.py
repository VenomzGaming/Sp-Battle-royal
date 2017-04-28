## IMPORTS

from .care import Care

from messages import SayText2


class Medikit(Care):
    name = 'Medic Kit'
    heal = 50
    weight = 0
