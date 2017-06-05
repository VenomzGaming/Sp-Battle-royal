## IMPORTS

from entities.entity import Entity
from weapons.entity import Weapon as SPWeapon
from entities.helpers import index_from_pointer
from messages import SayText2

from .weapon import Weapon
from ..globals import _authorize_weapon



class Healthshot(Weapon):
    name = 'Health shot'
    classname = 'weapon_healthshot'
    item_type = 'weapon'
    slot = 'tool'
    weight = 1.0

    def equip(self, player, loot):
        weapon = player.get_weapon(is_filters=self.slot)
        if weapon is None:
            self.use(player)
        else:
            ammo = weapon.get_ammo() + 1
            weapon.delay(0, weapon.set_ammo, (ammo, ))
        player.inventory.discard(self)

    def on_item_given(player, item):
        SayText2('Player {player} has got {item} !'.format(player=player.name, item=item.name)).send()

    def use(self, player, callback=on_item_given):
        def delay_callback():
            weapon_name = 'weapon_' + self.__class__.__name__.lower()
            weapon_pointer = player.give_named_item(weapon_name, 0, None, True)
            weapon = Entity(index_from_pointer(weapon_pointer))
            _authorize_weapon.append(index_from_pointer(weapon_pointer))
            callback(player, weapon)
     
        player.delay(0, delay_callback)

