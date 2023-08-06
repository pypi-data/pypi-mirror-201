from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.results import FindingsList, ValidationFinding, WrongValueFinding
from cd2t.References import References
from cd2t.schema import SchemaError
import copy

class List(BaseDataType):
    type = 'list'
    matching_classes = [list]
    options = [
        # option_name, required, class
        ('minimum', False, int, None),
        ('maximum', False, int, None),
        ('allow_duplicates', False, bool, True),
        ('elements', True, dict, dict()),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.allow_duplicates = True
        self.elements = dict()
        self.element_data_type = None
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.path = path
        self.load_schema_options(schema, path)
        if len(self.elements) == 0:
            self.element_data_type = AnyDataType()
            return
        if not 'type' in self.elements.keys():
            raise SchemaError("'elements' need to have a key 'type'", self.path)
        element_data_type_name = self.elements['type']
        if element_data_type_name not in data_types.keys():
            raise SchemaError("'elements' data type '%s' not found" % 
                              (element_data_type_name), self.path)
        self.element_data_type = data_types[element_data_type_name]()
        # Save recursively detected data type (i.e. from 'schema' --> subschema)
        self.element_data_type = self.element_data_type.build_schema(
            schema=self.elements, path=path+"[.]", data_types=data_types,
            subschemas=subschemas, subpath=subpath)
        return self
    
    def build_sub_references(self, data :any, path :str, references :References):
        i = 0
        for element in data:
            self.element_data_type.build_references(element, "%s[%d]" % (path, i), references)
            i += 1
    
    def autogenerate_data(self, data :any, path :str, references :References):
        FL = FindingsList()
        if not self.data_matches_type(data):
            return data, FL
        new_list = list()
        i = 0
        for element in data:
            _data, _FL = self.element_data_type.autogenerate_data(
                element, "%s[%d]" % (path, i), references)
            new_list.append(_data)
            FL += _FL
            i += 1
        return new_list, FL

    def verify_data(self, data :any, path :str, references=References()) -> FindingsList:
        FL = FindingsList()
        if self.minimum and len(data) < self.minimum:
            FL.append(WrongValueFinding(
                        path=path,
                        message='Length of list is lower than %d' % self.minimum))
        elif self.maximum and len(data) > self.maximum:
            FL.append(WrongValueFinding(
                        path=self.path,
                        message='Length of list is greater than %d' % self.maximum))
        i = 0
        for element in data:
            FL += self.element_data_type.validate_data(
                element, "%s[%d]" % (path, i), references)
            i += 1
        
        if not self.allow_duplicates:
            remaining_data = copy.copy(data)
            i = 0 
            for element in data:
                remaining_data = remaining_data[1:]
                if element in remaining_data:
                    relative_position = remaining_data.index(element) + 1
                    FL.append(ValidationFinding(
                        path="%s[%d]" % (path, i),
                        message='Element is same as on position %d' % (i + relative_position)))
                i += 1
        return FL
