## IMPORTS

from .armor import Armor

from messages import SayText2


class Helmet(Armor):
    name = 'Helmet'
    armor = 0
    weight = 10

    def equip(self, player):
        if not player.has_helmet:
            self.use(player)


    def use(self, player):
    	player.has_helmet = True
    	SayText2('Add Helmet').send()
