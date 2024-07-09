from unittest import TestCase
import os
from json import loads as json_loads

from isatools.database import *


here = os.path.dirname(os.path.abspath(__file__))


def get_investigation(filename):
    with open(os.path.join(here, '..', "data", "json", filename, "%s.json" % filename)) as f:
        data = json_loads(f.read())
    investigation = Investigation()
    investigation.from_dict(data)
    return investigation


def create_db():
    investigation = get_investigation("BII-I-1")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(investigation.to_sql(session=db.session))
        _investigation = db.session.query(Investigation.get_table()).first().to_json()
        another_investigation = Investigation()
        another_investigation.from_dict(_investigation)
        db.session.commit()

    return another_investigation, investigation


investigation_from_db, initial_investigation = create_db()
study_from_db = investigation_from_db.studies[0]
study_expected = initial_investigation.studies[0]


class TestAssertions(TestCase):

    def test_investigation_base_assertions(self):
        self.assertEqual(
            sorted(investigation_from_db.ontology_source_references, key=lambda d: d.name),
            sorted(initial_investigation.ontology_source_references, key=lambda d: d.name)
        )

    def test_study_base_assertions(self):
        self.assertEqual(study_from_db.comments, study_expected.comments)
        self.assertEqual(
            sorted(study_from_db.publications, key=lambda d: d.title),
            sorted(study_expected.publications, key=lambda d: d.title))
        self.assertEqual(
            sorted(study_from_db.factors, key=lambda d: d.name),
            sorted(study_expected.factors, key=lambda d: d.name))
        self.assertEqual(
            sorted(study_from_db.units, key=lambda d: d.term),
            sorted(study_expected.units, key=lambda d: d.term))
        self.assertEqual(
            sorted(study_from_db.design_descriptors, key=lambda d: d.term),
            sorted(study_expected.design_descriptors, key=lambda d: d.term))
        self.assertEqual(
            sorted(study_from_db.other_material, key=lambda x: x.name),
            sorted(study_expected.other_material, key=lambda x: x.name))

    def test_study_sources_assertions(self):
        sources_1 = sorted(study_from_db.sources, key=lambda x: x.name)
        sources_2 = sorted(study_expected.sources, key=lambda x: x.name)
        self.assertEqual(len(sources_1), len(sources_2))
        for index in range(len(sources_1)):
            source_1 = sources_1[index]
            source_2 = sources_2[index]
            self.assertEqual(source_1.name, source_2.name)
            self.assertEqual(len(source_1.characteristics), len(source_2.characteristics))
            for _index in range(len(source_1.characteristics)):
                characteristic_1 = source_1.characteristics[_index]
                self.assertIn(characteristic_1, source_2.characteristics)

    def test_study_samples_assertions(self):
        samples_1 = sorted(study_from_db.samples, key=lambda x: x.name)
        samples_2 = sorted(study_expected.samples, key=lambda x: x.name)
        for index in range(len(samples_1)):
            sample_1 = samples_1[index]
            sample_2 = samples_2[index]
            self.assertEqual(len(sample_1.characteristics), len(sample_2.characteristics))
            for _index in range(len(sample_1.characteristics)):
                characteristic_1 = sample_1.characteristics[_index]
                self.assertIn(characteristic_1, sample_2.characteristics)
            self.assertEqual(len(sample_1.factor_values), len(sample_2.factor_values))
            for _index in range(len(sample_1.factor_values)):
                factor_value_1 = sample_1.factor_values[_index]
                self.assertIn(factor_value_1, sample_2.factor_values)

    def test_study_contacts_assertions(self):
        contacts_1 = study_from_db.contacts
        contacts_2 = study_expected.contacts
        for contact in contacts_1:
            contact.roles = sorted(contact.roles, key=lambda d: d.term)
        for contact in contacts_2:
            contact.roles = sorted(contact.roles, key=lambda d: d.term)
        self.assertEqual(contacts_1, contacts_2)

    def test_study_protocols_assertions(self):
        protocols_1 = sorted(study_from_db.protocols, key=lambda x: x.name)
        protocols_2 = sorted(study_expected.protocols, key=lambda x: x.name)
        for i in range(len(protocols_1)):
            protocol_1 = protocols_1[i]
            protocol_2 = protocols_2[i]
            for param in protocol_1.parameters:
                self.assertIn(param, protocol_2.parameters)

    def test_study_characteristic_categories_assertions(self):
        characteristic_categories_1 = sorted(study_from_db.characteristic_categories, key=lambda x: x.term)
        characteristic_categories_2 = sorted(study_expected.characteristic_categories, key=lambda x: x.term)
        self.assertEqual(characteristic_categories_1, characteristic_categories_2)

    def test_study_process_sequence_assertion(self):
        process_sequence_1 = study_from_db.process_sequence
        process_sequence_2 = study_expected.process_sequence
        for sequence_1 in process_sequence_1:
            sequence_2 = [s for s in process_sequence_2 if s.id == sequence_1.id][0]
            self.assertEqual(sequence_1, sequence_2)

    def test_assay_base_assertions(self):
        assays_from_db = study_from_db.assays
        assays_expected = study_expected.assays

        for assay_1 in assays_from_db:
            assay_2 = [a for a in assays_expected if a.filename == assay_1.filename][0]
            self.assertEqual(assay_1.measurement_type, assay_2.measurement_type)
            self.assertEqual(assay_1.technology_type, assay_2.technology_type)
            self.assertEqual(assay_1.technology_platform, assay_2.technology_platform)
            self.assertEqual(
                sorted(assay_1.units, key=lambda d: d.term),
                sorted(assay_2.units, key=lambda d: d.term))
            self.assertEqual(
                sorted(assay_1.characteristic_categories, key=lambda d: d.term),
                sorted(assay_2.characteristic_categories, key=lambda d: d.term))
            process_sequence_1 = assay_1.process_sequence
            process_sequence_2 = assay_2.process_sequence
            for sequence_1 in process_sequence_1:
                sequence_2 = [s for s in process_sequence_2 if s.id == sequence_1.id][0]
                self.assertEqual(sequence_1, sequence_2)

    def test_load_more(self):
        with app.app_context():
            session = db.session
            investigation = get_investigation("BII-I-1")
            session.add(investigation.to_sql(session=session))
            session.commit()
            i = initial_investigation
            self.assertEqual(investigation, i)

            _investigation = session.query(Investigation.get_table()).all()
            self.assertEqual(len(_investigation), 2)

            investigation = get_investigation("BII-S-7")
            session.add(investigation.to_sql(session=session))
            session.commit()
            _investigation = session.query(Investigation.get_table()).all()
            self.assertEqual(len(_investigation), 3)

            investigation = get_investigation("BII-S-3")
            print(type(investigation))
            session.add(investigation.to_sql(session=session))
            session.commit()
            _investigation = session.query(Investigation.get_table()).all()
            self.assertEqual(len(_investigation), 4)