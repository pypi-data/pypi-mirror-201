from cd2t.types.base import BaseDataType
from cd2t.References import References
from cd2t.results import DataTypeMismatch, FindingsList
from cd2t.schema import SchemaError


class Multitype(BaseDataType):
    type = 'multitype'
    multi_type_class = True
    options = [
        # option_name, required, class
        ('types', True, list, None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.types = None
        self.type_names = list()
        self.type_objects = list()
        self.matching_classes = []
        self.data_type_mismatch_message = "None of the data types matches"
    
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
            if data_type.multi_type_class:
                raise SchemaError("Multi type '%s' not supported in 'multitype'" % type_name, path)
            if type_name not in self.type_names:
                self.type_names.append(type_name)
            else:
                raise SchemaError("Duplicate data type '%s' in 'types' found" % type_name, path)
            data_type.build_schema(schema=dic, path=path, data_types=data_types, subschemas=subschemas, subpath=subpath)
            self.type_objects.append(data_type)
            self.matching_classes.extend(data_type.matching_classes)
            i += 1
        return self

    def build_sub_references(self, data :any, path :str, references=References()) -> list:
        for type_object in self.type_objects:
            if type_object.data_matches_type(data):
                type_object.build_references(data=data, path=path, references=references)
    
    def autogenerate_data(self, data :any, path :str, references :References):
        FL = FindingsList()
        if data is None:
            return data, FL
        # Try to find ...
        for type_object in self.type_objects:
            if type_object.data_matches_type:
                FL += type_object.autogenerate_data(data=data, path=path, references=references)
        return data, FL

    def validate_data(self, data :any, path :str, references=References()) -> list:
        FL = FindingsList()
        for type_object in self.type_objects:
            if type_object.data_matches_type(data):
                return type_object.validate_data(data=data, path=path, references=references)
        FL.append(DataTypeMismatch(path=path, message='None of the data types matches'))
        return FL

