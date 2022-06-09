""" Dynamic indexer for the JSON loader feature.
Getters are:
    - get_item(field, itemID)
    - get_characteristic_category(itemID)
    - get_factor(itemID)
    - get_parameter(itemID)
    - get_protocol(itemID)
    - get_unit(itemID)
    - get_sample(itemID)
    - get_source(itemID)
Setters are:
    - add_item(field, itemID)
    - add_characteristic_category(itemID)
    - add_factor(itemID)
    - add_parameter(itemID)
    - add_protocol(itemID)
    - add_unit(itemID)
    - add_sample(itemID)
    - add_source(itemID)
After loading a resource, reset the store with self.reset_store()

Author: Terazus
"""


def make_init():
    def init(self):
        self.characteristic_categories = {}
        self.factors = {}
        self.parameters = {}
        self.protocols = {}
        self.units = {}
        self.samples = {}
        self.sources = {}
    return init


def make_print():
    def to_str(self):
        return ("LoaderStore:\n\t"
                "characteristic_categories: {indexes.characteristic_categories},\n\t"
                "factors: {indexes.factors},\n\t"
                "parameters: {indexes.parameters},\n\t"
                "protocols: {indexes.protocols},\n\t"
                "units: {indexes.units},\n\t"
                "samples: {indexes.samples},\n\t"
                "sources: {indexes.sources}").format(indexes=self)
    return to_str


def make_add_method():
    def add_item(self, index, item):
        getattr(self, index)[item.id] = item
    return add_item


def make_get_method():
    def get_item(self, index, id_):
        item = getattr(self, index)[id_]
        return item
    return get_item


def make_get_resolver(field_target):
    def resolve(self, id_):
        return self.get_item(field_target, id_)
    return resolve


def make_add_resolver(field_target):
    def resolve(self, id_):
        self.add_item(field_target, id_)
    return resolve


FIELDS = {
    "characteristic_category": 'characteristic_categories',
    "factor": 'factors',
    "parameter": "parameters",
    "protocol": "protocols",
    "unit": "units",
    "sample": "samples",
    "source": "sources"
}

methods = {
    '__init__': make_init(),
    'reset_store': make_init(),
    'add_item': make_add_method(),
    'get_item': make_get_method(),
    '__str__': make_print()
}

for field_name in FIELDS:
    field = FIELDS[field_name]
    methods['get_%s' % field_name] = make_get_resolver(field)
    methods['add_%s' % field_name] = make_add_resolver(field)

# parameters of type are 1. class name 2. inheritance as tuple 3. methods and attributes
Store = type('LoaderStore', (), methods)
loader_states = Store()


def new_store():
    return Store()

