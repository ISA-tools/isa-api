from isatools.create.models import AssayGraph
from collections import OrderedDict


def assay_template_convert_json_to_ordered_dict(assay_template_json):
    res = OrderedDict()
    res['measurement_type'] = assay_template_json['measurement_type']
    res['technology_type'] = assay_template_json['technology_type']
    for name, item in assay_template_json['workflow']:
        res[name] = item
    return res


def assay_template_convert_ordered_dict_to_json(assay_template_odict):
    res = dict()
    res['measurement_type'] = assay_template_odict['measurement_type']
    res['technology_type'] = assay_template_odict['technology_type']
    res['workflow'] = [
        [name, item] for name, item in assay_template_odict.items() if name not in [
            'measurement_type', 'technology_type'
        ]
    ]
    return res
