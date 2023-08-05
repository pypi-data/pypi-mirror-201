import re


class ValidationFinding():
    def __init__(self, path :str, message: str) -> None:
        self.path = path
        self.message = message
        self.namespace = ''

    def __str__(self) -> str:
        _str = self.message
        if self.path:
            _str = self.path + ': ' + _str
        if self.namespace:
            _str = self.namespace + ' > ' + _str
        return _str
    
    def __eg__(self, other):
        return str(self) == str(other)
    
    def __gt__(self, other):
        return str(self > str(other))
    
    def __lt__(self, other):
        return str(self) < str(other)


class ReferenceFinding(ValidationFinding):
    def __init__(self, path: str, message: str, reference=None) -> None:
        super().__init__(path, message)
        self.reference = reference


class UniqueErrorFinding(ReferenceFinding):
    pass


class MissingReferenceFinding(ReferenceFinding):
    pass


class DataFinding(ValidationFinding):
    pass
    

class DataTypeMismatch(DataFinding):
    pass
    

class WrongValueFinding(DataFinding):
    pass


class AutogenerationInfo():
    def __init__(self, path :str, message :str, reference :dict) -> None:
        self.reference = reference
        self.path = path
        self.message = message
        return
    
    def __str__(self) -> str:
        r_str = self.message
        if self.path:
            r_str = "%s: %s" % (self.path, r_str)
        return r_str


class AutogenerationError(AutogenerationInfo):
    pass