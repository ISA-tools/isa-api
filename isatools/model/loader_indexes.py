"""Dynamic indexer for the JSON loader feature.
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
        self.processes = {}
        self.term_sources = {}
        self.data_files = {}
        self.other_materials = {}

    return init


def make_print():
    def to_str(self):
        return (
            "LoaderStore:\n\t"
            f"characteristic_categories: {self.characteristic_categories},\n\t"
            f"factors: {self.factors},\n\t"
            f"parameters: {self.parameters},\n\t"
            f"protocols: {self.protocols},\n\t"
            f"units: {self.units},\n\t"
            f"samples: {self.samples},\n\t"
            f"sources: {self.sources},\n\t"
            f"processes: {self.processes},\n\t"
            f"term_sources: {self.term_sources},\n\t"
            f"data_files: {self.data_files},\n\t"
            f"other_materials: {self.other_materials}"
        )

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


def make_reset_method():
    def reset_item(self, index):
        setattr(self, index, {})

    return reset_item


def make_get_resolver(field_target):
    def resolve(self, id_):
        return self.get_item(field_target, id_)

    return resolve


def make_add_resolver(field_target):
    def resolve(self, item):
        self.add_item(field_target, item)

    return resolve


def make_reset_resolver(field_target):
    def resolve(self):
        self.reset_item(field_target)

    return resolve


def make_add_term_source():
    def add_term_source(self, item):
        self.term_sources[item.name] = item

    return add_term_source


def make_get_term_source():
    def get_term_source(self, name):
        return self.term_sources[name]

    return get_term_source


FIELDS = {
    "characteristic_category": "characteristic_categories",
    "factor": "factors",
    "parameter": "parameters",
    "protocol": "protocols",
    "unit": "units",
    "sample": "samples",
    "source": "sources",
    "process": "processes",
    "data_file": "data_files",
    "other_material": "other_materials",
}

methods = {
    "__init__": make_init(),
    "reset_store": make_init(),
    "add_item": make_add_method(),
    "get_item": make_get_method(),
    "reset_item": make_reset_method(),
    "__str__": make_print(),
    "get_term_source": make_get_term_source(),
    "add_term_source": make_add_term_source(),
}

for field_name in FIELDS:
    field = FIELDS[field_name]
    methods["get_%s" % field_name] = make_get_resolver(field)
    methods["add_%s" % field_name] = make_add_resolver(field)
    methods["reset_%s" % field_name] = make_reset_resolver(field)

# parameters of type are 1. class name 2. inheritance as tuple 3. methods and attributes
LoaderStore = type("LoaderStore", (), methods)
loader_states = LoaderStore()


def new_store():
    return LoaderStore()
