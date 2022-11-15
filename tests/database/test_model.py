from unittest import TestCase
import os
from json import loads as json_loads

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from isatools.database import Base, Investigation


here = os.path.dirname(os.path.abspath(__file__))


def get_investigation(filename):
    with open(os.path.join(here, '..', "data", "json", filename, "%s.json" % filename)) as f:
        data = json_loads(f.read())
    investigation = Investigation()
    investigation.from_dict(data)
    return investigation


def create_db():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    _Session = sessionmaker(bind=engine)
    session_ = _Session()
    investigation = get_investigation("BII-S-3")
    session_.add(investigation.to_sql(session=session_))
    session_.commit()

    _investigation = session_.query(Investigation.get_table()).first().to_json()
    another_investigation = Investigation()
    another_investigation.from_dict(_investigation)
    return another_investigation.studies[0], investigation.studies[0], session_, investigation


study_from_db, study_expected, session, initial_investigation = create_db()


class TestStudyAssertions(TestCase):

    def test_base_assertions(self):
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
            sorted(study_from_db.other_material, key=lambda x: x.name),
            sorted(study_expected.other_material, key=lambda x: x.name))

    def test_sources_assertions(self):
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

    def test_samples_assertions(self):
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

    def test_contacts_assertions(self):
        contacts_1 = study_from_db.contacts
        contacts_2 = study_expected.contacts
        for contact in contacts_1:
            contact.roles = sorted(contact.roles, key=lambda d: d.term)
        for contact in contacts_2:
            contact.roles = sorted(contact.roles, key=lambda d: d.term)
        self.assertEqual(contacts_1, contacts_2)

    def test_protocols_assertions(self):
        protocols_1 = sorted(study_from_db.protocols, key=lambda x: x.name)
        protocols_2 = sorted(study_expected.protocols, key=lambda x: x.name)
        for i in range(len(protocols_1)):
            protocol_1 = protocols_1[i]
            protocol_2 = protocols_2[i]
            for param in protocol_1.parameters:
                self.assertIn(param, protocol_2.parameters)

    def test_characteristic_categories_assertions(self):
        characteristic_categories_1 = sorted(study_from_db.characteristic_categories, key=lambda x: x.term)
        characteristic_categories_2 = sorted(study_expected.characteristic_categories, key=lambda x: x.term)
        self.assertEqual(characteristic_categories_1, characteristic_categories_2)

    def test_process_sequence_assertion(self):
        process_sequence_1 = study_from_db.process_sequence
        process_sequence_2 = study_expected.process_sequence
        ps1 = [p.id for p in process_sequence_1]
        ps2 = [p.id for p in process_sequence_2]
        for sequence in ps1:
            self.assertIn(sequence, ps2)

    def test_load_more(self):
        investigation = get_investigation("BII-S-3")
        session.add(investigation.to_sql(session=session))
        session.commit()
        _investigation = session.query(Investigation.get_table()).all()
        self.assertEqual(len(_investigation), 2)

        investigation = get_investigation("BII-S-7")
        session.add(investigation.to_sql(session=session))
        session.commit()
        _investigation = session.query(Investigation.get_table()).all()
        self.assertEqual(len(_investigation), 3)

        investigation = get_investigation("BII-I-1")
        session.add(investigation.to_sql(session=session))
        session.commit()
        _investigation = session.query(Investigation.get_table()).all()
        self.assertEqual(len(_investigation), 4)