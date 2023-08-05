from cd2t.references import *
from cd2t.types import *
from cd2t.schema import *
import copy


BUILTIN_DATA_TYPES = {
    'any': AnyDataType,
    'bool': Bool,
    'enum': Enum,
    'float': Float,
    'idlist': IDList,
    'integer': Integer,
    'list': List,
    'multitype': Multitype,
    'object': Object,
    'schema': SchemaDataType,
    'string': String
}


class Validator():
    def __init__(self) -> None:
        self._data_type_classes = copy.copy(BUILTIN_DATA_TYPES)
        self._autogen_refs = References()
        self.references = References()
        self._cur_schema = None
        return

    def load_data_type(self, type_name :str, type_class :any) -> None:
        if type_name in self._data_type_classes.keys():
            raise ValueError("Data type '%s' already loaded" % type_name)
        if not issubclass(type_class, BaseDataType):
            raise ValueError("Loading %s failed - not %s" % (type_class, BaseDataType))
        self._data_type_classes[type_name] = type_class
        return
    
    def load_schema(self, schema :dict) -> Schema:
        def verify_schema_format(schema_dic :dict, sub=False, sub_name=''):
            try:
                if not isinstance(schema_dic, dict):
                    raise SchemaError('needs to be an dictionary')
                if 'root' not in schema_dic.keys():
                    raise SchemaError("has no key 'root'")
                root_schema = schema_dic.get('root', None)
                if not isinstance(root_schema, dict):
                    raise SchemaError("root is no mapping")
                if len(root_schema) and 'type' not in root_schema.keys():
                    raise SchemaError("option 'type' in root schema missing")
            except SchemaError as se:
                if sub:
                    raise SchemaError("Subschema '%s' %s" % (sub_name, str(se)))
                raise SchemaError("Schema %s" % str(se))
            root_type_name = root_schema.get('type', None)
            if root_type_name is None:
                root_class = AnyDataType
            else:
                if root_type_name not in self._data_type_classes:
                    raise SchemaError("Schema root type '%s' not found" % str(root_type_name))
                root_class = self._data_type_classes[root_type_name]
            return root_class, root_schema
        
        schema = copy.copy(schema)
        sub_schemas = dict()
        if 'subschemas' in schema.keys():
            sub_schemas = schema['subschemas']
            if not isinstance(sub_schemas, dict):
                raise SchemaError("Schema subschemas is no mapping")
            for sub_name in sub_schemas.keys():
                sub_schema = sub_schemas[sub_name]
                if isinstance(sub_schema, Schema):
                    # This subschema was already verified/translated (recursively)
                    continue
                sub_type_class, sub_type_schema = verify_schema_format(sub_schema, sub=True, sub_name=sub_name)
                sub_type = sub_type_class().build_schema(
                                schema=sub_type_schema, path='->' + sub_name, data_types=self._data_type_classes,
                                subschemas=sub_schemas, subpath=[sub_name]
                            )
                sub_schema_obj = Schema()
                sub_schema_obj.set_root_data_type(sub_type)
                sub_schemas[sub_name] = sub_schema_obj
                
        root_type_class, root_type_schema = verify_schema_format(schema)
        root_type = root_type_class().build_schema(
                schema=root_type_schema, path='', data_types=self._data_type_classes,
                subschemas=sub_schemas, subpath=[]
            )
        schema_obj = Schema()
        schema_obj.set_root_data_type(root_type)
        self._cur_schema = schema_obj
        return schema_obj
    
    def _get_schema_object(self, schema) -> Schema:
        if isinstance(schema, Schema):
            if schema.root_data_type is None:
                if self._cur_schema is None:
                    raise SchemaError('need a schema or ' +\
                                            'Validator object loads a schema first')
                return self._cur_schema
            return schema
        raise SchemaError('Given schema is not a valid schema object')
        
    def change_namespace(self, name :str) -> None:
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError('name needs to be a non empty string')
        self._autogen_refs.change_namespace(str(name))
        self.references.change_namespace(name)
    
    def autogenerate_data(self, data :any, schema=Schema()) -> any:
        schema = self._get_schema_object(schema)
        root_data_type = schema.root_data_type
        return root_data_type.autogenerate_values(
            data=data, path='', references=self._autogen_refs)
    
    def validate_data(self, data :any, schema=Schema()) -> list:
        schema = self._get_schema_object(schema)
        root_data_type = schema.root_data_type
        results = root_data_type.validate_data(
                        data=data, path='', references=self.references)
        if self.references.namespace:
            for result in results:
                result.namespace = self.references.namespace
        return results
    