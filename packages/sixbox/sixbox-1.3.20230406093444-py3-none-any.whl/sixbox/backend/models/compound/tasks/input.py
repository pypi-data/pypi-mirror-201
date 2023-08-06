from sixbox.backend.meta.comp_mutable_dict import CompoundMutableDict
from sixbox.backend.meta.resource import Resource

# noinspection PyProtectedMember
from sixbox.backend.models.compound.tasks import map_input_output


# noinspection PyProtectedMember
class Input(CompoundMutableDict, Resource):
    """
    Task input resource.
    """
    _name = 'inputs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, item):
        # noinspection PyBroadException
        try:
            inputs = self._parent._data[self._name][item]
            return map_input_output(inputs, self._api)
        except Exception:
            return None
