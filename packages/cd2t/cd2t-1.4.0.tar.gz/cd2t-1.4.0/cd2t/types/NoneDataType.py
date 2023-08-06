from cd2t.types.base import BaseDataType


class NoneDataType(BaseDataType):
    type = 'none'

    def __init__(self) -> None:
        super().__init__()
        self.matching_classes.append(type(None))
