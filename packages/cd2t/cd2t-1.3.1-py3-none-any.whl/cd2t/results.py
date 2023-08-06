import re


class Finding():
    def __init__(self, message: str, path='') -> None:
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
    

class ValidationFinding(Finding):
    pass


class ReferenceFinding(ValidationFinding):
    def __init__(self, message: str, path='', reference=None) -> None:
        super().__init__(message=message, path=path)
        self.reference = reference


class UniqueErrorFinding(ReferenceFinding):
    pass


class MissingReferenceFinding(ReferenceFinding):
    pass

    
class DataTypeMismatch(ValidationFinding):
    pass
    

class WrongValueFinding(ValidationFinding):
    pass


class FindingsList(list):
    def __str__(self):
        __str_list = list()
        for finding in self:
            __str_list.append(str(finding))
        return '\n'.join( __str_list )
    
    def set_namespace(self, namespace :str):
        for finding in self:
            finding.namespace = namespace 


class AutogenerationInfo(Finding):
    pass


class AutogenerationError(AutogenerationInfo):
    pass