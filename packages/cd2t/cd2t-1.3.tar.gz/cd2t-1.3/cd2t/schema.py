from cd2t.types.datatype import DataType

_MAIN_KEY = 'root_data_type'

class Schema(dict):
    def __init__(self, root_data_type=None) -> None:
        super().__init__()
        self[_MAIN_KEY] = root_data_type
        if root_data_type is not None:
            self._check_rdt(root_data_type)
            self[_MAIN_KEY] = root_data_type

    @property
    def root_data_type(self):
        return self.get(_MAIN_KEY, None)
    
    @staticmethod
    def _check_rdt(rdt :DataType):
        if not issubclass(type(rdt), DataType):
            raise ValueError("Parameter '%s' is not a subclass to '%s'"
                                 % (_MAIN_KEY, DataType) )

    
    def set_root_data_type(self, root_data_type):
        self._check_rdt(root_data_type)
        self['root_data_type'] = root_data_type


class SchemaError(ValueError):
    def __init__(self, message: str, path='') -> None:
        super().__init__()
        self.path = path
        self.message = message

    def __str__(self):
        if self.path:
            return "%s: %s" % (self.path, self.message)
        return self.message
