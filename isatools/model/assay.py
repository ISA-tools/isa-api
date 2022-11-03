from isatools.model.comments import Commentable
from isatools.model.mixins import StudyAssayMixin
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.datafile import DataFile
from isatools.model.material import Material
from isatools.model.process import Process
from isatools.model.loader_indexes import loader_states as indexes


class Assay(Commentable, StudyAssayMixin, object):
    """An Assay represents a test performed either on material taken from a
    subject or on a whole initial subject, producing qualitative or
    quantitative
    measurements. An Assay groups descriptions of provenance of sample
    processing for related tests. Each test typically follows the steps of one
    particular experimental workflow described by a particular protocol.

    Attributes:
        measurement_type: An Ontology Annotation to qualify the endpoint, or
            what is being measured (e.g. gene expression profiling or protein
            identification).
        technology_type: An Ontology Annotation to identify the technology
            used to perform the measurement.
        technology_platform: Manufacturer and platform name,
        e.g. Bruker AVANCE.
        filename: A field to specify the name of the Assay file for
            compatibility with ISA-Tab.
        materials: Materials associated with the Assay, lists of 'samples' and
            'other_material'.
        units: A list of Units used in the annotation of material units.
        characteristic_categories: A list of OntologyAnnotation used in the
            annotation of material characteristics in the Assay.
        process_sequence: A list of Process objects representing the
            experimental graphs at the Assay level.
        comments: Comments associated with instances of this class.
        graph: A graph representation of the assay graph.
    """

    def __init__(self, measurement_type=None, technology_type=None,
                 technology_platform='', filename='', process_sequence=None,
                 data_files=None, samples=None, other_material=None,
                 characteristic_categories=None, units=None, comments=None):
        super().__init__(comments)
        StudyAssayMixin.__init__(
            self, filename=filename, samples=samples,
            other_material=other_material,
            process_sequence=process_sequence,
            characteristic_categories=characteristic_categories, units=units)

        self.__measurement_type = OntologyAnnotation()
        if measurement_type:
            self.measurement_type = measurement_type

        self.__technology_type = OntologyAnnotation()
        if technology_type:
            self.technology_type = technology_type

        self.__technology_platform = technology_platform

        if data_files is None:
            self.__data_files = []
        else:
            self.__data_files = data_files

    @property
    def measurement_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        assay measurement_type"""
        return self.__measurement_type

    @measurement_type.setter
    def measurement_type(self, val):
        if val is not None and not isinstance(val, (str, OntologyAnnotation)):
            raise AttributeError(
                'Assay.measurement_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__measurement_type = val

    @property
    def technology_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        assay technology type"""
        return self.__technology_type

    @technology_type.setter
    def technology_type(self, val):
        if val is not None and not isinstance(val, (str, OntologyAnnotation)):
            raise AttributeError(
                'Assay.technology_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__technology_type = val

    @property
    def technology_platform(self):
        """:obj:`str`: the technology_platform of the assay"""
        return self.__technology_platform

    @technology_platform.setter
    def technology_platform(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Assay.technology_platform must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__technology_platform = val

    @property
    def data_files(self):
        """:obj:`list` of :obj:`DataFile`: Container for data files"""
        return self.__data_files

    @data_files.setter
    def data_files(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, DataFile) for x in val):
                self.__data_files = list(val)
        else:
            raise AttributeError('{0}.data_files must be iterable containing DataFiles'.format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.Assay(measurement_type={measurement_type}, " \
               "technology_type={technology_type}, " \
               "technology_platform='{assay.technology_platform}', " \
               "filename='{assay.filename}', data_files={assay.data_files}, " \
               "samples={assay.samples}, " \
               "process_sequence={assay.process_sequence}, " \
               "other_material={assay.other_material}, " \
               "characteristic_categories={assay.characteristic_categories}," \
               " comments={assay.comments}, units={assay.units})" \
            .format(assay=self,
                    measurement_type=repr(self.measurement_type),
                    technology_type=repr(self.technology_type))

    def __str__(self):
        return """Assay(
    measurement_type={measurement_type}
    technology_type={technology_type}
    technology_platform={assay.technology_platform}
    filename={assay.filename}
    data_files={num_datafiles} DataFile objects
    samples={num_samples} Sample objects
    process_sequence={num_processes} Process objects
    other_material={num_other_material} Material objects
    characteristic_categories={num_characteristic_categories} OntologyAnnots
    comments={num_comments} Comment objects
    units={num_units} Unit objects
)""".format(assay=self,
            measurement_type=self.measurement_type.term if isinstance(self.measurement_type, OntologyAnnotation)
            else self.measurement_type if isinstance(self.measurement_type, str) else '',
            technology_type=self.technology_type.term if isinstance(self.technology_type, OntologyAnnotation)
            else self.technology_type if isinstance(self.technology_type, str) else '',
            num_datafiles=len(self.data_files),
            num_samples=len(self.samples),
            num_processes=len(self.process_sequence),
            num_other_material=len(self.other_material),
            num_characteristic_categories=len(self.characteristic_categories),
            num_comments=len(self.comments), num_units=len(self.units))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Assay) \
               and self.measurement_type == other.measurement_type \
               and self.technology_type == other.technology_type \
               and self.technology_platform == other.technology_platform \
               and self.filename == other.filename \
               and self.data_files == other.data_files \
               and self.samples == other.samples \
               and self.process_sequence == other.process_sequence \
               and self.other_material == other.other_material \
               and self.characteristic_categories \
               == other.characteristic_categories \
               and self.comments == other.comments \
               and self.units == other.units

    def __ne__(self, other):
        return not self == other

    def to_dict(self, ld=False):
        assay = {
            "measurementType": self.measurement_type.to_dict(ld=ld) if self.measurement_type else '',
            "technologyType": self.technology_type.to_dict(ld=ld) if self.technology_type else '',
            "technologyPlatform": self.technology_platform,
            "filename": self.filename,
            "characteristicCategories": self.categories_to_dict(ld=ld),
            "unitCategories": [unit.to_dict(ld=ld) for unit in self.units],
            "comments": [comment.to_dict(ld=ld) for comment in self.comments],
            "materials": {
                "samples": [{"@id": sample.id} for sample in self.samples],
                "otherMaterials": [mat.to_dict(ld=ld) for mat in self.other_material]
            },
            "dataFiles": [file.to_dict(ld=ld) for file in self.data_files],
            "processSequence": [process.to_dict(ld=ld) for process in self.process_sequence]
        }
        return self.update_isa_object(assay, ld)

    def from_dict(self, assay, isa_study):
        self.technology_platform = assay.get('technologyPlatform', '')
        self.filename = assay.get('filename', '')
        self.load_comments(assay.get('comments', []))

        # measurement type
        measurement_type_data = assay.get('measurementType', None)
        if measurement_type_data:
            measurement_type = OntologyAnnotation()
            measurement_type.from_dict(measurement_type_data)
            self.measurement_type = measurement_type

        # technology type
        technology_type_data = assay.get('technologyType', None)
        if technology_type_data:
            technology_type = OntologyAnnotation()
            technology_type.from_dict(technology_type_data)
            self.technology_type = technology_type

        # units categories
        for unit_data in assay.get('unitCategories', []):
            unit = OntologyAnnotation()
            unit.from_dict(unit_data)
            self.units.append(unit)
            indexes.add_unit(unit)

        # data files
        indexes.reset_data_file()
        for data_file_data in assay.get('dataFiles', []):
            data_file = DataFile()
            data_file.from_dict(data_file_data)
            self.data_files.append(data_file)
            indexes.add_data_file(data_file)

        # samples
        for sample_data in assay.get('materials', {}).get('samples', []):
            self.samples.append(indexes.get_sample(sample_data['@id']))

        # characteristic categories
        for characteristic_category_data in assay.get('characteristicCategories', []):
            characteristic_category = OntologyAnnotation()
            characteristic_category.from_dict(characteristic_category_data['characteristicType'])
            characteristic_category.id = characteristic_category_data['@id']
            isa_study.characteristic_categories.append(characteristic_category)
            indexes.add_characteristic_category(characteristic_category)

        # other materials
        for other_material_data in assay.get('materials', {}).get('otherMaterials', []):
            other_material = Material()
            other_material_data['name'] = (other_material_data['name']
                                           .replace("labeledextract-", "")
                                           .replace("extract-", ""))
            other_material.from_dict(other_material_data)

            self.other_material.append(other_material)
            indexes.add_other_material(other_material)

        # process sequence
        for process_sequence_data in assay.get('processSequence', []):
            process = Process()
            process.from_assay_dict(process_sequence_data, technology_type=self.technology_type)
            self.process_sequence.append(process)
            indexes.add_process(process)

            # link processes in process sequence
            for assay_process_json in assay.get('processSequence', []):
                try:
                    previous_process_id = assay_process_json['previousProcess']['@id']
                    indexes.get_process(assay_process_json["@id"]).prev_process = \
                        indexes.get_process(previous_process_id)
                except KeyError:
                    pass
                try:
                    next_process_id = assay_process_json['nextProcess']['@id']
                    indexes.get_process(assay_process_json["@id"]).next_process = indexes.get_process(next_process_id)
                except KeyError:
                    pass
