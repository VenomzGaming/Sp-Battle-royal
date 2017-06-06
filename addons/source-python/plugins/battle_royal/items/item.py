## IMPORTS

from engines.precache import Model
from entities.entity import Entity
from entities.helpers import index_from_pointer
from messages import SayText2
from weapons.entity import Weapon


## ALL DECLARATIONS


__all__ = (
    'Item',
    'items',
)

## GLOBAL

ITEM_ENTITY_TYPES = Entity, Weapon


## STORAGE OF ALL ITEMS

class Items(list):
    '''
        This class is used to store all <Items> and retrieve them by an attribute.
    '''

    def find_by_index(self, index):
        'Find item by entity index'
        for item in self:
            if not item.entity:
                continue
            elif item.entity.index == index:
                return item
        return None

    def clear(self, index):
        'Overriden <list.clear> to remove all entity before clear list'
        for item in self:
            if not item.entity:
                continue
            else:
                item.entity.remove()

        super(Items, self).clear()


items = Items()


## GENERIC ITEM CLASSES

class Item(object):
    '''
        Item is a unused class which implements
        all specific attributes a static item
        needs. Item has to be subclassed
        and given event methods to be used
        successfully.
        :param Entity entity:
            Existing Entity or Weapon.
    '''

    name = 'Unnamed'
    description = 'Unnamed Item'
    item_type = ''
    weight = 0.0
    amount = 1
    model = Model('models/props/coop_cementplant/coop_ammo_stash/coop_ammo_stash_empty.mdl')

    def __init__(self, entity):
        'Wrap the item around the entity, and store for later use.'
        self._entity = entity

    def __new__(cls, *args, **kwargs):
        'Store all the new instances inside the <Items> list.'
        instance = object.__new__(cls)
        items.append(instance)
        return instance

    @classmethod
    def create(cls, location):
        'Creation of the item in game. Proceed with this...'
        entity = Entity.create('prop_physics_override')
        entity.model = cls.model
        entity.origin = location
        entity.spawn_flags = 256
        entity.solid_flags = 152
        entity.collision_group = 11
        entity.spawn()
        return cls(entity)

    def can_be_used(self):
        'To be called before the item wants to be used.'
        raise NotImplementedError('Must be overriden in a subclass of <Item>.')

    def on_pickup(self, player):
        'To be called upon the item being picked up by the player.'
        raise NotImplementedError('Must be overriden in a subclass of <Item>.')

    def on_remove(self):
        'To be called when the item wants to be removed/destroyed.'
        raise NotImplementedError('Must be overriden in a subclass of <Item>.')

    def on_use(self, player):
        'To be called upon the item being used by a player.'
        raise NotImplementedError('Must be overriden in a subclass of <Item>.')

    def on_dropped(self, player):
        'To be called upon the item being dropped. Only applicable to weapons.'
        raise NotImplementedError('Must be overriden in a subclass of <Item>.')

    @property
    def entity(self):
        'Return the entity which this item wraps around.'
        return self._entity

    @entity.setter
    def entity(self, entity):
        'Only allow the setting of the item if it is of these types.'
        if type(entity) not in ITEM_ENTITY_TYPES:
            raise TypeError('Cannot bind <Item> to type <{}>. Must be type <{}>'.format(
                type(entity), ITEM_ENTITY_TYPES))
        self._entity = entity

    @classmethod
    def get_subclasses(cls):
        'Retrieve all subclasses for a given python class.'
        for subcls in cls.__subclasses__():
            yield subcls
            yield from subcls.get_subclasses()

    @classmethod
    def get_subclass_dict(cls):
        'Retrieve a dictionary for all subclasses for a given python class.'
        return { subcls.__name__: subcls for subcls in cls.get_subclasses() }
