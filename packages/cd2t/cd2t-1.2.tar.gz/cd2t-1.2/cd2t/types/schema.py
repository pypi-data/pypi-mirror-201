from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.schema import *
import copy

class SchemaDataType(BaseDataType):
    options = [
        # option_name, required, class
        ('subschema', True, str, ''),
    ]

    def __init__(self, data_type_classes=dict(), path=str()) -> None:
        super().__init__()
        self.subschema = ''
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.load_schema_options(schema, path)
        _sub_schema = subschemas.get(self.subschema, None)
        if _sub_schema is None:
            raise SchemaError("Could not found subschema '%s'" % self.subschema, path)
        if self.subschema in subpath:
            raise SchemaError("Subschema loop detected '%s'"
                                    % "'->'".join(subpath + [self.subschema]), path)
        new_subpath = copy.copy(subpath)
        new_subpath.append(self.subschema)
        if isinstance(_sub_schema, Schema):
            # Subschema was already build.
            return _sub_schema.root_data_type
        sub_root_schema = _sub_schema.get('root', None)
        if sub_root_schema is None:
            raise SchemaError("Subschema '%s' has no key 'root'" % self.subschema, path)
        if not isinstance(sub_root_schema, dict):
            raise SchemaError("Subschema '%s' root is not a mapping" % self.subschema, path)
        if len(sub_root_schema) == 0:
            # Empty dict --> type 'any'
            sub_data_obj = AnyDataType()
        else:
            if 'type' not in sub_root_schema.keys():
                raise SchemaError("Subschema '%s' root has no key 'type'" % self.subschema, path)
            sub_data_class = data_types.get(sub_root_schema['type'], None)
            if sub_data_class is None:
                raise SchemaError("Subschema '%s' root data type '%s' not found"
                                        % (self.subschema, sub_root_schema['type']), path)
            sub_data_obj = sub_data_class().build_schema(
                                schema=sub_root_schema, path=path + '->' + self.subschema,
                                data_types=data_types,
                                subschemas=subschemas, subpath=new_subpath)
        sub_schema_obj = Schema()
        sub_schema_obj.set_root_data_type(sub_data_obj)
        subschemas[self.subschema] = sub_schema_obj
        return sub_data_obj
    