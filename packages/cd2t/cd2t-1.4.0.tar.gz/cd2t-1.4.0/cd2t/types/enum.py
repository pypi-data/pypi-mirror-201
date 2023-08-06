from cd2t.types.base import BaseDataType
from cd2t.References import References
from cd2t.results import WrongValueFinding, FindingsList
from cd2t.schema import SchemaError


class Enum(BaseDataType):
    type = 'enum'
    multi_type_class = True
    options = [
        # option_name, required, class
        ('allowed_values', True, list, None),
    ]
    supported_data_types = [int, float, dict, list, str]

    def __init__(self, data_type_classes=dict(), path=str()) -> None:
        super().__init__()
        self.matching_classes = []
        self.allowed_values = None
        self.data_type_mismatch_message = "None of the allowed value data types matches"
    
    def verify_options(self, path: str):
        if not len(self.allowed_values):
            raise SchemaError("'allowed_values' must have at least one element", path)
        for value in self.allowed_values:
            value_type = type(value)
            if value_type not in self.supported_data_types:
                raise SchemaError("'allowed_values' contains unsupported data types", path)
            if value_type not in self.matching_classes:
                self.matching_classes.append(value_type)

    def verify_data(self, data :any, path :str, references=References()) -> FindingsList:
        FL = FindingsList()
        if data not in self.allowed_values:
            FL.append(WrongValueFinding(path=path, message='Value not allowed'))
        return FL
