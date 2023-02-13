def make_get_table_method(target: type) -> callable:
    @staticmethod
    def get_table():
        return target
    return get_table


def get_characteristic_categories(categories):
    characteristics_categories = []
    for characteristic in categories:
        id_ = characteristic.ontology_annotation_id
        id_ = '#characteristic_category/' + id_ if not id_.startswith('#characteristic_category/') else id_
        characteristic_to_append = {'@id': id_, 'characteristicType': characteristic.to_json()}
        characteristics_categories.append(characteristic_to_append)
    return characteristics_categories
