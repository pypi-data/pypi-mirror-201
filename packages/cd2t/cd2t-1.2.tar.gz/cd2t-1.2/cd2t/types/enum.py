from cd2t.types.base import BaseDataType
from cd2t.references import *
from cd2t.results import *
from cd2t.schema import SchemaError


class Enum(BaseDataType):
    options = [
        # option_name, required, class
        ('allowed_values', True, list, None),
    ]
    supported_data_types = [int, float, dict, list]

    def __init__(self, data_type_classes=dict(), path=str()) -> None:
        super().__init__()
        self.allowed_values = None
    
    def verify_options(self, path: str):
        if not len(self.allowed_values):
            raise SchemaError("'allowed_values' must have at least one element", path)

 
    def verify_data(self, data :any, path :str, references=References()) -> list:
        results = list()
        if data not in self.allowed_values:
            results.append(WrongValueFinding(path=path, message='Value not allowed'))
        return results
