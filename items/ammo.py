## IMPORTS

from messages import SayText2

from .item import Item

class Ammo(Item):
    item_type = 'ammo'
    clip = 0
    ammo = 10
    models = 'models/props/coop_cementplant/coop_ammo_stash/coop_ammo_stash_full.mdl'

    def use(self, player):
    	weapon = player.get_weapon(self.slot)
    	if weapon is not None and self.type in weapon.tags:
    		if self.clip != 0:
    			weapon.clip += self.clip
    		weapon.ammo += self.ammo
    		SayText2('Add Ammo to ' + weapon.classname).send()
    	else:		
        	SayText2('Can\'t use').send()
