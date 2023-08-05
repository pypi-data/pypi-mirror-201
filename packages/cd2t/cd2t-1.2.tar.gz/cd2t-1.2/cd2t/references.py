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


class References():
    def __init__(self, namespace=str()) -> None:
        # Current data namespace
        self.namespace = namespace
        self.namespaces = {
            namespace: dict(
                unique=list(),   # list of ReferenceElements for unique checks
                producer=list(), # list of providing ReferenceElements
                consumer=list()  # list of consuming ReferenceElements
            )
        }

        #namespace local reference information
        self.unique = self.namespaces[namespace]['unique']
        self.producer = self.namespaces[namespace]['producer']
        self.consumer = self.namespaces[namespace]['consumer']

        # global reference information
        self.global_unique = list() # list of ReferenceElements for unique checks
        self.global_producer = list() # list of providing ReferenceElements
        self.global_consumer = list() # list of consuming ReferenceElements
    
    def change_namespace(self, namespace :str) -> None:
        if self.namespace == namespace:
            return
        if namespace not in self.namespaces.keys():
            self.namespaces[namespace] = dict(
                unique=list(),   # list of ReferenceElements for unique checks
                producer=list(), # list of providing ReferenceElements
                consumer=list()  # list of consuming ReferenceElements
            )
        
        self.unique = self.namespaces[namespace]['unique']
        self.producer = self.namespaces[namespace]['producer']
        self.consumer = self.namespaces[namespace]['consumer']
        
        self.namespace = namespace
    
    def _link_to_producers(self, consumer :ReferenceElement) -> list[ReferenceElement]:
        if not OPT.CONSUMER in consumer.options:
            return list()
        consumer_list = list()
        # Linking within namespace
        for provider in self.producer:
            if consumer.reference == provider.reference and consumer.value == provider.value:
                consumer.consumes_from.append(provider)
                provider.provides_to.append(consumer)
                consumer_list.append(provider)
        if OPT.CONSUMER_GLOBAL not in consumer.options:
          return consumer_list
        # Linking to global
        for provider in self.global_producer:
            if consumer.reference == provider.reference and consumer.value == provider.value:
                if consumer in provider.provides_to:
                    # global provider is the same as the one already found in namespace
                    continue
                consumer.consumes_from.append(provider)
                provider.provides_to.append(consumer)
                consumer_list.append(provider)
        return consumer_list
    
    def _link_to_consumers(self, producer :ReferenceElement) -> list[ReferenceElement]:
        if not OPT.PRODUCER in producer.options:
            return list()
        consumer_list = list()
        # Linking within namespace
        for consumer in self.consumer:
            if producer.reference == consumer.reference and producer.value == consumer.value:
                producer.provides_to.append(consumer)
                consumer.consumes_from.append(producer)
                consumer_list.append(consumer)
        if OPT.CONSUMER_GLOBAL not in producer.options:
          return consumer_list
        # Linking to global
        for consumer in self.global_producer:
            if producer.reference == consumer.reference and producer.value == consumer.value:
                if producer in consumer.provides_to:
                    # global consumer is the same as the one already found in namespace
                    continue
                producer.provides_to.append(consumer)
                consumer.consumes_from.append(producer)
                consumer_list.append(consumer)
        return consumer_list
    
    def add_element(self, reference :ReferenceElement) -> list:
        linked_elements = list()
        reference.namespace = self.namespace
        if OPT.UNIQUE in reference.options:
            if self.same_unique(reference):
                raise ReferenceError("Reference already defined")
            self.unique.append(reference)
            if OPT.UNIQUE_GLOBAL in reference.options:
                self.global_unique.append(reference)
        if OPT.PRODUCER in reference.options:
            self.producer.append(reference)
            if OPT.PRODUCER_GLOBAL in reference.options:
                self.global_producer.append(reference)
            linked_elements = self._link_to_consumers(reference)
        if OPT.CONSUMER in reference.options:
            self.consumer.append(reference)
            if OPT.CONSUMER_GLOBAL in reference.options:
                self.global_consumer.append(reference)
            linked_elements = self._link_to_producers(reference)
        return linked_elements
            
    def same_unique(self, reference :ReferenceElement):
        for ref in self.unique:
            if reference.reference == ref.reference and reference.value == ref.value:
                return ref
        if OPT.UNIQUE_GLOBAL not in reference.options:
            return None
        for ref in self.global_unique:
            if reference.reference == ref.reference and reference.value == ref.value:
                return ref
        return None
    
    def get_producer_consumer_issues(self):
        results = list()
        for namespace, ref_lists in self.namespaces.items():
            for consumer in ref_lists['consumer']:
                if len(consumer.consumes_from) == 0:
                    # No producer found during analysis!
                    results.append(ReferenceFinding(path=namespace+" > "+consumer.path,
                                                    message="No provider found"))
            for producer in ref_lists['producer']:
                if OPT.ALLOW_ORPHAN_PRODUCER not in producer.options and len(producer.provides_to) == 0:
                    # Producer has no consumer!
                    results.append(ReferenceFinding(path=namespace+" > "+producer.path,
                                                    message="Producer has no consumer"))
        return results