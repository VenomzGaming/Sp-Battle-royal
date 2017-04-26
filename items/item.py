from entities.entity import Entity
from entities.helpers import index_from_pointer
from engines.precache import Model
from messages import SayText2

## ALL DECLARATIONS

__all__ = (
    'Item',
)

class Item:
    name = ''
    item_type = ''
    description = ''
    models = None
    amount = 1
    weight = 0

    def create(self, location):
        entity = Entity.create('prop_physics_override')
        entity.spawn()
        if self.models is not None:
            entity.world_model_index = Model(self.models).index
        entity.teleport(location)
        SayText2('Create entity').send()
        return entity

    def use(self):
        SayText2('Can\'t use').send()

    def destroy(self):
        SayText2('Can\'t destroy').send()

    def show(self):
        SayText2(self.name).send()
        SayText2(self.item_type).send()
        SayText2(self.description).send()
        SayText2(str(self.weight)).send()

    @classmethod
    def get_subclasses(cls):
        for subcls in cls.__subclasses__():
            yield subcls
            yield from subcls.get_subclasses()

    @classmethod
    def get_subclass_dict(cls):
        return { subcls.__name__: subcls for subcls in cls.get_subclasses() }
