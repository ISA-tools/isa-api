from abc import ABCMeta
from typing import List
from warnings import warn
from random import shuffle

from isatools.model.publication import Publication
from isatools.model.person import Person
from isatools.model.source import Source
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.sample import Sample
from isatools.model.characteristic import Characteristic
from isatools.model.material import Material
from isatools.model.process import Process
from isatools.model.utils import find as find_material, _build_assay_graph


class MetadataMixin(metaclass=ABCMeta):
    """Abstract mixin class to contain metadata fields found in Investigation
    and Study sections of ISA

    Attributes:
        identifier: An identifier associated with objects of this class.
        title: A title associated with objects of this class.
        description: A description associated with objects of this class.
        submission_date: A submission date associated with objects of this
            class.
        public_release_date: A submission date associated with objects of this
            class.
    """

    def __init__(self, filename='', identifier='', title='', description='',
                 submission_date='', public_release_date='', publications=None,
                 contacts=None):

        self.__filename = filename
        self.__identifier = identifier
        self.__title = title
        self.__description = description
        self.__submission_date = submission_date
        self.__public_release_date = public_release_date

        if publications is None:
            self.__publications = []
        else:
            self.__publications = publications

        if contacts is None:
            self.contacts = []
        else:
            self.__contacts = contacts

    @property
    def filename(self):
        """:obj:`str`: A filename"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and isinstance(val, str):
            self.__filename = val
        else:
            raise AttributeError('{0}.filename must be a string'.format(type(self).__name__))

    @property
    def identifier(self):
        """:obj:`str`: An identifier"""
        return self.__identifier

    @identifier.setter
    def identifier(self, val):
        if val is not None and isinstance(val, str):
            self.__identifier = val
        else:
            raise AttributeError('{0}.identifier must be a string'.format(type(self).__name__))

    @property
    def title(self):
        """:obj:`str`: A title"""
        return self.__title

    @title.setter
    def title(self, val):
        if val is not None and isinstance(val, str):
            self.__title = val
        else:
            raise AttributeError('{0}.title must be a string'.format(type(self).__name__))

    @property
    def description(self):
        """:obj:`str`: A description"""
        return self.__description

    @description.setter
    def description(self, val):
        if val is not None and isinstance(val, str):
            self.__description = val
        else:
            raise AttributeError('{0}.description must be a string'.format(type(self).__name__))

    @property
    def submission_date(self):
        """:obj:`str`: A submission date"""
        return self.__submission_date

    @submission_date.setter
    def submission_date(self, val):
        if val is not None and isinstance(val, str):
            self.__submission_date = val
        else:
            raise AttributeError('{0}.submission_date must be a string'.format(type(self).__name__))

    @property
    def public_release_date(self):
        """:obj:`str`: A public release date"""
        return self.__public_release_date

    @public_release_date.setter
    def public_release_date(self, val):
        if val is not None and isinstance(val, str):
            self.__public_release_date = val
        else:
            raise AttributeError('{0}.public_release_date must be a string'.format(type(self).__name__))

    @property
    def publications(self):
        """:obj:`list` of :obj:`Publication`: Container for ISA publications"""
        return self.__publications

    @publications.setter
    def publications(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Publication) for x in val):
                self.__publications = list(val)
        else:
            raise AttributeError('{0}.publications must be iterable containing Publications'
                                 .format(type(self).__name__))

    @property
    def contacts(self):
        """:obj:`list` of :obj:`Person`: Container for ISA contacts"""
        return self.__contacts

    @contacts.setter
    def contacts(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Person) for x in val):
                self.__contacts = list(val)
        else:
            raise AttributeError('{0}.contacts must be iterable containing Person objects'.format(type(self).__name__))


class StudyAssayMixin(metaclass=ABCMeta):
    """Abstract mixin class to contain common fields found in Study
    and Assay sections of ISA

    Attributes:
        filename: A field to specify the file for compatibility with ISA-Tab.
        materials: Materials associated with the Study or Assay.
        sources: Sources associated with the Study or Assay.
        samples: Samples associated with the Study or Assay.
        other_material: Other Material types associated with the Study or
        Assay.
        units: A list of Units used in the annotation of materials.
        characteristic_categories-: A list of OntologyAnnotation used in
            the annotation of material characteristics.
        process_sequence: A list of Process objects representing the
            experimental graphs.
        graph: Graph representation of the experimental graph.

    """

    def __init__(self, filename='',
                 sources: List[Source] = None,
                 samples: List[Sample] = None,
                 other_material: List[Material] = None,
                 units: List[OntologyAnnotation] = None,
                 characteristic_categories: List[OntologyAnnotation] = None,
                 process_sequence: List[Process] = None):
        self.__filename = filename

        self.__materials = {
            'sources': sources if sources else [],
            'samples': [],
            'other_material': []
        }
        if not (sources is None):
            self.__materials['sources'] = sources
        if not (samples is None):
            self.__materials['samples'] = samples
        if not (other_material is None):
            self.__materials['other_material'] = other_material

        self.__units = []
        self.__process_sequence = []
        self.__characteristic_categories = []

        if units:
            self.__units = units
        if process_sequence:
            self.__process_sequence = process_sequence
        if characteristic_categories:
            self.__characteristic_categories = characteristic_categories

    @property
    def filename(self):
        """:obj:`str`: the filename of the study or assay"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('{0}.filename must be a str or None; got {1}:{2}'
                                 .format(type(self).__name__, val, type(val)))
        self.__filename = val

    @property
    def units(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for study units
        """
        return self.__units

    @units.setter
    def units(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__units = list(val)
        else:
            raise AttributeError('{}.units must be iterable containing OntologyAnnotations'.format(type(self).__name__))

    @property
    def sources(self):
        """:obj:`list` of :obj:`Source`: Container for study sources"""
        return self.__materials['sources']

    @sources.setter
    def sources(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Source) for x in val):
                self.__materials['sources'] = list(val)
        else:
            raise AttributeError('{}.sources must be iterable containing Sources'.format(type(self).__name__))

    def add_source(self, name='', characteristics=None, comments=None):
        """Adds a new source to the source materials list.
        :param string name: Source name
        :param list[Characteristics] characteristics: Characteristics about the Source
        :param list comments: Comments about the Source
        """
        s = Source(name=name, characteristics=characteristics, comments=comments)
        self.sources.append(s)

    def yield_sources(self, name=None):
        """Gets an iterator of matching sources for a given name.

        Args:
            name: Source name

        Returns:
            :obj:`filter` of :obj:`Source` that can be iterated on.  If name is
                None, yields all sources.
        """
        return filter(lambda x: x, self.sources) if name is None else filter(lambda x: x.name == name, self.sources)

    def get_source(self, name):
        """Gets the first matching source material for a given name.

        Args:
            name: Source name

        Returns:
            :obj:`Source` matching the name. Only returns the first found.

        """
        slist = list(self.yield_sources(name=name))
        if len(slist) > 0:
            return slist[-1]
        return None

    def yield_sources_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching sources for a given characteristic.

        Args:
            characteristic: Source characteristic

        Returns:
            :obj:`filter` of :obj:`Source` that can be iterated on. If
                characteristic is None, yields all sources.
        """
        if characteristic is None:
            return filter(lambda x: x, self.sources)
        return filter(lambda x: characteristic in x.characteristics, self.sources)

    def get_source_by_characteristic(self, characteristic):
        """Gets the first matching source material for a given characteristic.

        Args:
            characteristic: Source characteristic

        Returns:
            :obj:`Source` matching the characteristic. Only returns the first
                found.

        """
        slist = list(
            self.yield_sources_by_characteristic(
                characteristic=characteristic))
        if len(slist) > 0:
            return slist[-1]
        return None

    def get_source_names(self):
        """Gets all of the source names.

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.sources]

    @property
    def samples(self):
        """:obj:`list` of :obj:`Sample`: Container for study samples"""
        return self.__materials['samples']

    @samples.setter
    def samples(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Sample) for x in val):
                self.__materials['samples'] = list(val)
        else:
            raise AttributeError('{}.samples must be iterable containing Samples'.format(type(self).__name__))

    def add_sample(self, name='', characteristics=None, factor_values=None,
                   derives_from=None, comments=None):
        """Adds a new sample to the sample materials list.
        :param string name: Sample name
        :param list[Characteristics] characteristics: Characteristics about the sample
        :param list comments: Comments about the sample
        :param list derives_from: Sources
        :param list factor_values: FactorValues
        """

        s = Sample(name=name, characteristics=characteristics,
                   factor_values=factor_values, derives_from=derives_from,
                   comments=comments)
        self.samples.append(s)

    def yield_samples(self, name=None):
        """Gets an iterator of matching samples for a given name.
        :param string name: Sample name
        :return: object:`filter` of object:`Source` that can be iterated on.  If name is None, yields all samples.
        """
        return filter(lambda x: x, self.samples) if name is None else filter(lambda x: x.name == name, self.samples)

    def get_sample(self, name):
        """Gets the first matching sample material for a given name.

        Args:
            name: Sample name

        Returns:
            :obj:`Sample` matching the name. Only returns the first found.

        """
        slist = list(self.yield_samples(name=name))
        if len(slist) > 0:
            return slist[-1]
        return None

    def yield_samples_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching samples for a given characteristic.

        Args:
            characteristic: Sample characteristic

        Returns:
            :obj:`filter` of :obj:`Sample` that can be iterated on. If
                characteristic is None, yields all samples.
        """
        if characteristic is None:
            return filter(lambda x: x, self.samples)
        else:
            return filter(lambda x: characteristic in x.characteristics, self.samples)

    def get_sample_by_characteristic(self, characteristic):
        """Gets the first matching sample material for a given characteristic.

        Args:
            characteristic: Sample characteristic

        Returns:
            :obj:`Sample` matching the characteristic. Only returns the first
                found.

        """
        slist = list(
            self.yield_samples_by_characteristic(
                characteristic=characteristic))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def yield_samples_by_factor_value(self, factor_value=None):
        """Gets an iterator of matching samples for a given factor_value.

        Args:
            factor_value: Sample factor value

        Returns:
            :obj:`filter` of :obj:`Sample` that can be iterated on. If
                factor_value is None, yields all samples.
        """
        if factor_value is None:
            return filter(lambda x: x, self.samples)
        else:
            return filter(lambda x: factor_value in x.factor_values, self.samples)

    def get_sample_by_factor_value(self, factor_value):
        """Gets the first matching sample material for a given factor_value.

        Args:
            factor_value: Sample factor value

        Returns:
            :obj:`Sample` matching the factor_value. Only returns the first
                found.

        """
        slist = list(
            self.yield_samples_by_factor_value(
                factor_value=factor_value))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def get_sample_names(self):
        """Gets all of the sample names.

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.samples]

    @property
    def other_material(self):
        """:obj:`list` of :obj:`Material`: Container for study other_material
        """
        return self.__materials['other_material']

    @other_material.setter
    def other_material(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Material) for x in val):
                self.__materials['other_material'] = list(val)
        else:
            raise AttributeError(
                '{}.other_material must be iterable containing Materials'
                    .format(type(self).__name__))

    def yield_materials_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching materials for a given characteristic.

        Args:
            characteristic: Material characteristic

        Returns:
            :obj:`filter` of :obj:`Material` that can be iterated on. If
                characteristic is None, yields all materials.
        """
        if characteristic is None:
            return filter(lambda x: x, self.other_material)
        else:
            return filter(lambda x: characteristic in x.characteristics, self.other_material)

    def get_material_by_characteristic(self, characteristic):
        """Gets the first matching material material for a given
        characteristic.

        Args:
            characteristic: Material characteristic

        Returns:
            :obj:`Material` matching the characteristic. Only returns the first
                found.

        """
        mlist = list(
            self.yield_materials_by_characteristic(
                characteristic=characteristic))
        if len(mlist) > 0:
            return mlist[-1]
        else:
            return None

    @property
    def materials(self):
        """:obj:`dict` of :obj:`list`: Container for sources, samples and
        other_material"""
        warn("the `materials` dict property is being deprecated in favour of `sources`, `samples`, "
             "and `other_material` properties.", DeprecationWarning)
        return self.__materials

    @property
    def process_sequence(self):
        """:obj:`list` of :obj:`Process`: Container for study Processes"""
        return self.__process_sequence

    @process_sequence.setter
    def process_sequence(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Process) for x in val):
                self.__process_sequence = list(val)
        else:
            raise AttributeError(
                '{}.process_sequence must be iterable containing Processes'
                    .format(type(self).__name__))

    @property
    def characteristic_categories(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for study
        characteristic categories used"""
        return self.__characteristic_categories

    @characteristic_categories.setter
    def characteristic_categories(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__characteristic_categories = list(val)
        else:
            raise AttributeError('{}.characteristic_categories must be iterable containing OntologyAnnotation'
                                 .format(type(self).__name__))

    @property
    def graph(self):
        """:obj:`networkx.DiGraph` A graph representation of the study's
        process sequence"""
        if len(self.process_sequence) > 0:
            return _build_assay_graph(self.process_sequence)
        return None

    @graph.setter
    def graph(self, graph):
        raise AttributeError('{}.graph is not settable'.format(type(self).__name__))

    def shuffle_materials(self, attribute):
        """
        Shuffles the samples in the Study or Assay

        :param attribute: The attribute to shuffle
        :example:
            study.shuffle_materials('samples')
            assay.shuffle_materials('Extract Name')
            assay.shuffle_materials('Labeled Extract Name')
        """

        ontology_mapping = {
            'samples': 'extraction',
            'sources': 'sampling',
            'Extract Name': None,
            'Labeled Extract Name': 'data acquisition'
        }

        if attribute not in ontology_mapping:
            error = '%s should be in %s' % (attribute, ', '.join(list(ontology_mapping.keys())))
            raise ValueError(error)

        if attribute == 'samples' or attribute == 'sources':
            target_material = [x for x in getattr(self, attribute)]
        else:
            target_material = [x for x in getattr(self, 'other_material') if getattr(x, 'type') == attribute]

        shuffle(target_material)
        mat_index = 0
        for mat in target_material:
            ontology_term = 'randomized order'
            if ontology_mapping[attribute]:
                ontology_term = 'randomized %s order' % ontology_mapping[attribute]
            ontology_annotation = OntologyAnnotation(term=ontology_term)
            characteristic = Characteristic(category=ontology_annotation, value=mat_index)
            char, char_index = find_material(lambda x: x.category.term == ontology_term, mat.characteristics)
            if not char:
                mat.characteristics.append(characteristic)
            else:
                mat.characteristics[char_index] = characteristic
            mat_index += 1

    def categories_to_dict(self):
        characteristics_categories = []
        for characteristic in self.characteristic_categories:
            id_ = characteristic.id
            if id_.startswith('#ontology_annotation/'):
                id_ = id_.replace('#ontology_annotation/', '#characteristic_category/')
            else:
                id_ = '#characteristic_category/' + id_
            characteristics_categories.append({
                '@id': id_,
                'characteristicType': characteristic.to_dict()
            })
        return characteristics_categories
