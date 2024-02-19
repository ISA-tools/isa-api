from os import path

from pandas import DataFrame
from numpy import nan

from isatools.constants import SYNONYMS
from isatools.model import (
    OntologyAnnotation,
    Investigation,
    Source,
    Process,
    Sample,
    load_protocol_types_info,
    DataFile,
    Material
)
from isatools.isatab.defaults import log
from isatools.isatab.graph import _all_end_to_end_paths, _longest_path_and_attrs
from isatools.isatab.utils import (
    get_comment_column,
    get_pv_columns,
    get_fv_columns,
    get_characteristic_columns,
    get_object_column_map,
    get_column_header
)


def write_study_table_files(inv_obj, output_dir):
    """Writes out study table files according to pattern defined by

    Source Name, [ Characteristics[], ... ],
    Protocol Ref*: 'sample collection', [ ParameterValue[], ... ],
    Sample Name, [ Characteristics[], ... ]
    [ FactorValue[], ... ]

    which should be equivalent to studySample.xml in default config

    :param inv_obj: An Investigation object containing ISA content
    :param output_dir: A path to a directory to write the ISA-Tab study files
    :return: None
    """
    if not isinstance(inv_obj, Investigation):
        raise NotImplementedError
    for study_obj in inv_obj.studies:
        s_graph = study_obj.graph

        if s_graph is None:
            break
        protrefcount = 0
        protnames = dict()

        def flatten(current_list):
            return [item for sublist in current_list for item in sublist]

        columns = []

        # start_nodes, end_nodes = _get_start_end_nodes(s_graph)
        paths = _all_end_to_end_paths(
            s_graph,
            [x for x in s_graph.nodes() if isinstance(s_graph.indexes[x], Source)])
        log.warning(s_graph.nodes())

        sample_in_path_count = 0
        protocol_in_path_count = 0
        longest_path = _longest_path_and_attrs(paths, s_graph.indexes)

        for node_index in longest_path:
            node = s_graph.indexes[node_index]
            if isinstance(node, Source):
                olabel = "Source Name"
                columns.append(olabel)
                columns += flatten(
                    map(lambda x: get_characteristic_columns(olabel, x),
                        node.characteristics))
                columns += flatten(
                    map(lambda x: get_comment_column(
                        olabel, x), node.comments))
            elif isinstance(node, Process):
                olabel = "Protocol REF.{}".format(protocol_in_path_count)
                columns.append(olabel)
                protocol_in_path_count += 1
                if node.executes_protocol.name not in protnames.keys():
                    protnames[node.executes_protocol.name] = protrefcount
                    protrefcount += 1
                columns += flatten(map(lambda x: get_pv_columns(olabel, x),
                                       node.parameter_values))
                if node.date is not None:
                    columns.append(olabel + ".Date")
                if node.performer is not None:
                    columns.append(olabel + ".Performer")
                columns += flatten(
                    map(lambda x: get_comment_column(
                        olabel, x), node.comments))

            elif isinstance(node, Sample):
                olabel = "Sample Name.{}".format(sample_in_path_count)
                columns.append(olabel)
                sample_in_path_count += 1
                columns += flatten(
                    map(lambda x: get_characteristic_columns(olabel, x),
                        node.characteristics))
                columns += flatten(
                    map(lambda x: get_comment_column(
                        olabel, x), node.comments))
                columns += flatten(map(lambda x: get_fv_columns(olabel, x),
                                       node.factor_values))

        omap = get_object_column_map(columns, columns)
        # load into dictionary
        df_dict = dict(map(lambda k: (k, []), flatten(omap)))

        for path_ in paths:
            for k in df_dict.keys():  # add a row per path
                df_dict[k].extend([""])

            sample_in_path_count = 0
            protocol_in_path_count = 0
            for node_index in path_:
                node = s_graph.indexes[node_index]
                if isinstance(node, Source):
                    olabel = "Source Name"
                    df_dict[olabel][-1] = node.name
                    for c in node.characteristics:
                        category_label = c.category.term if isinstance(c.category.term, str) \
                            else c.category.term["annotationValue"]
                        clabel = "{0}.Characteristics[{1}]".format(
                            olabel, category_label)
                        write_value_columns(df_dict, clabel, c)
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value

                elif isinstance(node, Process):
                    olabel = "Protocol REF.{}".format(protocol_in_path_count)
                    protocol_in_path_count += 1
                    df_dict[olabel][-1] = node.executes_protocol.name
                    for pv in node.parameter_values:
                        pvlabel = "{0}.Parameter Value[{1}]".format(
                            olabel, pv.category.parameter_name.term)
                        write_value_columns(df_dict, pvlabel, pv)
                    if node.date is not None:
                        df_dict[olabel + ".Date"][-1] = node.date
                    if node.performer is not None:
                        df_dict[olabel + ".Performer"][-1] = node.performer
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value

                elif isinstance(node, Sample):
                    olabel = "Sample Name.{}".format(sample_in_path_count)
                    sample_in_path_count += 1
                    df_dict[olabel][-1] = node.name
                    for c in node.characteristics:
                        category_label = c.category.term if isinstance(c.category.term, str) \
                            else c.category.term["annotationValue"]
                        clabel = "{0}.Characteristics[{1}]".format(
                            olabel, category_label)
                        write_value_columns(df_dict, clabel, c)
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value
                    for fv in node.factor_values:
                        fvlabel = "{0}.Factor Value[{1}]".format(
                            olabel, fv.factor_name.name)
                        write_value_columns(df_dict, fvlabel, fv)
        """if isinstance(pbar, ProgressBar):
            pbar.finish()"""

        DF = DataFrame(columns=columns)
        DF = DF.from_dict(data=df_dict)
        DF = DF[columns]  # reorder columns
        DF = DF.sort_values(by=DF.columns[0], ascending=True)
        # arbitrary sort on column 0

        for dup_item in set([x for x in columns if columns.count(x) > 1]):
            for j, each in enumerate(
                    [i for i, x in enumerate(columns) if x == dup_item]):
                columns[each] = dup_item + str(j)

        DF.columns = columns  # reset columns after checking for dups

        for i, col in enumerate(columns):
            if "Comment[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif col.endswith("Term Source REF"):
                columns[i] = "Term Source REF"
            elif col.endswith("Term Accession Number"):
                columns[i] = "Term Accession Number"
            elif col.endswith("Unit"):
                columns[i] = "Unit"
            elif "Characteristics[" in col:
                if "material type" in col.lower():
                    columns[i] = "Material Type"
                else:
                    columns[i] = col[col.rindex(".") + 1:]
            elif "Factor Value[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif "Parameter Value[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif col.endswith("Date"):
                columns[i] = "Date"
            elif col.endswith("Performer"):
                columns[i] = "Performer"
            elif "Protocol REF" in col:
                columns[i] = "Protocol REF"
            elif col.startswith("Sample Name."):
                columns[i] = "Sample Name"

        log.debug("Rendered {} paths".format(len(DF.index)))

        DF_no_dups = DF.drop_duplicates()
        if len(DF.index) > len(DF_no_dups.index):
            log.debug("Dropping duplicates...")
            DF = DF_no_dups

        log.debug("Writing {} rows".format(len(DF.index)))
        # reset columns, replace nan with empty string, drop empty columns
        DF.columns = columns
        DF = DF.replace('', nan)
        DF = DF.dropna(axis=1, how='all')

        with open(path.join(output_dir, study_obj.filename), 'w') as out_fp:
            DF.to_csv(
                path_or_buf=out_fp, index=False, sep='\t', encoding='utf-8')


def write_assay_table_files(inv_obj, output_dir, write_factor_values=False):
    """Writes out assay table files according to pattern defined by

    Sample Name,
    Protocol Ref: 'sample collection', [ ParameterValue[], ... ],
    Material Name, [ Characteristics[], ... ]
    [ FactorValue[], ... ]

    :param inv_obj: An Investigation object containing ISA content
    :param output_dir: A path to a directory to write the ISA-Tab assay files
    :param write_factor_values: Flag to indicate whether or not to write out
    the Factor Value columns in the assay tables
    :return: None
    """

    if not isinstance(inv_obj, Investigation):
        raise NotImplementedError
    protocol_types_dict = load_protocol_types_info()
    for study_obj in inv_obj.studies:
        for assay_obj in study_obj.assays:
            a_graph = assay_obj.graph
            if a_graph is None:
                break
            protrefcount = 0
            protnames = dict()

            def flatten(current_list):
                return [item for sublist in current_list for item in sublist]

            columns = []

            # start_nodes, end_nodes = _get_start_end_nodes(a_graph)
            paths = _all_end_to_end_paths(
                a_graph, [x for x in a_graph.nodes()
                          if isinstance(a_graph.indexes[x], Sample)])
            if len(paths) == 0:
                log.info("No paths found, skipping writing assay file")
                continue
            if _longest_path_and_attrs(paths, a_graph.indexes) is None:
                raise IOError(
                    "Could not find any valid end-to-end paths in assay graph")
            
            protocol_in_path_count = 0
            for node_index in _longest_path_and_attrs(paths, a_graph.indexes):
                node = a_graph.indexes[node_index]
                if isinstance(node, Sample):
                    olabel = "Sample Name"
                    # olabel = "Sample Name.{}".format(sample_in_path_count)
                    # sample_in_path_count += 1
                    columns.append(olabel)
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))
                    if write_factor_values:
                        columns += flatten(
                            map(lambda x: get_fv_columns(olabel, x),
                                node.factor_values))

                elif isinstance(node, Process):
                    olabel = "Protocol REF.{}".format(protocol_in_path_count)
                    columns.append(olabel)
                    protocol_in_path_count += 1
                    if node.executes_protocol.name not in protnames.keys():
                        protnames[node.executes_protocol.name] = protrefcount
                        protrefcount += 1
                    if node.date is not None:
                        columns.append(olabel + ".Date")
                    if node.performer is not None:
                        columns.append(olabel + ".Performer")
                    columns += flatten(map(lambda x: get_pv_columns(olabel, x),
                                           node.parameter_values))
                    if node.executes_protocol.protocol_type:
                        oname_label = get_column_header(
                            node.executes_protocol.protocol_type.term,
                            protocol_types_dict
                        )
                        if oname_label is not None:
                            columns.append(oname_label)
                        elif node.executes_protocol.protocol_type.term.lower() \
                                in protocol_types_dict["nucleic acid hybridization"][SYNONYMS]:
                            columns.extend(
                                ["Hybridization Assay Name",
                                 "Array Design REF"])
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))

                    for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                        if output.label not in columns:
                            columns.append(output.label)
                        columns += flatten(
                            map(lambda x: get_comment_column(output.label, x),
                                output.comments))
                elif isinstance(node, Material):
                    olabel = node.type
                    columns.append(olabel)
                    columns += flatten(
                        map(lambda x: get_characteristic_columns(olabel, x),
                            node.characteristics))
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))

                elif isinstance(node, DataFile):
                    pass  # handled in process

            omap = get_object_column_map(columns, columns)

            # load into dictionary
            df_dict = dict(map(lambda k: (k, []), flatten(omap)))

            def pbar(x):
                return x

            for path_ in pbar(paths):
                for k in df_dict.keys():  # add a row per path
                    df_dict[k].extend([""])

                protocol_in_path_count = 0
                for node_index in path_:
                    node = a_graph.indexes[node_index]
                    if isinstance(node, Process):
                        olabel = "Protocol REF.{}".format(protocol_in_path_count)
                        protocol_in_path_count += 1
                        df_dict[olabel][-1] = node.executes_protocol.name
                        if node.executes_protocol.protocol_type:
                            oname_label = get_column_header(
                                node.executes_protocol.protocol_type.term,
                                protocol_types_dict
                            )
                            if oname_label is not None:
                                df_dict[oname_label][-1] = node.name

                            elif node.executes_protocol.protocol_type.term.lower() in \
                                    protocol_types_dict["nucleic acid hybridization"][SYNONYMS]:
                                df_dict["Hybridization Assay Name"][-1] = \
                                    node.name
                                df_dict["Array Design REF"][-1] = \
                                    node.array_design_ref
                        if node.date is not None:
                            df_dict[olabel + ".Date"][-1] = node.date
                        if node.performer is not None:
                            df_dict[olabel + ".Performer"][-1] = node.performer
                        for pv in node.parameter_values:
                            pvlabel = "{0}.Parameter Value[{1}]".format(olabel, pv.category.parameter_name.term)
                            write_value_columns(df_dict, pvlabel, pv)
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                            df_dict[colabel][-1] = co.value

                        for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                            output_by_type = []
                            delim = ";"
                            olabel = output.label
                            if output.label not in columns:
                                columns.append(output.label)
                            output_by_type.append(output.filename)
                            df_dict[olabel][-1] = delim.join(map(str, output_by_type))

                            for co in output.comments:
                                colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                                df_dict[colabel][-1] = co.value

                    elif isinstance(node, Sample):
                        olabel = "Sample Name"
                        # olabel = "Sample Name.{}".format(sample_in_path_count)
                        # sample_in_path_count += 1
                        df_dict[olabel][-1] = node.name
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(
                                olabel, co.name)
                            df_dict[colabel][-1] = co.value
                        if write_factor_values:
                            for fv in node.factor_values:
                                fvlabel = "{0}.Factor Value[{1}]".format(olabel, fv.factor_name.name)
                                write_value_columns(df_dict, fvlabel, fv)

                    elif isinstance(node, Material):
                        olabel = node.type
                        df_dict[olabel][-1] = node.name
                        for c in node.characteristics:
                            if c.category is not None:
                                category_label = c.category.term if isinstance(c.category.term, str) \
                                    else c.category.term["annotationValue"]
                                clabel = "{0}.Characteristics[{1}]".format(olabel, category_label)
                                write_value_columns(df_dict, clabel, c)
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(
                                olabel, co.name)
                            df_dict[colabel][-1] = co.value

                    elif isinstance(node, DataFile):
                        pass  # handled in process

            DF = DataFrame(columns=columns)
            DF = DF.from_dict(data=df_dict)
            DF = DF[columns]  # reorder columns
            try:
                DF = DF.sort_values(by=DF.columns[0], ascending=True)
            except ValueError as e:
                log.critical('Error thrown: column labels are: {}'.format(DF.columns))
                log.critical('Error thrown: data is: {}'.format(DF))
                raise e
            # arbitrary sort on column 0

            for dup_item in set([x for x in columns if columns.count(x) > 1]):
                for j, each in enumerate(
                        [i for i, x in enumerate(columns) if x == dup_item]):
                    columns[each] = ".".join([dup_item, str(j)])

            DF.columns = columns

            for i, col in enumerate(columns):
                if col.endswith("Term Source REF"):
                    columns[i] = "Term Source REF"
                elif col.endswith("Term Accession Number"):
                    columns[i] = "Term Accession Number"
                elif col.endswith("Unit"):
                    columns[i] = "Unit"
                elif "Characteristics[" in col:
                    if "material type" in col.lower():
                        columns[i] = "Material Type"
                    elif "label" in col.lower():
                        columns[i] = "Label"
                    else:
                        columns[i] = col[col.rindex(".") + 1:]
                elif "Factor Value[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif "Parameter Value[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif col.endswith("Date"):
                    columns[i] = "Date"
                elif col.endswith("Performer"):
                    columns[i] = "Performer"
                elif "Comment[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif "Protocol REF" in col:
                    columns[i] = "Protocol REF"
                elif "." in col:
                    columns[i] = col[:col.rindex(".")]

            log.debug("Rendered {} paths".format(len(DF.index)))
            if len(DF.index) > 1:
                if len(DF.index) > len(DF.drop_duplicates().index):
                    log.debug("Dropping duplicates...")
                    DF = DF.drop_duplicates()

            log.debug("Writing {} rows".format(len(DF.index)))
            # reset columns, replace nan with empty string, drop empty columns
            DF.columns = columns
            DF = DF.replace('', nan)
            DF = DF.dropna(axis=1, how='all')

            with open(path.join(
                    output_dir, assay_obj.filename), 'w') as out_fp:
                DF.to_csv(path_or_buf=out_fp, index=False, sep='\t',
                          encoding='utf-8')


def write_value_columns(df_dict, label, x):
    """Adds values to the DataFrame dictionary when building the tables

    :param df_dict: The DataFrame dictionary to insert the relevant values
    :param label: Header label needed for the object
    :param x: Object of interest
    :return: None
    """

    if isinstance(x.value, (int, float)) and x.unit:
        if isinstance(x.unit, OntologyAnnotation):
            df_dict[label][-1] = x.value
            df_dict[label + ".Unit"][-1] = x.unit.term
            df_dict[label + ".Unit.Term Source REF"][-1] = ""
            if x.unit.term_source:
                if type(x.unit.term_source) == str:
                    df_dict[label + ".Unit.Term Source REF"][-1] = x.unit.term_source
                elif x.unit.term_source.name:
                    df_dict[label + ".Unit.Term Source REF"][-1] = x.unit.term_source.name

            # df_dict[label + ".Unit.Term Source REF"][-1] = \
            #     x.unit.term_source.name if x.unit.term_source else ""
            df_dict[label + ".Unit.Term Accession Number"][-1] = \
                x.unit.term_accession
        else:
            df_dict[label][-1] = x.value
            df_dict[label + ".Unit"][-1] = x.unit
    elif isinstance(x.value, OntologyAnnotation):
        df_dict[label][-1] = x.value.term
        df_dict[label + ".Term Source REF"][-1] = ""
        if x.value.term_source:
            if type(x.value.term_source) == str:
                df_dict[label + ".Term Source REF"][-1] = x.value.term_source
            elif x.value.term_source.name:
                df_dict[label + ".Term Source REF"][-1] = x.value.term_source.name

        df_dict[label + ".Term Accession Number"][-1] = x.value.term_accession
    else:
        df_dict[label][-1] = x.value
