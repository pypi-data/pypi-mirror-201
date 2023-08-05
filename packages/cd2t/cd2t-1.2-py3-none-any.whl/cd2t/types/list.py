from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.results import *
from cd2t.references import *
from cd2t.schema import SchemaError
import copy

class List(BaseDataType):
    matching_class = list
    options = [
        # option_name, required, class
        ('minimum', False, int, None),
        ('maximum', False, int, None),
        ('allow_duplicates', False, bool, True),
        ('elements', True, dict, dict()),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.matching_classes = [list]
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
        self.element_data_type.build_schema(schema=self.elements,
                                            path=path+"[.]",
                                            data_types=data_types,
                                            subschemas=subschemas,
                                            subpath=subpath)
        return self
    
    def autogenerate_values(self, data :any, path :str, references :References):
        if not isinstance(data, list):
            return data, list()
        new_list = list()
        results = list()
        i = 0
        for element in data:
            _data, _results = self.element_data_type.autogenerate_values(
                element, "%s[%d]" % (path, i), references)
            new_list.append(_data)
            results.extend(_results)
            i += 1
        return new_list, results

    def verify_data(self, data :any, path :str, references=References()) -> list:
        if not isinstance(data, list):
            return [DataTypeMismatch(path=path, message='Value is not a list.')]
        results = list()
        if self.minimum and len(data) < self.minimum:
            results.append(WrongValueFinding(
                        path=path,
                        message='Length of list is lower than %d' % self.minimum))
        if self.maximum and len(data) > self.maximum:
            results.append(WrongValueFinding(
                        path=self.path,
                        message='Length of list is greater than %d' % self.maximum))
        i = 0
        for element in data:
            results.extend(self.element_data_type.validate_data(
                element, "%s[%d]" % (path, i), references))
            i += 1
        
        if not self.allow_duplicates:
            remaining_data = copy.copy(data)
            i = 0 
            for element in data:
                remaining_data = remaining_data[1:]
                if element in remaining_data:
                    relative_position = remaining_data.index(element) + 1
                    results.append(ValidationFinding(
                        path="%s[%d]" % (path, i),
                        message='Element is same as on position %d' % (i + relative_position)))
                i += 1
        return results
