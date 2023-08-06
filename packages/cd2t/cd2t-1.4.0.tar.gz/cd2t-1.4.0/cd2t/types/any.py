from cd2t.types.base import BaseDataType 
from cd2t.References import References
from cd2t.results import FindingsList


class AnyDataType(BaseDataType):
    type = 'any'
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        return self

    def validate_data(self, data :any, path :str, references=References()) -> FindingsList:
        return FindingsList()