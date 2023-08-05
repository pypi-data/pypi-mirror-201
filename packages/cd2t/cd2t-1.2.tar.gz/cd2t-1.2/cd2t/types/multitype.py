from cd2t.types.base import BaseDataType
from cd2t.references import *
from cd2t.results import *
from cd2t.schema import SchemaError


class Multitype(BaseDataType):
    options = [
        # option_name, required, class
        ('types', True, list, None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.types = None
        self.type_names = list()
        self.type_objects = list()
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.load_schema_options(schema, path)
        i = 0
        for dic in self.types:
            if not isinstance(dic, dict):
                raise SchemaError("Non-object found in option 'types' at position %d" % i, path)
            if len(dic) == 0:
                raise SchemaError("Empty object found in option 'types' at position %d" % 1, path)
            if 'type' not in dic.keys():
                raise SchemaError("Object does not have 'type' attribute in option 'types' at position %d" % i ,path)
            type_name = dic['type']
            if type_name not in data_types.keys():
                raise SchemaError("Type '%s' not found in option 'types' at position %d" % (type_name, i), path)
            data_type = data_types[type_name]()
            if data_type.matching_class is None:
                raise SchemaError("Multi type '%s' not supported in 'multitype'" % type_name, path)
            if type_name not in self.type_names:
                self.type_names.append(type_name) 
            else:
                raise SchemaError("Duplicate data type '%s' in 'types' found" % type_name, path)
            data_type.build_schema(schema=dic, path=path, data_types=data_types, subschemas=subschemas, subpath=subpath)
            self.type_objects.append(data_type)
            i += 1
        return self
    
    def autogenerate_values(self, data :any, path :str, references :References):
        if data is None:
            return data, list()
        # Try to find ...
        for type_object in self.type_objects:
            if isinstance(data, type_object.matching_class):
                # a matching type for the data...
                return type_object.autogenerate_values(data=data, path=path, references=references)
        return data, list()

    def validate_data(self, data :any, path :str, references=References()) -> list:
        # Try to find ...
        for type_object in self.type_objects:
            if isinstance(data, type_object.matching_class):
                # a matching type for the data...
                return type_object.validate_data(data=data, path=path, references=references)
        return [DataTypeMismatch(path=path, message='None of the data types matches')]

