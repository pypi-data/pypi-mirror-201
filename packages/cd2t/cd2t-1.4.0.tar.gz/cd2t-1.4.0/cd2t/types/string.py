from cd2t.types.base import BaseDataType
from cd2t.utils import string_matches_regex_list
from cd2t.schema import SchemaError
from cd2t.results import FindingsList, WrongValueFinding
from cd2t.References import References, OPT, ReferenceElement, ConsumerElement
import re

class String(BaseDataType):
    type = 'string'
    matching_classes = [str]
    support_reference = True
    options = [
        # option_name, required, class
        ('maximum', False, int, None),
        ('minimum', False, int, None),
        ('allowed_values', False, list, None),
        ('not_allowed_values', False, list, list()),
        ('regex_mode', False, bool, False),
        ('regex_multiline', False, bool, False),
        ('regex_fullmatch', False, bool, True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.allowed_values = None
        self.not_allowed_values = list()
        self.regex_mode = False
        self.regex_multiline = False
        self.regex_fullmatch = True
        self.allow_namespace_lookups = False
        self.namespace_separator_char = None
    
    def load_reference_option(self, schema :dict, path :str):
        if not self.support_reference or 'reference' not in schema.keys():
            return
        options = schema.get('reference', None)
        if isinstance(options, dict):
            self.allow_namespace_lookups = options.pop('allow_namespace_lookups', False)
            if not isinstance(self.allow_namespace_lookups, bool):
                raise SchemaError("Option 'allow_namespace_lookups' under 'reference' must be 'bool'", path)
            self.namespace_separator_char = options.pop('namespace_separator_char', None)
            if self.namespace_separator_char is not None and not isinstance(self.namespace_separator_char, str):
                raise SchemaError("Option 'namespace_separator_char' under 'reference' must be 'string'", path)
        super().load_reference_option(schema=schema, path=path)
    
    def verify_options(self, path: str):
        for string in self.not_allowed_values:
            if not isinstance(string, str):
                raise SchemaError("Option 'not_allowed_values' contains non-string", path)
        if self.allowed_values is not None:
            for string in self.allowed_values:
                if not isinstance(string, str):
                    raise SchemaError("Option 'allowed_values' contains non-string", path)
        if self.allow_namespace_lookups:
            if OPT.CONSUMER not in self.ref_OPT:
                raise SchemaError("Namespace lookup needs 'mode' == 'consumer'", path)
            if self.namespace_separator_char is None:
                raise SchemaError("Namespace lookup requires 'namespace_separator_char' to be set", path)
            if not self.namespace_separator_char:
                raise SchemaError("'namespace_separator_char' mustn't be '' (empty)", path)
        
    def verify_data(self, data :any, path :str, reference=References()) -> FindingsList:
        FL = FindingsList()
        if self.minimum is not None and self.minimum > len(data):
            FL.append(WrongValueFinding(
                path=path, message='String length is lower than minimum %d' % self.minimum))
        elif self.maximum is not None and self.maximum < len(data):
            FL.append(WrongValueFinding(
                path=path, message='String length is greater than maximum %d' % self.maximum))
        if self.regex_mode:
            matches = string_matches_regex_list(
                    data, self.not_allowed_values, self.regex_multiline, self.regex_fullmatch)
            if matches:
                FL.append(WrongValueFinding(
                    path=path, message="String matches not allowed regex '%s'" % matches))
            elif self.allowed_values:
                if not string_matches_regex_list(
                        data, self.allowed_values, self.regex_multiline, self.regex_fullmatch):
                    FL.append(WrongValueFinding(
                        path=path, message="String does not match any allowed regex strings"))
        else:
            if self.not_allowed_values and data in self.not_allowed_values:
                FL.append(WrongValueFinding(
                    path=path, message="String is not allowed"))
            if self.allowed_values and data not in self.allowed_values:
                FL.append(WrongValueFinding(
                    path=path, message="String is not allowed"))
        return FL
    
    def get_reference_element(self, path :str, ref_data :any) -> any:
        if OPT.CONSUMER in self.ref_OPT and self.allow_namespace_lookups:
            if self.namespace_separator_char in ref_data:
                provider_ns, value = ref_data.split(self.namespace_separator_char, 1)
                return ConsumerElement(reference=self.ref_key,
                                       path=path,
                                       value=value,
                                       options=self.ref_OPT,
                                       provider_namespace=provider_ns)
        return ReferenceElement(self.ref_key, path, ref_data, self.ref_OPT)
