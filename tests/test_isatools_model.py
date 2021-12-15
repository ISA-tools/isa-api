"""Tests on isatools.model classes"""
from __future__ import absolute_import
import datetime
import unittest
from unittest.mock import patch

from isatools.model import (
    Comment, Investigation, OntologySource, OntologyAnnotation, Publication, Person, Study, StudyFactor, Characteristic,
    Assay, Protocol, ProtocolParameter, ParameterValue, ProtocolComponent, Source, Sample, Extract, LabeledExtract,
    FactorValue, DataFile, RawDataFile, DerivedDataFile, RawSpectralDataFile, ArrayDataFile, DerivedSpectralDataFile,
    ProteinAssignmentFile, PeptideAssignmentFile, DerivedArrayDataMatrixFile,
    PostTranslationalModificationAssignmentFile, AcquisitionParameterDataFile, FreeInductionDecayDataFile,
    load_protocol_types_info
)


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.comment_default = Comment()
        self.comment = Comment(name='N', value='V')

    def test_repr(self):
        self.assertEqual("isatools.model.Comment(name='', value='')",
                         repr(self.comment_default))
        self.assertEqual("isatools.model.Comment(name='N', value='V')",
                         repr(self.comment))

    def test_str(self):
        self.assertEqual("""Comment(
    name=
    value=
)""", str(self.comment_default))

        self.assertEqual("""Comment(
    name=N
    value=V
)""", str(self.comment))

    def test_eq(self):
        expected_comment = Comment(name='N', value='V')

        self.assertEqual(expected_comment, self.comment)
        self.assertEqual(hash(expected_comment), hash(self.comment))

    def test_ne(self):
        expected_other_comment = Comment(name='V', value='N')

        self.assertNotEqual(expected_other_comment, self.comment)
        self.assertNotEqual(hash(expected_other_comment), hash(self.comment))

    def test_raises_AttributeError(self):
        try:
            self.comment_default.name = 0
        except AttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')

        try:
            self.comment_default.value = 0
        except AttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')


class InvestigationTest(unittest.TestCase):

    def setUp(self):
        self.investigation_default = Investigation()
        self.investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual("isatools.model.Investigation(identifier='', "
                         "filename='', title='', submission_date='', "
                         "public_release_date='', "
                         "ontology_source_references=[], publications=[], "
                         "contacts=[], studies=[], comments=[])",
                         repr(self.investigation_default))
        self.assertEqual("isatools.model.Investigation(identifier='id', "
                         "filename='file', title='T', "
                         "submission_date='2017-01-01 00:00:00', "
                         "public_release_date='2017-01-01 00:00:00', "
                         "ontology_source_references=[], publications=[], "
                         "contacts=[], studies=[], comments=[])",
                         repr(self.investigation))

    def test_str(self):
        self.assertEqual("""Investigation(
    identifier=
    filename=
    title=
    submission_date=
    public_release_date=
    ontology_source_references=0 OntologySources
    publications=0 Publication objects
    contacts=0 Person objects
    studies=0 Study objects
    comments=0 Comment objects
)""", str(self.investigation_default))

        self.assertEqual("""Investigation(
    identifier=id
    filename=file
    title=T
    submission_date=2017-01-01 00:00:00
    public_release_date=2017-01-01 00:00:00
    ontology_source_references=0 OntologySources
    publications=0 Publication objects
    contacts=0 Person objects
    studies=0 Study objects
    comments=0 Comment objects
)""", str(self.investigation))

    def test_eq(self):
        expected_investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))
        self.assertEqual(expected_investigation, self.investigation)
        self.assertEqual(hash(expected_investigation), hash(self.investigation))

    def test_ne(self):
        expected_other_investigation = Investigation(
            identifier='id2', filename='file2', title='T2',
            submission_date=datetime.datetime(day=2, month=1, year=2017),
            public_release_date=datetime.datetime(day=2, month=1, year=2017))
        self.assertNotEqual(expected_other_investigation, self.investigation)
        self.assertNotEqual(
            hash(expected_other_investigation), hash(self.investigation))


class OntologySourceTest(unittest.TestCase):

    def setUp(self):
        self.ontology_source_default = OntologySource(name='N')
        self.ontology_source = OntologySource(name='N', file='F', version='V',
                                              description='D')

    def test_repr(self):
        self.assertEqual("isatools.model.OntologySource(name='N', file='', "
                         "version='', description='', comments=[])",
                         repr(self.ontology_source_default))
        self.assertEqual("isatools.model.OntologySource(name='N', file='F', "
                         "version='V', description='D', comments=[])",
                         repr(self.ontology_source))

    def test_str(self):
        self.assertEqual("""OntologySource(
    name=N
    file=
    version=
    description=
    comments=0 Comment objects
)""", str(self.ontology_source_default))

        self.assertEqual("""OntologySource(
    name=N
    file=F
    version=V
    description=D
    comments=0 Comment objects
)""", str(self.ontology_source))

    def test_eq(self):
        expected_ontology_source = OntologySource(
            name='N', file='F', version='V', description='D', comments=[])
        self.assertEqual(expected_ontology_source, self.ontology_source)
        self.assertEqual(
            hash(expected_ontology_source),  hash(self.ontology_source))

    def test_ne(self):
        expected_other_ontology_source = OntologySource(
            name='N2', file='F2', version='V2', description='D2', comments=[])
        self.assertNotEqual(
            expected_other_ontology_source, self.ontology_source)
        self.assertNotEqual(
            hash(expected_other_ontology_source), hash(self.ontology_source))


class OntologyAnnotationTest(unittest.TestCase):

    def setUp(self):
        self.ontology_annotation_default = OntologyAnnotation()
        self.ontology_annotation = OntologyAnnotation(
            term='T', term_source=OntologySource('N'), term_accession='A')

    def test_repr(self):
        self.assertEqual("isatools.model.OntologyAnnotation(term='', "
                         "term_source=None, term_accession='', comments=[])",
                         repr(self.ontology_annotation_default))
        self.assertEqual("isatools.model.OntologyAnnotation(term='T', "
                         "term_source=isatools.model.OntologySource("
                         "name='N', file='', version='', description='', "
                         "comments=[]), term_accession='A', comments=[])",
                         repr(self.ontology_annotation))

    def test_str(self):
        self.assertTrue(isinstance(self.ontology_annotation_default, OntologyAnnotation))
        self.assertEqual(self.ontology_annotation_default.term, "")
        self.assertEqual(self.ontology_annotation_default.term_source, None)
        self.assertEqual(self.ontology_annotation_default.term_accession, "")
        self.assertEqual(self.ontology_annotation_default.comments, [])

        self.assertTrue(isinstance(self.ontology_annotation, OntologyAnnotation))
        self.assertEqual(self.ontology_annotation.term, "T")
        self.assertTrue(isinstance(self.ontology_annotation.term_source, OntologySource))
        self.assertEqual(self.ontology_annotation.term_source.name, "N")
        self.assertEqual(self.ontology_annotation.term_accession, "A")
        self.assertEqual(self.ontology_annotation.comments, [])

    def test_eq(self):
        expected_ontology_annotation = OntologyAnnotation(
            term='T', term_source=OntologySource(name='N'), term_accession='A')
        self.assertEqual(expected_ontology_annotation, self.ontology_annotation)
        self.assertEqual(
            hash(expected_ontology_annotation),  hash(self.ontology_annotation))

    def test_ne(self):
        expected_other_ontology_annotation = OntologyAnnotation(
            term='T2', term_source=OntologySource(name='N2'),
            term_accession='A2')
        self.assertNotEqual(expected_other_ontology_annotation, self.ontology_annotation)
        self.assertNotEqual(
            hash(expected_other_ontology_annotation), hash(self.ontology_annotation))


class PublicationTest(unittest.TestCase):

    def setUp(self):
        self.publication_default = Publication()
        self.publication = Publication(
            pubmed_id='1', doi='10', author_list='A. Author', title='T',
            status=OntologyAnnotation(term='S'))

    def test_repr(self):
        self.assertEqual("isatools.model.Publication(pubmed_id='', "
                         "doi='', author_list='', title='', status=None, "
                         "comments=[])",
                         repr(self.publication_default))
        self.assertEqual("isatools.model.Publication(pubmed_id='1', "
                         "doi='10', author_list='A. Author', title='T', "
                         "status=isatools.model.OntologyAnnotation(term='S', "
                         "term_source=None, term_accession='', comments=[]), "
                         "comments=[])",
                         repr(self.publication))

    def test_str(self):
        self.assertEqual("""Publication(
    pubmed_id=
    doi=
    author_list=
    title=
    status=
    comments=0 Comment objects
)""", str(self.publication_default))

        self.assertEqual("""Publication(
    pubmed_id=1
    doi=10
    author_list=A. Author
    title=T
    status=S
    comments=0 Comment objects
)""", str(self.publication))

    def test_eq(self):
        expected_publication = Publication(
            pubmed_id='1', doi='10', author_list='A. Author', title='T', 
            status=OntologyAnnotation(term='S'))
        self.assertEqual(expected_publication, self.publication)
        self.assertEqual(
            hash(expected_publication),  hash(self.publication))

    def test_ne(self):
        expected_other_publication = Publication(
            pubmed_id='2', doi='20', author_list='B. Author', title='T2',
            status=OntologyAnnotation(term='S2'))
        self.assertNotEqual(expected_other_publication, self.publication)
        self.assertNotEqual(
            hash(expected_other_publication), hash(self.publication))


class PersonTest(unittest.TestCase):

    def setUp(self):
        self.person_default = Person()
        self.person = Person(last_name='L', first_name='F', mid_initials='M',
                             email='a@b.com', phone='0', fax='1', address='A',
                             affiliation='Af',
                             roles=[OntologyAnnotation(term='R')])

    def test_repr(self):
        self.assertEqual("isatools.model.Person(last_name='', first_name='', "
                         "mid_initials='', email='', phone='', fax='', "
                         "address='', affiliation='', roles=[], comments=[])",
                         repr(self.person_default))
        self.assertEqual("isatools.model.Person(last_name='L', first_name='F', "
                         "mid_initials='M', email='a@b.com', phone='0', "
                         "fax='1', address='A', affiliation='Af', "
                         "roles=[isatools.model.OntologyAnnotation(term='R', "
                         "term_source=None, term_accession='', comments=[])], "
                         "comments=[])",
                         repr(self.person))

    def test_str(self):
        self.assertEqual("""Person(
    last_name=
    first_name=
    mid_initials=
    email=
    phone=
    fax=
    address=
    roles=0 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.person_default))

        self.assertEqual("""Person(
    last_name=L
    first_name=F
    mid_initials=M
    email=a@b.com
    phone=0
    fax=1
    address=A
    roles=1 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.person))

    def test_eq(self):
        expected_person = Person(last_name='L', first_name='F', 
                                 mid_initials='M', email='a@b.com', phone='0', 
                                 fax='1', address='A', affiliation='Af', 
                                 roles=[OntologyAnnotation(
                                     term='R', term_source=None, 
                                     term_accession='', comments=[])], 
                                 comments=[])
        self.assertEqual(expected_person, self.person)
        self.assertEqual(hash(expected_person),  hash(self.person))

    def test_ne(self):
        expected_other_person = Person(last_name='F', first_name='L',
                                 mid_initials='M2', email='c@d.com', phone='1',
                                 fax='2', address='A2', affiliation='Af2',
                                 roles=[OntologyAnnotation(
                                     term='R2', term_source=None,
                                     term_accession='', comments=[])],
                                 comments=[])
        self.assertNotEqual(expected_other_person, self.person)
        self.assertNotEqual(
            hash(expected_other_person), hash(self.person))


class StudyTest(unittest.TestCase):

    def setUp(self):
        self.study_default = Study()
        self.study = Study(
            filename='file', identifier='0', title='T', description='D',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual("isatools.model.Study(filename='', "
                         "identifier='', title='', description='', "
                         "submission_date='', public_release_date='', "
                         "contacts=[], design_descriptors=[], publications=[], "
                         "factors=[], protocols=[], assays=[], sources=[], "
                         "samples=[], process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.study_default))
        self.assertEqual("isatools.model.Study(filename='file', "
                         "identifier='0', title='T', description='D', "
                         "submission_date='2017-01-01 00:00:00', "
                         "public_release_date='2017-01-01 00:00:00', "
                         "contacts=[], design_descriptors=[], publications=[], "
                         "factors=[], protocols=[], assays=[], sources=[], "
                         "samples=[], process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.study))

    def test_str(self):
        self.assertEqual("""Study(
    identifier=
    filename=
    title=
    description=
    submission_date=
    public_release_date=
    contacts=0 Person objects
    design_descriptors=0 OntologyAnnotation objects
    publications=0 Publication objects
    factors=0 StudyFactor objects
    protocols=0 Protocol objects
    assays=0 Assay objects
    sources=0 Source objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.study_default))

        self.assertEqual("""Study(
    identifier=0
    filename=file
    title=T
    description=D
    submission_date=2017-01-01 00:00:00
    public_release_date=2017-01-01 00:00:00
    contacts=0 Person objects
    design_descriptors=0 OntologyAnnotation objects
    publications=0 Publication objects
    factors=0 StudyFactor objects
    protocols=0 Protocol objects
    assays=0 Assay objects
    sources=0 Source objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.study))

    def test_eq(self):
        expected_study = Study(
            filename='file', identifier='0', title='T', description='D',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017),
            contacts=[], design_descriptors=[], publications=[], factors=[],
            protocols=[], assays=[], sources=[], samples=[],
            process_sequence=[], other_material=[],
            characteristic_categories=[], comments=[], units=[])
        self.assertEqual(expected_study, self.study)
        self.assertEqual(hash(expected_study),  hash(self.study))

    def test_ne(self):
        expected_other_study = Study(
            filename='file2', identifier='1', title='T2', description='D2',
            submission_date=datetime.datetime(day=2, month=1, year=2017),
            public_release_date=datetime.datetime(day=2, month=1, year=2017),
            contacts=[], design_descriptors=[], publications=[], factors=[],
            protocols=[], assays=[], sources=[], samples=[],
            process_sequence=[], other_material=[],
            characteristic_categories=[], comments=[], units=[])
        self.assertNotEqual(expected_other_study, self.study)
        self.assertNotEqual(hash(expected_other_study), hash(self.study))


class StudyFactorTest(unittest.TestCase):

    def setUp(self):
        self.factor_default = StudyFactor()
        self.factor = StudyFactor(name='N', factor_type=OntologyAnnotation('T'))

    def test_repr(self):
        self.assertEqual("isatools.model.StudyFactor(name='', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.factor_default))
        self.assertEqual("isatools.model.StudyFactor(name='N', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='T', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.factor))

    def test_str(self):
        self.assertEqual("""StudyFactor(
    name=
    factor_type=
    comments=0 Comment objects
)""", str(self.factor_default))

        self.assertEqual("""StudyFactor(
    name=N
    factor_type=T
    comments=0 Comment objects
)""", str(self.factor))

    def test_eq(self):
        expected_factor = StudyFactor(
            name='N', factor_type=OntologyAnnotation(term='T'))
        self.assertEqual(expected_factor, self.factor)
        self.assertEqual(hash(expected_factor),  hash(self.factor))

    def test_ne(self):
        expected_other_factor = StudyFactor(
            name='N2', factor_type=OntologyAnnotation(term='T2'))
        self.assertNotEqual(expected_other_factor, self.factor)
        self.assertNotEqual(hash(expected_other_factor), hash(self.factor))


class CharacteristicTest(unittest.TestCase):

    def setUp(self):
        self.characteristic_default = Characteristic()
        self.characteristic = Characteristic(
            category=OntologyAnnotation(term='C'), value=0,
            unit=OntologyAnnotation(term='U') )

    def test_repr(self):
        self.assertEqual("isatools.model.Characteristic("
                         "category=None, value=None, unit=None, comments=[])",
                         repr(self.characteristic_default))
        self.assertEqual("isatools.model.Characteristic("
                         "category=isatools.model.OntologyAnnotation("
                         "term='C', term_source=None, term_accession='', "
                         "comments=[]), value=0, "
                         "unit=isatools.model.OntologyAnnotation(term='U', "
                         "term_source=None, term_accession='', comments=[]), "
                         "comments=[])", repr(self.characteristic))

    def test_str(self):
        self.assertEqual("""Characteristic(
    category=
    value=
    unit=
    comments=0 Comment objects
)""", str(self.characteristic_default))

        self.assertEqual("""Characteristic(
    category=C
    value=0
    unit=U
    comments=0 Comment objects
)""", str(self.characteristic))

    def test_eq(self):
        expected_characteristic = Characteristic(
            category=OntologyAnnotation(term='C'), value=0,
            unit=OntologyAnnotation(term='U'))
        self.assertEqual(expected_characteristic, self.characteristic)
        self.assertEqual(
            hash(expected_characteristic), hash(self.characteristic))

    def test_ne(self):
        expected_other_characteristic = Characteristic(
            category=OntologyAnnotation(term='C2'), value=1,
            unit=OntologyAnnotation(term='U2'))
        self.assertNotEqual(expected_other_characteristic, self.characteristic)
        self.assertNotEqual(
            hash(expected_other_characteristic), hash(self.characteristic))


class AssayTest(unittest.TestCase):

    def setUp(self):
        self.assay_default = Assay()
        self.assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                           technology_type=OntologyAnnotation(term='TT'),
                           technology_platform='TP', filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.Assay(measurement_type="
                         "isatools.model.OntologyAnnotation(term='', "
                         "term_source=None, term_accession='', comments=[]), "
                         "technology_type=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), technology_platform='', filename='', "
                         "data_files=[], samples=[], process_sequence=[], "
                         "other_material=[], characteristic_categories=[], "
                         "comments=[], units=[])",
                         repr(self.assay_default))
        self.assertEqual("isatools.model.Assay(measurement_type="
                         "isatools.model.OntologyAnnotation(term='MT', "
                         "term_source=None, term_accession='', comments=[]), "
                         "technology_type=isatools.model.OntologyAnnotation("
                         "term='TT', term_source=None, term_accession='', "
                         "comments=[]), technology_platform='TP', "
                         "filename='file', data_files=[], samples=[], "
                         "process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.assay))

    def test_str(self):
        self.assertEqual("""Assay(
    measurement_type=
    technology_type=
    technology_platform=
    filename=
    data_files=0 DataFile objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.assay_default))

        self.assertEqual("""Assay(
    measurement_type=MT
    technology_type=TT
    technology_platform=TP
    filename=file
    data_files=0 DataFile objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.assay))

    def test_eq(self):
        expected_assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                           technology_type=OntologyAnnotation(term='TT'),
                           technology_platform='TP', filename='file')
        self.assertEqual(expected_assay, self.assay)
        self.assertEqual(hash(expected_assay),  hash(self.assay))

    def test_ne(self):
        expected_other_assay = Assay(
            measurement_type=OntologyAnnotation(term='MT2'),
            technology_type=OntologyAnnotation(term='TT2'),
            technology_platform='TP2', filename='file2')
        self.assertNotEqual(expected_other_assay, self.assay)
        self.assertNotEqual(hash(expected_other_assay), hash(self.assay))


class ProtocolTest(unittest.TestCase):

    def setUp(self):
        self.protocol_default = Protocol()
        self.protocol = Protocol(
            name='N', protocol_type=OntologyAnnotation(term='PT'), uri='U',
            version='1')

    @patch('pprint.pprint')
    def test_allowed_protocol_types(self, mock_pprint):
        protocol_types_dict = load_protocol_types_info()
        Protocol.show_allowed_protocol_types()
        mock_pprint.assert_called_with(protocol_types_dict)

    def test_repr(self):
        self.assertEqual("isatools.model.Protocol(name='', "
                         "protocol_type=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), uri='', version='', parameters=[], "
                         "components=[], comments=[])",
                         repr(self.protocol_default))
        self.assertEqual("isatools.model.Protocol(name='N', "
                         "protocol_type=isatools.model.OntologyAnnotation("
                         "term='PT', term_source=None, term_accession='', "
                         "comments=[]), uri='U', version='1', parameters=[], "
                         "components=[], comments=[])",
                         repr(self.protocol))

    def test_str(self):
        self.assertEqual("""Protocol(
    name=
    protocol_type=
    uri=
    version=
    parameters=0 ProtocolParameter objects
    components=0 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.protocol_default))

        self.assertEqual("""Protocol(
    name=N
    protocol_type=PT
    uri=U
    version=1
    parameters=0 ProtocolParameter objects
    components=0 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.protocol))

    def test_eq(self):
        expected_protocol = Protocol(
            name='N', protocol_type=OntologyAnnotation(term='PT'), uri='U',
            version='1')
        self.assertEqual(expected_protocol, self.protocol)
        self.assertEqual(hash(expected_protocol),  hash(self.protocol))

    def test_ne(self):
        expected_other_protocol = Protocol(
            name='N2', protocol_type=OntologyAnnotation(term='PT2'), uri='U2',
            version='2')
        self.assertNotEqual(expected_other_protocol, self.protocol)
        self.assertNotEqual(hash(expected_other_protocol), hash(self.protocol))


class ProtocolParameterTest(unittest.TestCase):

    def setUp(self):
        self.parameter_default = ProtocolParameter()
        self.parameter = ProtocolParameter(
            parameter_name=OntologyAnnotation(term='P'))

    def test_repr(self):
        self.assertEqual("isatools.model.ProtocolParameter("
                         "parameter_name=None, comments=[])",
                         repr(self.parameter_default))
        self.assertEqual("isatools.model.ProtocolParameter("
                         "parameter_name=isatools.model.OntologyAnnotation("
                         "term='P', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.parameter))

    def test_str(self):
        self.assertEqual("""ProtocolParameter(
    parameter_name=
    comments=0 Comment objects
)""", str(self.parameter_default))

        self.assertEqual("""ProtocolParameter(
    parameter_name=P
    comments=0 Comment objects
)""", str(self.parameter))

    def test_eq(self):
        expected_parameter = ProtocolParameter(
            parameter_name=OntologyAnnotation(term='P'))
        self.assertEqual(expected_parameter, self.parameter)
        self.assertEqual(hash(expected_parameter),  hash(self.parameter))

    def test_ne(self):
        expected_other_parameter = ProtocolParameter(
            parameter_name=OntologyAnnotation(term='P2'))
        self.assertNotEqual(expected_other_parameter, self.parameter)
        self.assertNotEqual(hash(expected_other_parameter), hash(self.parameter))


class ParameterValueTest(unittest.TestCase):

    def setUp(self):
        self.parameter_value_default = ParameterValue()
        self.parameter_value = ParameterValue(
            ProtocolParameter(parameter_name=OntologyAnnotation(term='P')),
            value=0, unit=OntologyAnnotation(term='U'))

    def test_repr(self):
        self.assertEqual("isatools.model.ParameterValue(category=None, "
                         "value=None, unit=None, comments=[])",
                         repr(self.parameter_value_default))
        self.assertEqual("isatools.model.ParameterValue("
                         "category=isatools.model.ProtocolParameter("
                         "parameter_name=isatools.model.OntologyAnnotation("
                         "term='P', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value=0, "
                         "unit=isatools.model.OntologyAnnotation("
                         "term='U', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.parameter_value))

    def test_str(self):
        self.assertEqual("""ParameterValue(
    category=
    value=None
    unit=
    comments=0 Comment objects
)""", str(self.parameter_value_default))

        self.assertEqual("""ParameterValue(
    category=P
    value=0
    unit=U
    comments=0 Comment objects
)""", str(self.parameter_value))

    def test_eq(self):
        expected_parameter_value = ParameterValue(
            ProtocolParameter(parameter_name=OntologyAnnotation(term='P')),
            value=0, unit=OntologyAnnotation(term='U'))
        self.assertEqual(expected_parameter_value, self.parameter_value)
        self.assertEqual(
            hash(expected_parameter_value),  hash(self.parameter_value))

    def test_ne(self):
        expected_other_parameter_value = ParameterValue(
            ProtocolParameter(parameter_name=OntologyAnnotation(term='P2')),
            value=1, unit=OntologyAnnotation(term='U2'))
        self.assertNotEqual(
            expected_other_parameter_value, self.parameter_value)
        self.assertNotEqual(
            hash(expected_other_parameter_value), hash(self.parameter_value))


class ProtocolComponentTest(unittest.TestCase):

    def setUp(self):
        self.component_default = ProtocolComponent()
        self.component = ProtocolComponent(
            name='C', component_type=OntologyAnnotation(term='CT'))

    def test_repr(self):
        self.assertEqual("isatools.model.ProtocolComponent(name='', "
                         "category=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.component_default))
        self.assertEqual("isatools.model.ProtocolComponent(name='C', "
                         "category=isatools.model.OntologyAnnotation("
                         "term='CT', term_source=None, term_accession='', "
                         "comments=[]), comments=[])",
                         repr(self.component))

    def test_str(self):
        self.assertEqual("""ProtocolComponent(
    name=
    category=
    comments=0 Comment objects
)""", str(self.component_default))

        self.assertEqual("""ProtocolComponent(
    name=C
    category=CT
    comments=0 Comment objects
)""", str(self.component))

    def test_eq(self):
        expected_component = ProtocolComponent(
            name='C', component_type=OntologyAnnotation(term='CT'))
        self.assertEqual(expected_component, self.component)
        self.assertEqual(
            hash(expected_component),  hash(self.component))

    def test_ne(self):
        expected_other_component = ProtocolComponent(
            name='C2', component_type=OntologyAnnotation(term='CT2'))
        self.assertNotEqual(expected_other_component, self.component)
        self.assertNotEqual(
            hash(expected_other_component), hash(self.component))
        

class SourceTest(unittest.TestCase):

    def setUp(self):
        self.source_default = Source()
        self.source = Source(name='S')

    def test_repr(self):
        self.assertEqual("isatools.model.Source(name='', characteristics=[], "
                         "comments=[])",
                         repr(self.source_default))
        self.assertEqual("isatools.model.Source(name='S', characteristics=[], "
                         "comments=[])",
                         repr(self.source))

    def test_str(self):
        self.assertEqual("""Source(
    name=
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.source_default))

        self.assertEqual("""Source(
    name=S
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.source))

    def test_eq(self):
        expected_source = Source(name='S')
        self.assertEqual(expected_source, self.source)
        self.assertEqual(hash(expected_source),  hash(self.source))

    def test_ne(self):
        expected_other_source = Source(name='S2')
        self.assertNotEqual(expected_other_source, self.source)
        self.assertNotEqual(hash(expected_other_source), hash(self.source))


class SampleTest(unittest.TestCase):

    def setUp(self):
        self.sample_default = Sample()
        self.sample = Sample(name='S')

    def test_repr(self):
        self.assertEqual("isatools.model.Sample(name='', characteristics=[], "
                         "factor_values=[], derives_from=[], comments=[])",
                         repr(self.sample_default))
        self.assertEqual("isatools.model.Sample(name='S', characteristics=[], "
                         "factor_values=[], derives_from=[], comments=[])",
                         repr(self.sample))

    def test_str(self):
        self.assertEqual("""Sample(
    name=
    characteristics=0 Characteristic objects
    factor_values=0 FactorValue objects
    derives_from=0 Source objects
    comments=0 Comment objects
)""", str(self.sample_default))

        self.assertEqual("""Sample(
    name=S
    characteristics=0 Characteristic objects
    factor_values=0 FactorValue objects
    derives_from=0 Source objects
    comments=0 Comment objects
)""", str(self.sample))

    def test_eq(self):
        expected_sample = Sample(name='S')
        self.assertEqual(expected_sample, self.sample)
        self.assertEqual(hash(expected_sample), hash(self.sample))

    def test_ne(self):
        expected_other_sample = Sample(name='S2')
        self.assertNotEqual(expected_other_sample, self.sample)
        self.assertNotEqual(hash(expected_other_sample), hash(self.sample))


class ExtractTest(unittest.TestCase):

    def setUp(self):
        self.extract_default = Extract()
        self.extract = Extract(name='E')

    def test_repr(self):
        self.assertEqual("isatools.model.Extract(name='', type='Extract Name', "
                         "characteristics=[], comments=[])",
                         repr(self.extract_default))
        self.assertEqual("isatools.model.Extract(name='E', "
                         "type='Extract Name', characteristics=[], "
                         "comments=[])",
                         repr(self.extract))

    def test_str(self):
        self.assertEqual("""Extract(
    name=
    type=Extract Name
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.extract_default))

        self.assertEqual("""Extract(
    name=E
    type=Extract Name
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.extract))

    def test_eq(self):
        expected_extract = Extract(name='E')
        self.assertEqual(expected_extract, self.extract)
        self.assertEqual(hash(expected_extract),  hash(self.extract))

    def test_ne(self):
        expected_other_extract = Extract(name='S2')
        self.assertNotEqual(expected_other_extract, self.extract)
        self.assertNotEqual(hash(expected_other_extract), hash(self.extract))


class LabeledExtractTest(unittest.TestCase):

    def setUp(self):
        self.labeled_extract_default = LabeledExtract()
        self.labeled_extract = LabeledExtract(name='E')

    def test_repr(self):
        self.assertEqual("isatools.model.LabeledExtract(name='', "
                         "type='Labeled Extract Name', characteristics=[], "
                         "comments=[])", repr(self.labeled_extract_default))
        self.assertEqual("isatools.model.LabeledExtract(name='E', "
                         "type='Labeled Extract Name', characteristics=[], "
                         "comments=[])", repr(self.labeled_extract))

    def test_str(self):
        self.assertEqual("""LabeledExtract(
    name=
    type=LabeledExtract Name
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.labeled_extract_default))

        self.assertEqual("""LabeledExtract(
    name=E
    type=LabeledExtract Name
    characteristics=0 Characteristic objects
    comments=0 Comment objects
)""", str(self.labeled_extract))

    def test_eq(self):
        expected_labeled_extract = LabeledExtract(name='E')
        self.assertEqual(expected_labeled_extract, self.labeled_extract)
        self.assertEqual(hash(expected_labeled_extract),
                         hash(self.labeled_extract))

    def test_ne(self):
        expected_other_labeled_extract = LabeledExtract(name='S2')
        self.assertNotEqual(expected_other_labeled_extract, self.labeled_extract)
        self.assertNotEqual(hash(expected_other_labeled_extract),
                            hash(self.labeled_extract))


class FactorValueTest(unittest.TestCase):

    def setUp(self):
        self.factor_value_default = FactorValue()
        self.factor_value = FactorValue(factor_name=StudyFactor(name='F'),
            value=0, unit=OntologyAnnotation(term='U'))

    def test_repr(self):
        self.assertEqual("isatools.model.FactorValue(factor_name=None, "
                         "value=None, unit=None)",
                         repr(self.factor_value_default))
        self.assertEqual("isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor(name='F', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value=0, "
                         "unit=isatools.model.OntologyAnnotation(term='U', "
                         "term_source=None, term_accession='', comments=[]))",
                         repr(self.factor_value))

    def test_str(self):
        self.assertEqual("""FactorValue(
    factor_name=
    value=None
    unit=
)""", str(self.factor_value_default))

        self.assertEqual("""FactorValue(
    factor_name=F
    value=0
    unit=U
)""", str(self.factor_value))

    def test_eq(self):
        expected_factor_value = FactorValue(factor_name=StudyFactor(name='F'),
            value=0, unit=OntologyAnnotation(term='U'))
        self.assertEqual(expected_factor_value, self.factor_value)
        self.assertEqual(
            hash(expected_factor_value),  hash(self.factor_value))

    def test_ne(self):
        expected_other_factor_value = FactorValue(
            factor_name=StudyFactor(name='F2'), value=1,
            unit=OntologyAnnotation(term='U2'))
        self.assertNotEqual(
            expected_other_factor_value, self.factor_value)
        self.assertNotEqual(
            hash(expected_other_factor_value), hash(self.factor_value))


class DataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = DataFile()
        self.data_file = DataFile(filename='file', label='Data File Name')

    def test_repr(self):
        self.assertEqual("isatools.model.DataFile(filename='', label='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.DataFile(filename='file', "
                         "label='Data File Name', generated_from=[], "
                         "comments=[])", repr(self.data_file))

    def test_str(self):
        self.assertEqual("""DataFile(
    filename=
    label=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""DataFile(
    filename=file
    label=Data File Name
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = DataFile(filename='file', label='Data File Name')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = DataFile(filename='file2',
                                            label='Raw Data File')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file), hash(self.data_file))


class RawDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = RawDataFile()
        self.data_file = RawDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.RawDataFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.RawDataFile(filename='file', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""RawDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""RawDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = RawDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = RawDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class DerivedDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = DerivedDataFile()
        self.data_file = DerivedDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.DerivedDataFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.DerivedDataFile(filename='file', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""DerivedDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""DerivedDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = DerivedDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = DerivedDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class RawSpectralDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = RawSpectralDataFile()
        self.data_file = RawSpectralDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.RawSpectralDataFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.RawSpectralDataFile(filename='file', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""RawSpectralDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""RawSpectralDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = RawSpectralDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = RawSpectralDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class ArrayDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = ArrayDataFile()
        self.data_file = ArrayDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.ArrayDataFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.ArrayDataFile(filename='file', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""ArrayDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""ArrayDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = ArrayDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = ArrayDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class DerivedSpectralDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = DerivedSpectralDataFile()
        self.data_file = DerivedSpectralDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.DerivedSpectralDataFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.DerivedSpectralDataFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""DerivedSpectralDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""DerivedSpectralDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = DerivedSpectralDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = DerivedSpectralDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class ProteinAssignmentFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = ProteinAssignmentFile()
        self.data_file = ProteinAssignmentFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.ProteinAssignmentFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.ProteinAssignmentFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""ProteinAssignmentFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""ProteinAssignmentFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = ProteinAssignmentFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = ProteinAssignmentFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class PeptideAssignmentFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = PeptideAssignmentFile()
        self.data_file = PeptideAssignmentFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.PeptideAssignmentFile(filename='', "
                         "generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.PeptideAssignmentFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""PeptideAssignmentFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""PeptideAssignmentFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = PeptideAssignmentFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = PeptideAssignmentFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class DerivedArrayDataMatrixFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = DerivedArrayDataMatrixFile()
        self.data_file = DerivedArrayDataMatrixFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.DerivedArrayDataMatrixFile("
                         "filename='', generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.DerivedArrayDataMatrixFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""DerivedArrayDataMatrixFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""DerivedArrayDataMatrixFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = DerivedArrayDataMatrixFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = DerivedArrayDataMatrixFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class PostTranslationalModificationAssignmentFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = PostTranslationalModificationAssignmentFile()
        self.data_file = PostTranslationalModificationAssignmentFile(
            filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model."
                         "PostTranslationalModificationAssignmentFile("
                         "filename='', generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model."
                         "PostTranslationalModificationAssignmentFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""PostTranslationalModificationAssignmentFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""PostTranslationalModificationAssignmentFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = PostTranslationalModificationAssignmentFile(
            filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = PostTranslationalModificationAssignmentFile(
            filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class AcquisitionParameterDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = AcquisitionParameterDataFile()
        self.data_file = AcquisitionParameterDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.AcquisitionParameterDataFile("
                         "filename='', generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.AcquisitionParameterDataFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""AcquisitionParameterDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""AcquisitionParameterDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = AcquisitionParameterDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = AcquisitionParameterDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))


class FreeInductionDecayDataFileTest(unittest.TestCase):

    def setUp(self):
        self.data_file_default = FreeInductionDecayDataFile()
        self.data_file = FreeInductionDecayDataFile(filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.FreeInductionDecayDataFile("
                         "filename='', generated_from=[], comments=[])",
                         repr(self.data_file_default))
        self.assertEqual("isatools.model.FreeInductionDecayDataFile("
                         "filename='file', generated_from=[], comments=[])",
                         repr(self.data_file))

    def test_str(self):
        self.assertEqual("""FreeInductionDecayDataFile(
    filename=
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file_default))

        self.assertEqual("""FreeInductionDecayDataFile(
    filename=file
    generated_from=0 Sample objects
    comments=0 Comment objects
)""", str(self.data_file))

    def test_eq(self):
        expected_data_file = FreeInductionDecayDataFile(filename='file')
        self.assertEqual(expected_data_file, self.data_file)
        self.assertEqual(hash(expected_data_file),  hash(self.data_file))

    def test_ne(self):
        expected_other_data_file = FreeInductionDecayDataFile(filename='file2')
        self.assertNotEqual(expected_other_data_file, self.data_file)
        self.assertNotEqual(hash(expected_other_data_file),
                            hash(self.data_file))