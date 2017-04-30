## IMPORTS

from weapons.entity import Weapon
from messages import SayText2

from .weapon import WeaponItem



class Healthshot(WeaponItem):
    name = 'Health shot'
    item_type = 'weapon'
    slot = 'tool'
    weight = 1

    def create(self, location):
        weapon = Weapon.create('weapon_healthshot')
        weapon.teleport(location)
        weapon.spawn()
        return weapon

    def equip(self, player):
        weapon = player.get_weapon(is_filters=self.slot)
        if weapon is None:
            self.use(player)
            player.inventory.remove(self)

