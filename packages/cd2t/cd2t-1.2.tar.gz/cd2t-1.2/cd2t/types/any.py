from cd2t.types.base import BaseDataType 
from cd2t.references import *


class AnyDataType(BaseDataType):
    matching_class = None
    options = []
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        return self
    

    def validate_data(self, data :any, path :str, references=References()) -> list:
        return list()