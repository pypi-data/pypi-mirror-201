from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.references import *
from cd2t.results import *
from cd2t.schema import SchemaError
import re


class IDList(BaseDataType):
    matching_class = dict
    support_reference = True
    options = [
        # option_name, required, class
        ('minimum', False, int, None),
        ('maximum', False, int, None),
        ('elements', True, dict, None),
        ('id_type', False, str, 'string'),
        ('id_minimum', False, int, None),
        ('id_maximum', False, int, None),
        ('allowed_ids', False, list, None),
        ('not_allowed_ids', False, list, list()),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.type = None
        self.minimum = None
        self.maximum = None
        self.elements = None
        self.element_type = None
        self.id_type = 'string'
        self.id_minimum = None
        self.id_maximum = None
        self.allowed_ids = None
        self.not_allowed_ids = list()
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        if self.id_type not in ['string', 'integer']:
            raise SchemaError("id_type '%s' is not valid" % self.id_type, path)
        if 'type' in self.elements.keys():
            element_type_name = self.elements['type']
            if element_type_name not in data_types:
                raise SchemaError("Elements data type '%s' not found" % element_type_name, path)
            self.element_type = data_types[element_type_name]()
        elif self.elements:
            raise SchemaError("'type' not found in elements schema", path)
        else:
            self.element_type = AnyDataType()
        self.element_type.build_schema(schema=self.elements, path=path+'<.>',
                                       data_types=data_types, subschemas=subschemas, subpath=subpath)
        return self
    
    def autogenerate_values(self, data :any, path :str, references :References):
        if not isinstance(data, dict):
            return data, list()
        new_dict = dict()
        results = list()
        for id, element in data.items():
            new_path = str(id) if not path else "%s.%s" % (path, str(id))
            _data, _results = self.element_type.autogenerate_values(data=element,
                                                            path=new_path,
                                                            references=references)
            new_dict[id] = _data
            results.extend(_results)
        return new_dict, results

    def verify_data(self, data :any, path :str, references=References()) -> list:
        if not isinstance(data, dict):
            return [DataTypeMismatch(path=path, message="Value is not an ID list")]
        results = list()
        if self.minimum and len(data) < self.minimum:
            results.append(WrongValueFinding(
                        path=path,
                        message='Attribute (ID) count is lower than minimum %d' % self.minimum))
        if self.maximum is not None and len(data) > self.maximum:
            results.append(WrongValueFinding(
                        path=path,
                        message='Attribute (ID) count is greater than maximum %d' % self.maximum))

        for id, element in data.items():
            _results = list()
            if self.id_type == 'string':
                if not isinstance(id, str):
                    _results.append(WrongValueFinding(
                        path=path, message="Attribute (ID) '%s' is not a string" % str(id)))
                elif self.id_minimum and len(id) < self.id_minimum:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="String length of attribute (ID) '%s' is lower than minimum %d" %
                                (id, self.id_minimum)))
                elif self.id_maximum is not None and len(id) > self.id_maximum:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="String length of attribute (ID) '%s' is greater than maximum %d" %
                                (id, self.id_maximum)))
                else:
                    not_allowed = False
                    for regex in self.not_allowed_ids:
                        if re.match(regex, id):
                            _results.append(WrongValueFinding(
                                path=path,
                                message="Attribute '%s' is not allowed" % id))
                            not_allowed = True
                    if not not_allowed and self.allowed_ids:
                        allowed = False
                        for regex in self.allowed_ids:
                            if re.match(regex, id):
                                allowed = True
                                break
                        if not allowed:
                            _results.append(WrongValueFinding(
                                    path=path,
                                    message="Attribute '%s' does not match any allowed value" % id))
                    
            else: # id_type == 'integer'
                if not isinstance(id, int):
                    _results.append(WrongValueFinding(
                        path=path, message="Attribute (ID) '%s' is not a integer" % str(id)))
                elif self.id_minimum and id < self.id_minimum:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="Attribute (ID) '%d' is lower than minimum %d" % (id, self.id_minimum)))
                elif self.id_maximum is not None and id > self.id_maximum:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="Attribute (ID) '%d' is greater than maximum %d" % (id, self.id_maximum)))
                elif id in self.not_allowed_ids:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="Attribute (ID) '%d' is not allowed" % id, ))
                elif self.allowed_ids and id not in self.allowed_ids:
                    _results.append(WrongValueFinding(
                        path=path,
                        message="Attribute (ID) '%d' is not an allowed value" % id, ))

            if not _results:
                new_path = str(id) if not path else "%s.%s" % (path, str(id))
                results.extend(self.element_type.validate_data(
                    data=element, path=new_path, references=references))
            else:
                results.extend(_results)
        return results

    def verify_reference(self, data :any, path :str, references=References()) -> list:
        if not isinstance(data, dict) or OPT.NONE in self.ref_OPT:
            return []
        results = list()
        for id in data.keys():
            element = ReferenceElement(self.ref_key, path, id, self.ref_OPT)
            other = references.same_unique(element)
            if other is not None:
                if references.namespace != other.namespace:
                    _path = "%s > %s" % (other.namespace, other.path)
                else:
                    _path = other.path
                results.append(UniqueErrorFinding(path=path, message="ID '%s' already used at '%s'" % (str(id), _path)))
            else:
                references.add_element(element)
        return results
