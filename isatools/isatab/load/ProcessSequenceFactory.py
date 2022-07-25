from isatools.isatab.utils import process_keygen, find_lt, find_gt, pairwise,  get_object_column_map, get_value
from isatools.isatab.defaults import (
    log,
    _RX_COMMENT,
    _LABELS_MATERIAL_NODES,
    _LABELS_DATA_NODES,
    _RX_CHARACTERISTICS,
    _RX_FACTOR_VALUE,
    _LABELS_ASSAY_NODES,
    _RX_PARAMETER_VALUE
)
from isatools.model import (
    OntologyAnnotation,
    Comment,
    Material,
    Characteristic,
    Source,
    Sample,
    DataFile,
    FactorValue,
    Process,
    ParameterValue,
    plink
)


def preprocess(DF):
    """Check headers, and insert Protocol REF if needed

    :param DF: Table DataFrame
    :return: Processed DataFrame
    """
    columns = DF.columns
    process_node_name_indices = [x for x, y in enumerate(columns) if y in _LABELS_ASSAY_NODES]
    missing_process_indices = list()
    protocol_ref_cols = [x for x in columns if x.startswith('Protocol REF')]
    num_protocol_refs = len(protocol_ref_cols)
    indexes = _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES + _LABELS_ASSAY_NODES + protocol_ref_cols
    all_cols_indicies = [i for i, c in enumerate(columns) if c in indexes]

    for i in process_node_name_indices:
        if not columns[find_lt(all_cols_indicies, i)].startswith('Protocol REF'):
            log.info('warning: Protocol REF missing between \'{}\' and \'{}\''
                     .format(columns[find_lt(all_cols_indicies, i)], columns[i]))
            missing_process_indices.append(i)

    # insert Protocol REF columns
    offset = 0

    for i in reversed(missing_process_indices):
        leftcol = columns[find_lt(all_cols_indicies, i)]
        rightcol = columns[i]
        # Force use of unknown protocol always, until we can insert missing
        # protocol from above inferences into study metadata
        inferred_protocol_type = ''
        log.info('Inserting protocol {} in between {} and {}'
                 .format(inferred_protocol_type if inferred_protocol_type != '' else 'unknown', leftcol, rightcol))
        DF.insert(i, 'Protocol REF.{}'.format(num_protocol_refs + offset),
                  'unknown' if inferred_protocol_type == '' else inferred_protocol_type)
        DF.isatab_header.insert(i, 'Protocol REF')
        offset += 1
    return DF


class ProcessSequenceFactory:
    """The ProcessSequenceFactory is used to parse the tables and build the
    process sequences representing the experimental graphs"""

    def __init__(self, ontology_sources=None, study_samples=None,
                 study_protocols=None, study_factors=None):
        self.ontology_sources = ontology_sources
        self.samples = study_samples
        self.protocols = study_protocols
        self.factors = study_factors

    def create_from_df(self, DF):
        """Create the process sequences from the table DataFrame

        :param DF: Table DataFrame
        :return: List of Processes coressponding to the process sequences. The
        Processes are linked appropriately to all other ISA content objects,
        such as Samples, DataFiles, and to each other.
        """
        DF = preprocess(DF=DF)

        ontology_source_map = {}
        protocol_map = {}
        sources = {}
        other_material = {}
        data = {}
        processes = {}
        characteristic_categories = {}
        unit_categories = {}
        samples = {}

        if self.ontology_sources is not None:
            ontology_source_map = dict(map(lambda x: (x.name, x), self.ontology_sources))
        if self.protocols is not None:
            protocol_map = dict(map(lambda x: (x.name, x), self.protocols))

        try:
            sources = dict(map(lambda x: ('Source Name:' + x, Source(name=x)),
                               [x for x in DF['Source Name'].drop_duplicates() if x != '']))
        except KeyError:
            pass

        try:
            if self.samples is not None:
                sample_map = dict(map(lambda x: ('Sample Name:' + x.name, x), self.samples))
                sample_keys = list(map(lambda x: 'Sample Name:' + x,
                                       [str(x) for x in DF['Sample Name'].drop_duplicates() if x != '']))
                for k in sample_keys:
                    try:
                        samples[k] = sample_map[k]
                    except KeyError:
                        log.warning('warning! Did not find sample referenced at assay level in study samples')
            else:
                samples = dict(
                    map(lambda x: ('Sample Name:' + x, Sample(name=x)),
                        [str(x) for x in DF['Sample Name'].drop_duplicates() if x != '']))
        except KeyError:
            pass

        try:
            extracts = dict(
                map(lambda x: ('Extract Name:' + x, Material(name=x, type_='Extract Name')),
                    [x for x in DF['Extract Name'].drop_duplicates() if x != '']))
            other_material.update(extracts)
        except KeyError:
            pass

        try:
            if 'Labeled Extract Name' in DF.columns:
                try:
                    category = characteristic_categories['Label']
                except KeyError:
                    category = OntologyAnnotation(term='Label')
                    characteristic_categories['Label'] = category
                for _, lextract_name in DF['Labeled Extract Name'].drop_duplicates().iteritems():
                    if lextract_name != '':
                        lextract = Material(name=lextract_name, type_='Labeled Extract Name')
                        lextract.characteristics = [
                            Characteristic(category=category, value=OntologyAnnotation(term=DF.loc[_, 'Label']))
                        ]
                        other_material['Labeled Extract Name:' + lextract_name] = lextract
        except KeyError:
            pass

        for data_col in [x for x in DF.columns if x.endswith(" File")]:
            filenames = [x for x in DF[data_col].drop_duplicates() if x != '']
            data.update(dict(map(lambda x: (':'.join([data_col, x]), DataFile(filename=x, label=data_col)), filenames)))

        node_cols = [i for i, c in enumerate(DF.columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]
        proc_cols = [i for i, c in enumerate(DF.columns) if c.startswith("Protocol REF")]

        try:
            object_column_map = get_object_column_map(DF.isatab_header, DF.columns)
        except AttributeError:
            object_column_map = get_object_column_map(DF.columns, DF.columns)

        def get_node_by_label_and_key(labl, this_key):
            n = None
            lk = labl + ':' + this_key
            if labl == 'Source Name':
                n = sources[lk]
            if labl == 'Sample Name':
                n = samples[lk]
            elif labl in ('Extract Name', 'Labeled Extract Name'):
                n = other_material[lk]
            elif labl.endswith(' File'):
                n = data[lk]
            return n

        for _cg, column_group in enumerate(object_column_map):
            # for each object, parse column group

            object_label = column_group[0]

            if object_label in _LABELS_MATERIAL_NODES:

                for _, object_series in DF[column_group].drop_duplicates().iterrows():
                    node_name = str(object_series[object_label])
                    node_key = ":".join([object_label, node_name])
                    material = None
                    if object_label == "Source Name":
                        try:
                            material = sources[node_key]
                        except KeyError:
                            pass  # skip if object not found
                    elif object_label == "Sample Name":
                        try:
                            material = samples[node_key]
                        except KeyError:
                            pass  # skip if object not found
                    else:
                        try:
                            material = other_material[node_key]
                        except KeyError:
                            pass  # skip if object not found

                    if material is not None:

                        for charac_column in [c for c in column_group if c.startswith('Characteristics[')]:
                            category_key = next(iter(_RX_CHARACTERISTICS.findall(charac_column)))
                            try:
                                category = characteristic_categories[category_key]
                            except KeyError:
                                category = OntologyAnnotation(term=category_key)
                                characteristic_categories[category_key] = category

                            characteristic = Characteristic(category=category)

                            v, u = get_value(
                                charac_column, column_group, object_series,
                                ontology_source_map, unit_categories)

                            characteristic.value = v
                            characteristic.unit = u

                            if characteristic.category.term in [
                                x.category.term
                                for x in material.characteristics]:
                                log.warning(
                                    'Duplicate characteristic found for '
                                    'material, skipping adding to material '
                                    'object')
                            else:
                                material.characteristics.append(characteristic)

                        for comment_column in [c for c in column_group if c.startswith('Comment[')]:
                            comment_key = next(iter(_RX_COMMENT.findall(comment_column)))
                            if comment_key not in [x.name for x in material.comments]:
                                comment = Comment(name=comment_key, value=str(object_series[comment_column]))
                                material.comments.append(comment)

                for _, object_series in DF.drop_duplicates().iterrows():
                    node_name = str(object_series['Sample Name'])
                    node_key = ":".join(['Sample Name', node_name])
                    material = None
                    try:
                        material = samples[node_key]
                    except KeyError:
                        pass  # skip if object not found

                    if isinstance(material, Sample) and self.factors is not None:
                        for fv_column in [c for c in DF.columns if c.startswith('Factor Value[')]:
                            category_key = next(iter(_RX_FACTOR_VALUE.findall(fv_column)))
                            factor_hits = [f for f in self.factors if f.name == category_key]

                            if len(factor_hits) != 1:
                                raise ValueError('Could not resolve Study Factor from Factor Value ', category_key)

                            factor = factor_hits[0]
                            fv = FactorValue(factor_name=factor)
                            v, u = get_value(fv_column, DF.columns, object_series, ontology_source_map, unit_categories)
                            fv.value = v
                            fv.unit = u
                            fv_set = set(material.factor_values)
                            fv_set.add(fv)
                            material.factor_values = list(fv_set)

            elif object_label in _LABELS_DATA_NODES:
                for _, object_series in DF[column_group].drop_duplicates().iterrows():
                    try:
                        data_file = get_node_by_label_and_key(object_label, str(object_series[object_label]))
                        for comment_column in [c for c in column_group if c.startswith('Comment[')]:
                            comment_key = next(iter(_RX_COMMENT.findall(comment_column)))
                            if comment_key not in [x.name for x in data_file.comments]:
                                comment = Comment(name=comment_key, value=str(object_series[comment_column]))
                                data_file.comments.append(comment)
                    except KeyError:
                        pass  # skip if object not found

            elif object_label.startswith('Protocol REF'):
                object_label_index = list(DF.columns).index(object_label)

                # don't drop duplicates
                for _, object_series in DF.iterrows():
                    protocol_ref = str(object_series[object_label])
                    process_key = process_keygen(protocol_ref, column_group, _cg, DF.columns, object_series, _, DF)

                    # TODO: Keep process key sequence here to reduce number of
                    # passes on Protocol REF columns?

                    try:
                        process = processes[process_key]
                    except KeyError:
                        process = Process(executes_protocol=protocol_ref)
                        processes.update(dict([(process_key, process)]))

                    output_node_index = find_gt(node_cols, object_label_index)
                    output_proc_index = find_gt(proc_cols, object_label_index)

                    post_chained_protocol = any(
                        col_name for col_name in DF.columns[(object_label_index + 1): output_node_index].values
                        if col_name.startswith('Protocol REF')
                    )

                    if (output_proc_index < output_node_index > -1 and not post_chained_protocol) \
                            or (output_proc_index > output_node_index):

                        output_node_label = DF.columns[output_node_index]
                        output_node_value = str(object_series[output_node_label])
                        node_key = output_node_value
                        output_node = None
                        try:
                            output_node = get_node_by_label_and_key(output_node_label, node_key)
                        except KeyError:
                            pass  # skip if object not found

                        if output_node is not None and output_node not in process.outputs:
                            process.outputs.append(output_node)

                    input_node_index = find_lt(node_cols, object_label_index)
                    input_proc_index = find_lt(proc_cols, object_label_index)

                    previous_chained_protocol = any(
                        col_name for col_name in DF.columns[input_node_index: (object_label_index - 1)].values
                        if col_name.startswith('Protocol REF')
                    )

                    if input_proc_index < input_node_index > -1 and not previous_chained_protocol:
                        input_node_label = DF.columns[input_node_index]
                        input_node_value = str(object_series[input_node_label])
                        node_key = input_node_value
                        input_node = None
                        try:
                            input_node = get_node_by_label_and_key(input_node_label, node_key)
                        except KeyError:
                            pass  # skip if object not found

                        if input_node is not None and input_node not in process.inputs:
                            process.inputs.append(input_node)

                    name_column_hits = [n for n in column_group if n in _LABELS_ASSAY_NODES]
                    if len(name_column_hits) == 1:
                        process.name = str(object_series[name_column_hits[0]])

                    for pv_column in [c for c in column_group if c.startswith('Parameter Value[')]:
                        category_key = next(iter(_RX_PARAMETER_VALUE.findall(pv_column)))
                        if category_key not in [x.category.parameter_name.term for x in process.parameter_values]:
                            try:
                                protocol = protocol_map[protocol_ref]
                            except KeyError:
                                raise KeyError('Could not find protocol matching ', protocol_ref)

                            param_hits = [p for p in protocol.parameters if p.parameter_name.term == category_key]

                            if len(param_hits) == 1:
                                category = param_hits[0]
                            else:
                                raise ValueError(
                                    'Could not resolve Protocol parameter '
                                    'from Parameter Value ', category_key)

                            parameter_value = ParameterValue(category=category)
                            v, u = get_value(pv_column,
                                             column_group,
                                             object_series,
                                             ontology_source_map,
                                             unit_categories)
                            parameter_value.value = v
                            parameter_value.unit = u
                            process.parameter_values.append(parameter_value)

                    for comment_column in [c for c in column_group if c.startswith('Comment[')]:
                        comment_key = next(iter(_RX_COMMENT.findall(comment_column)))
                        if comment_key not in [x.name for x in process.comments]:
                            process.comments.append(Comment(name=comment_key, value=str(object_series[comment_column])))

        for _, object_series in DF.iterrows():  # don't drop duplicates
            process_key_sequence = list()
            source_node_context = None
            sample_node_context = None
            for _cg, column_group in enumerate(object_column_map):
                # for each object, parse column group
                object_label = column_group[0]

                if object_label.startswith('Source Name'):
                    try:
                        source_node_context = get_node_by_label_and_key(object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found

                if object_label.startswith('Sample Name'):
                    try:
                        sample_node_context = get_node_by_label_and_key(object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found
                    if source_node_context is not None:
                        if source_node_context not in sample_node_context.derives_from:
                            sample_node_context.derives_from.append(source_node_context)

                if object_label.startswith('Protocol REF'):
                    protocol_ref = str(object_series[object_label])
                    process_key = process_keygen(protocol_ref, column_group, _cg, DF.columns, object_series, _, DF)
                    process_key_sequence.append(process_key)

                if object_label.endswith(' File'):
                    data_node = None
                    try:
                        data_node = get_node_by_label_and_key(object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found
                    if sample_node_context is not None and data_node is not None:
                        if sample_node_context not in data_node.generated_from:
                            data_node.generated_from.append(sample_node_context)

            # Link the processes in each sequence
            for pair in pairwise(process_key_sequence):
                left = processes[pair[0]]  # get process on left of pair
                r = processes[pair[1]]  # get process on right of pair
                plink(left, r)

        return sources, samples, other_material, data, processes, characteristic_categories, unit_categories
