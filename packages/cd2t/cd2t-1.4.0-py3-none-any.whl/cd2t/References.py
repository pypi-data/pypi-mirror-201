import enum
from cd2t.results import ValidationFinding

class OPT(enum.IntFlag):
    NONE = 1
    UNIQUE = 2
    UNIQUE_GLOBAL = 4
    PRODUCER = 8
    PRODUCER_GLOBAL = 16
    CONSUMER = 32
    CONSUMER_GLOBAL = 64
    ALLOW_ORPHAN_PRODUCER = 128


INIT_OPTIONS = OPT.UNIQUE | OPT.UNIQUE_GLOBAL | OPT.PRODUCER | OPT.PRODUCER_GLOBAL


class ReferenceFinding(ValidationFinding):
    pass
    

class ReferenceError(Exception):
    pass


class ReferenceElement():
    def __init__(self, reference='', path='', value=None, options=INIT_OPTIONS, namespace='') -> None:
        if not isinstance(namespace, str): raise ValueError("'namespace' not a string")
        self.namespace = namespace
        if not isinstance(reference, str): raise ValueError("'reference' not a string")
        self.reference = reference
        if not isinstance(path, str): raise ValueError("'path' not a string")
        self.path = path
        if not isinstance(options, OPT): raise ValueError("'options' not a OPT object")
        self.options = options
        self.value = value
        self.consumes_from = list()
        self.provides_to = list()

class ConsumerElement(ReferenceElement):
    def __init__(self, reference='', path='', value=None, options=INIT_OPTIONS, namespace='', provider_namespace='') -> None:
        super().__init__(reference, path, value, options, namespace)
        self.provider_namespace = provider_namespace
    

class GlobalSpace():
    uOPT = OPT.UNIQUE_GLOBAL
    pOPT = OPT.PRODUCER_GLOBAL
    cOPT = OPT.CONSUMER_GLOBAL

    def __init__(self) -> None:
        self.references = dict()

    def get_uniques_by_value(self, value :any, ref_key :str) -> list[ReferenceElement]:
        return self._get_elements_by_value(value, ref_key, 'uniques')

    def get_producers_by_value(self, value :any, ref_key :str) -> list[ReferenceElement]:
        return self._get_elements_by_value(value, ref_key, 'producers')

    def get_consumers_by_value(self, value :any, ref_key :str) -> list[ReferenceElement]:
        return self._get_elements_by_value(value, ref_key, 'consumers')
    
    def _get_elements_by_value(self, value :any, ref_key :str, _list :str) -> list[ReferenceElement]:
        if ref_key not in self.references.keys():
            return list()
        return [e for e in self.references[ref_key][_list] if e.value == value]

    def get_uniques_by_ref_key(self, ref_key :str) -> list[ReferenceElement]:
        return self.references.get(ref_key, dict()).get('uniques', list())

    def get_producers_by_ref_key(self, ref_key :str) -> list[ReferenceElement]:
        return self.references.get(ref_key, dict()).get('producers', list())

    def get_consumers_by_ref_key(self, ref_key :str) -> list[ReferenceElement]:
        return self.references.get(ref_key, dict()).get('consumers', list())

    def _add_ref_key(self, ref_key :str):
        if ref_key in self.references.keys():
            return
        self.references[ref_key] = dict(
            uniques=list(),
            producers=list(),
            consumers=list()
        )
    
    def add_element(self, new_RE :ReferenceElement) -> list:
        linked_elements = list()
        self._add_ref_key(new_RE.reference)
        if self.uOPT in new_RE.options:
            if self.get_uniques_by_value(new_RE.value, new_RE.reference):
                raise ReferenceError("Reference already defined")
            self.references[new_RE.reference]['uniques'].append(new_RE)
        if self.pOPT in new_RE.options:
            self.references[new_RE.reference]['producers'].append(new_RE)
            linked_elements = self._link_to_consumers(new_RE)
        if self.cOPT in new_RE.options:
            self.references[new_RE.reference]['consumers'].append(new_RE)
            linked_elements = self._link_to_producers(new_RE)
        return linked_elements
    
    def _link_to_producers(self, consumer :ReferenceElement) -> list[ReferenceElement]:
        producer_list = list()
        for producer in self.references[consumer.reference]['producers']:
            if consumer.value == producer.value and producer not in consumer.consumes_from:
                # Maybe linking already from another NS or in Global
                consumer.consumes_from.append(producer)
                producer.provides_to.append(consumer)
                producer_list.append(producer)
        return producer_list
    
    def _link_to_consumers(self, producer :ReferenceElement) -> list[ReferenceElement]:
        consumer_list = list()
        for consumer in self.references[producer.reference]['consumers']:
            if producer.value == consumer.value and consumer not in producer.provides_to:
                # Maybe linking already from another NS or in Global
                producer.provides_to.append(consumer)
                consumer.consumes_from.append(producer)
                consumer_list.append(consumer)
        return consumer_list
    
    def get_producer_consumer_issues(self):
        results = list()
        for ref_key, ref_lists in self.references.items():
            for consumer in ref_lists['consumers']:
                if len(consumer.consumes_from) == 0:
                    # No producer found during analysis!
                    results.append(ReferenceFinding(path=consumer.path,
                                                    message="No provider found"))
            for producer in ref_lists['producers']:
                if OPT.ALLOW_ORPHAN_PRODUCER not in producer.options and len(producer.provides_to) == 0:
                    # Producer has no consumer!
                    results.append(ReferenceFinding(path=producer.path,
                                                    message="Producer has no consumer"))
        return results


class NameSpace(GlobalSpace):
    uOPT = OPT.UNIQUE
    pOPT = OPT.PRODUCER
    cOPT = OPT.CONSUMER


class References():
    def __init__(self, namespace=str()) -> None:
        self.namespace = namespace
        self.globalspace_obj = GlobalSpace()
        self.ns_obj_store = dict()
        self._create_namespace(namespace)
        self.namespace_obj = self.ns_obj_store[namespace]
    
    def change_namespace(self, namespace :str) -> None:
        self._create_namespace(namespace)
        self.namespace_obj = self.ns_obj_store[namespace]
        self.namespace = namespace

    def _create_namespace(self, namespace :str) -> None:
        if namespace not in self.ns_obj_store.keys():
            self.ns_obj_store[namespace] = NameSpace()
    
    def add_element(self, reference :ReferenceElement) -> list:
        reference.namespace = self.namespace
        linked_elements = self.globalspace_obj.add_element(reference)

        if isinstance(reference, ConsumerElement) and reference.provider_namespace:
            self._create_namespace(reference.provider_namespace)
            linked_elements += self.ns_obj_store[reference.provider_namespace].add_element(reference)
        else:
            linked_elements += self.namespace_obj.add_element(reference)
        return linked_elements
    
    def get_producer_consumer_issues(self):
        results = list()
        for namespace, ns_obj in self.ns_obj_store.items():
            _results = ns_obj.get_producer_consumer_issues()
            for r in _results:
                r.path = namespace+" > "+r.path
                results.append(r)
        return results
        
    def same_unique(self, reference :str) -> list[ReferenceElement]:
        others = self.namespace_obj.get_uniques_by_value(
            reference.value, reference.reference)
        if OPT.UNIQUE_GLOBAL in reference.options:
            others += self.globalspace_obj.get_uniques_by_value(
                reference.value, reference.reference)
        if others:
            return others[0]
        return None
