## IMPORTS

from entities.entity import Entity
from weapons.entity import Weapon
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .item import Item
from ..globals import _authorize_weapon, _weapon_name


class WeaponItem(Item):
    item_type = 'weapon'
    ammo = 0
    clip = 0
    slot = ''

    def create(self, location, set_ammo=False):
        weapon_name = 'weapon_' + self.__class__.__name__.lower()
        weapon = Weapon.create(weapon_name)
        weapon.teleport(location)
        weapon.spawn()
        if set_ammo:
            weapon.delay(0, weapon.set_ammo, (self.ammo, ))
            weapon.delay(0.1, weapon.set_clip, (self.clip, ))

        return weapon

    def equip(self, player, set_ammo=False):
        SayText2('Equip').send()
        weapon = player.get_weapon(is_filters=self.slot)
        if weapon is None:
            can_used = self.use(player, set_ammo)
            if can_used:
                SayText2('Can used').send()
                player.inventory.remove(self)

    def change(self, player, weapon):
        SayText2('Change').send()
        weapon_name, clip, ammo = weapon.classname.split('_')[1].title(), weapon.clip, weapon.ammo
        player.drop_weapon(weapon.pointer, None, None)
        Delay(0.1, weapon.remove)
        item_class = _weapon_name[weapon_name] if weapon_name in _weapon_name else weapon_name
        item = Item.get_subclass_dict()[item_class]()
        player.inventory.add(item)
        self.ammo = ammo
        self.clip = clip
        Delay(0.2, self.equip, (player, True))
            
    def on_item_given(player, item):
        SayText2('Player {player} has got {item} !'.format(player=player.name, item=item.classname)).send()

    def use(self, player, set_ammo=False, callback=on_item_given):
        def delay_callback():
            weapon = self.create(player.origin, set_ammo)
            _authorize_weapon.append(weapon.index)
            callback(player, weapon)
     
        weapon = player.get_weapon(is_filters=self.slot)
        if weapon is None:
            player.delay(0, delay_callback)
            return True
        else:
            if not set_ammo:
                SayText2('Not Loot').send()
                self.change(player, weapon)
                return False
            else:
                return False