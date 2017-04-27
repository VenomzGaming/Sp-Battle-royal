## IMPORTS

from .armor import Armor

from messages import SayText2


class Helmet(Armor):
    name = 'Helmet'
    armor = 0
    weight = 10


    def use(self, player):
    	player.has_helmet = True
    	SayText2('Add Helmet').send()
