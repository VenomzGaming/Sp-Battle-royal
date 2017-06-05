## IMPORTS

from entities.entity import Entity
from weapons.entity import Weapon as SPWeapon
from entities.helpers import index_from_pointer
from listeners.tick import Delay
from messages import SayText2

from .item import Item, items
from ..globals import _authorize_weapon, _weapon_name


class Weapon(Item):
    classname = ''
    item_type = 'weapon'
    ammo = 0
    clip = 0
    slot = ''

    @classmethod
    def create(cls, location):
        'Creation of the item in game. Proceed with this...'
        weapon_name = 'weapon_' + cls.__name__.lower()
        weapon = SPWeapon.create(weapon_name)
        weapon.teleport(location)
        weapon.spawn()
        return cls(weapon)

    def __init__(self, entity, *args, **kwargs):
        'Setting the ammo and clip count of the weapon on pickup.'
        super().__init__(entity, *args, **kwargs)
        self.ammo = 0
        self.clip = 15

    def can_be_used(self, player):
        weapon = player.get_weapon(is_filters=self.slot)
        return True if weapon is None else False

    def on_pickup(self, player):
        'Upon the item being picked up. Called after all checks.'
        if player.get_weapon(is_filters=self.slot):
            if not player.inventory.add(self):
                return False
        else:
            self.on_use(player)

        self.on_remove()
        return True

    def on_remove(self):
        'Called upon the wanted removal of the entity.'
        if self.entity is None:
            return

        if self in items:
            items.remove(self)
        self.entity.remove()

    def on_use(self, player):
        'Called upon the item being used. <use> input.'

        weapon = player.get_weapon(is_filters=self.slot)
        if weapon:
            weapon_name = weapon.classname.split('_')[1].title()
            item = Item.get_subclass_dict()[weapon_name](weapon)
            if not player.inventory.add(item):
                return False
            item._save_ammo()
            player.delay(0.1, item._drop, (player, ), cancel_on_level_end=True)

        player.inventory.discard(self)
        player.delay(0.2, self._setup_weapon, (player, ), cancel_on_level_end=True)

        return True

    def on_dropped(self, player):
        'Called when the weapon is dropped by a player.'
        setattr(player, '{}_weapon'.format(self.slot), None)
        self.entity.delay(0.1, self.entity.remove, cancel_on_level_end=True)

    def _setup_weapon(self, player):
        'When the weapon is given, this sets up the ammo and clip.'
        self.entity = SPWeapon.create(self.classname)
        _authorize_weapon.append(self.entity.index)
        self.entity.teleport(player.origin)
        self.entity.spawn()
        self._setup_ammo()

    def _drop(self, player):
        'Drop the item from the player.'
        player.drop_weapon(self.entity.pointer)
        self.entity.remove()
        # player.delay(0.1, self.entity.remove, cancel_on_level_end=True)

    def _save_ammo(self):
        'Saves the current ammo and clip counts.'
        SayText2('Weapon : ' + str(self.entity.clip)).send()
        self.ammo = self.entity.ammo
        self.clip = self.entity.clip

    def _setup_ammo(self):
        'Sets the current ammo and clip counts.'
        SayText2('item : ' + str(self.clip)).send()
        self.entity.delay(0, self.entity.set_ammo, (self.ammo, ))
        self.entity.delay(0.1, self.entity.set_clip, (self.clip, ))
