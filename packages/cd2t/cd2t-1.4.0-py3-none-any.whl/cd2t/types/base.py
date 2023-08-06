from cd2t.types.datatype import DataType
from cd2t.utils import *
from cd2t.results import *
from cd2t.schema import *
from cd2t.References import *


class BaseDataType(DataType):
    type = ''
    matching_classes = []
    multi_type_class = False
    options = [
        # option_name, required?, class, init_value
    ]
    support_reference = False

    def __init__(self) -> None:
        self.ref_OPT = OPT.NONE
        self.ref_key = ''
        self.data_type_mismatch_message = "Value is not '%s'" % self.type
        return
    
    def data_matches_type(self, data :any) -> bool:
        for cls in self.matching_classes:
            if isinstance(data, cls):
                return True
        return False
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        self.verify_options(path=path)
        return self
    
    def load_reference_option(self, schema :dict, path :str):
        if not self.support_reference or 'reference' not in schema.keys():
            return
        options = schema.pop('reference', None)
        if options is None or not isinstance(options, dict):
            raise SchemaError("Option 'reference' must be a dictionary.", path)
        
        if 'key' not in options.keys():
            raise SchemaError("Option 'key' is required under 'reference'", path)
        self.ref_key = options.pop('key')
        if not isinstance(self.ref_key, str):
            raise SchemaError("Option 'key' under 'reference' must be a string", path)
        
        mode = options.pop('mode', 'unique')
        u_scope = options.pop('unique_scope', 'global')
        p_scope = options.pop('producer_scope', 'global')
        c_scope = options.pop('consumer_scope', 'global')
        orphan = options.pop('allow_orphan_producer', True)
        if mode == 'unique':
            self.ref_OPT = OPT.UNIQUE | OPT.PRODUCER
        elif mode == 'producer':
            self.ref_OPT = OPT.PRODUCER
        elif mode == 'consumer':
            self.ref_OPT = OPT.CONSUMER
        else:
            raise SchemaError("'mode' under 'reference' is unsupported", path)
        if OPT.UNIQUE in self.ref_OPT:
            if u_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.UNIQUE_GLOBAL
            elif u_scope != 'namespace':
                raise SchemaError("Option 'unique_scope' under 'reference' must either 'global' or 'namespace'", path)
        if OPT.PRODUCER in self.ref_OPT:
            if p_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.PRODUCER_GLOBAL
            elif p_scope != 'namespace':
                raise SchemaError("Option 'producer_scope' under 'reference' must either 'global' or 'namespace'", path)
            if orphan:
                self.ref_OPT = self.ref_OPT | OPT.ALLOW_ORPHAN_PRODUCER
        if OPT.CONSUMER in self.ref_OPT:
            if c_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.CONSUMER_GLOBAL
            elif c_scope != 'namespace':
                raise SchemaError("Option 'consumer_scope' under 'reference' must either 'global' or 'namespace'", path)
        if not isinstance(orphan, bool):
            raise SchemaError("'allow_orphan_producer' must be bool", path)
        if len(options):
            raise SchemaError("Unknown 'reference' options '%s'" % ', '.join(options.keys()), path)
    
    def verify_options(self, path :str):
        return
    
    def load_schema_options(self, schema :dict, path :str) -> None:
        schema.pop('type', None)
        for option, required, cls, init_value in self.options:
            if option in schema.keys():
                value = schema[option]
                if not isinstance(value, cls):
                    raise SchemaError("'%s' has wrong value type" % option, path)
                exec("self." + option + " = value")
                schema.pop(option, None)
            elif required:
                raise SchemaError("Option '%s' missing" % option, path)
        if len(schema):
            raise SchemaError("Unknown options '%s'" % ', '.join(schema.keys()), path)
        return

    def validate_data(self, data :any, path :str, references=References()) -> FindingsList:
        FL = FindingsList()
        if not self.data_matches_type(data):
            FL.append(DataTypeMismatch(path=path, message=self.data_type_mismatch_message))
            return FL
        FL += self.verify_reference(data, path, references)
        FL += self.verify_data(data, path, references)
        return FL

    def verify_data(self, data :any, path :str, references :References) -> FindingsList:
        return FindingsList()
    
    def build_sub_references(self, data :any, path :str, references :References) -> None:
        return
    
    def build_references(self, data :any, path :str, references :References) -> None:
        if self.data_matches_type(data):
            self.verify_reference(data=data, path=path, references=references)
            self.build_sub_references(data=data, path=path, references=references)
    
    def autogenerate_data(self, data :any, path :str, references :References):
        return data, FindingsList()
    
    def get_reference_data(self, data :any, path :str) -> any:
        return data, FindingsList()
    
    def get_reference_element(self, path :str, ref_data :any) -> any:
        return ReferenceElement(self.ref_key, path, ref_data, self.ref_OPT)
    
    def verify_reference(self, data :any, path :str, references :References) -> FindingsList:
        FL = FindingsList()
        if not self.support_reference or OPT.NONE in self.ref_OPT:
            return FL
        ref_data, _FL = self.get_reference_data(data, path)
        FL += _FL
        ref_element = self.get_reference_element(path, ref_data)
        if OPT.UNIQUE in self.ref_OPT:
            other = references.same_unique(ref_element)
            if other is not None:
                if other.namespace != references.namespace:
                    _path = "%s > %s" % (other.namespace, other.path)
                else:
                    _path = other.path
                FL.append(ReferenceFinding(
                    path=path,message="Unique value already used at '%s'" % _path))
                return FL
        # If unique or just for producer/consumer mapping, add element to references
        references.add_element(ref_element)
        return FL
