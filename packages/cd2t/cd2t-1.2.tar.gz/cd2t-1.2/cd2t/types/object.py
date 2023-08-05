from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.utils import string_matches_regex_list, regex_matches_in_string_list
from cd2t.references import *
from cd2t.results import *
from cd2t.schema import SchemaError


class Object(BaseDataType):
    matching_class = dict
    support_reference = True
    options = [
        # option_name, required, class, init_value
        ('attributes', False, dict, None),
        ('required_attributes', False, list, list),
        ('dependencies', False, dict, dict()),
        ('reference_attributes', False, list, None),
        ('ignore_undefined_attributes', False, bool, False),
        ('allow_regex_attributes', False, bool, False),
        ('autogenerate', False, bool, True)
    ]

    def __init__(self) -> None:
        super().__init__()
        self.attributes = None
        self.attributes_objects = dict()
        self.required_attributes = list()
        self.dependencies = dict()
        self.reference_attributes = None
        self.ignore_undefined_attributes = False
        self.allow_regex_attributes = False
        self.autogenerate = True
        return
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        if self.attributes is None:
            # No other options should be set:
            for option, required, cls, init_value in self.options:
                if exec("self." + option + " != init_value"):
                    raise SchemaError("Option 'attribute' is omitted, no other option is expected.")
            return self
        if self.reference_attributes is None:
            if self.ref_key and self.allow_regex_attributes:
                raise SchemaError("Reference attributes must be defined if reference is enabled and regex is allowed", path)
            self.reference_attributes = self.attributes
        for req_attr in self.required_attributes:
            if not self._attribute_in_list(req_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                raise SchemaError("Required attribute '%s' not in attributes" % req_attr, path)
        for ref_attr in self.reference_attributes:
            if ref_attr not in self.attributes.keys():
                raise SchemaError("Reference attribute '%s' not in attributes" % ref_attr, path)
        for dep_attr, dep_info in self.dependencies.items():
            if dep_attr not in self.attributes.keys():
                raise SchemaError("Depency attribute '%s' not in attributes" % dep_attr, path)
            if not isinstance(dep_info, dict):
                raise SchemaError("Dependency for '%s' is not a dictionary" % dep_attr, path)
            for req_attr in dep_info.get('requires', []):
                if not self._attribute_in_list(req_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                    raise SchemaError("Required attribute '%s' " % req_attr +\
                                      "for dependency '%s' not in attributes" % dep_attr, path)
            for ex_attr in dep_info.get('excludes', []):
                if not self._attribute_in_list(ex_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                    raise SchemaError("Excluded attribute '%s' " % ex_attr +\
                                      "for dependency '%s' not in attributes" % dep_attr, path)
        #
        if path:
            path = path + '.'
        for a_name, a_schema in self.attributes.items():
            if not isinstance(a_schema, dict):
                raise SchemaError("Attribute '%s' schema is not a dictionary" % a_name, path)
            if 'type' in a_schema.keys():
                type_name = a_schema['type']
                if type_name not in data_types.keys():
                    raise SchemaError("Attribute '%s' data type '%s' not found" % (a_name, type_name), path)
                data_type = data_types[type_name]()
            else:
                data_type = AnyDataType()
            data_type.build_schema(a_schema, path + a_name, data_types, subschemas, subpath)
            self.attributes_objects[a_name] = data_type
        return self
    
    def autogenerate_values(self, data :any, path :str, references :References):
        if data is None or not isinstance(data, dict):
            return data, list()
        new_data = dict()
        results = list()
        for a_name, a_data in data.items():
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                new_data[a_name] = a_data
                continue
            new_path = a_name if not path else "%s.%s" % (path, a_name)
            _data, _results = data_type.autogenerate_values(a_data, new_path, references)
            new_data[a_name] = _data
            results.extend(_results)
        if not self.allow_regex_attributes and self.autogenerate:
            for a_name, data_type in self.attributes_objects.items():
                if a_name not in data.keys():
                    new_path = a_name if not path else "%s.%s" % (path, a_name)
                    _data, _results = data_type.autogenerate_values(
                        data=None, path=new_path, references=references)
                    if _results:
                        new_data[a_name] = _data
                        results.extend(_results)
        return new_data, results
    
    @staticmethod
    def _attribute_in_list(attribute :str, attributes :list, regex_allowed=False) -> bool:
        if regex_allowed:
            return  regex_matches_in_string_list(attribute, attributes)
        elif attribute in attributes:
            return attribute
        return None
    
    def _get_attribute_object(self, name :str, regex_allowed=False) -> bool:
        if regex_allowed:
            name = string_matches_regex_list(string=name,
                                                   regex_list=list(self.attributes_objects.keys()),
                                                   full_match=True)
        return self.attributes_objects.get(name, None)

    def verify_data(self, data :any, path :str, references=References()) -> list:
        results = list()
        if not isinstance(data, dict):
            return [DataTypeMismatch(path=path, message='Value is not an object')]
        if self.attributes is None:
            return list()
        for a_name, a_data in data.items():
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                if self.ignore_undefined_attributes:
                    continue
                results.append(ValidationFinding(path=path, message="Invalid attribute '%s'" % a_name))
                continue
            new_path = a_name if not path else "%s.%s" % (path, a_name)
            results.extend(data_type.validate_data(data=a_data, path=new_path, references=references))
        for req_attr in self.required_attributes:
            found_in_data_keys = False
            if self.allow_regex_attributes:
                if regex_matches_in_string_list(
                                                        regex=req_attr,
                                                        strings=list(data.keys()),
                                                        full_match=True):
                    found_in_data_keys = True
            elif req_attr in data.keys():
                found_in_data_keys = True
            if not found_in_data_keys:
                results.append(ValidationFinding(
                    path = path,
                    message = "Required attribute '%s' missing" % req_attr))
        for attr_name, dep_info in self.dependencies.items():
            if not attr_name in data.keys():
                continue
            for req_attr in dep_info.get('requires', list()):
                if req_attr not in data.keys():
                    results.append(ValidationFinding(
                        path = path,
                        message = "Required attribute '%s' for attribute '%s' missing" % (req_attr, attr_name)))
            for ex_attr in dep_info.get('excludes', list()):
                if ex_attr in data.keys():
                    results.append(ValidationFinding(
                        path = path,
                        message = "Excluded attribute '%s' for attribute '%s' found" % (ex_attr, attr_name)))
        return results
    
    def get_reference_data(self, data: any, path :str) -> any:
        ref_data = list()
        results = list()
        for ref_attr in self.reference_attributes:
            if ref_attr not in data.keys():
                results.append(ValidationFinding(path = path,
                                           message = "Reference attribute '%s' missing" % ref_attr))
            ref_data.append(data[ref_attr])
        return ref_data, results
