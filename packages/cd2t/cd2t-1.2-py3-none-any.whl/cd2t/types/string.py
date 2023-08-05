from cd2t.types.base import BaseDataType
from cd2t.utils import string_matches_regex_list
from cd2t.schema import SchemaError
from cd2t.results import *
from cd2t.references import *
import re

class String(BaseDataType):
    matching_class = str
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
    
    def verify_options(self, path: str):
        for string in self.not_allowed_values:
            if not isinstance(string, str):
                raise SchemaError("%s: Option 'not_allowed_values' contains non-string" % path)
        if self.allowed_values is not None:
            for string in self.allowed_values:
                if not isinstance(string, str):
                    raise SchemaError("%s: Option 'allowed_values' contains non-string" % path)
        
    def verify_data(self, data :any, path :str, reference=References()) -> list:
        if not isinstance(data, str):
            return [DataTypeMismatch(path, 'Value is not a string')]
        if self.minimum is not None and self.minimum > len(data):
            return [WrongValueFinding(path, 'String length is lower than minimum %d' % self.minimum)]
        if self.maximum is not None and self.maximum < len(data):
            return [WrongValueFinding(path, 'String length is greater than maximum %d' % self.maximum)]
        if self.regex_mode:
            matches = string_matches_regex_list(
                    data, self.not_allowed_values, self.regex_multiline, self.regex_fullmatch)
            if matches:
                return [WrongValueFinding(path, "String matches not allowed regex '%s'" % matches)]
            elif self.allowed_values:
                if not string_matches_regex_list(
                        data, self.allowed_values, self.regex_multiline, self.regex_fullmatch):
                    return [WrongValueFinding(path, "String does not match any allowed regex strings")]
        else:
            if self.not_allowed_values and data in self.not_allowed_values:
                return [WrongValueFinding(path, "String is not allowed")]
            if self.allowed_values and data not in self.allowed_values:
                return [WrongValueFinding(path, "String is not allowed")]
        return []
