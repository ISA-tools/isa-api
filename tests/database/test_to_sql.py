import json
import os
import unittest

from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session

from isatools.database import Comment, Investigation, OntologyAnnotation, Process, Publication, db

here = os.path.dirname(os.path.abspath(__file__))


def make_engine(foreign_keys=False):
    engine = create_engine("sqlite://")
    if foreign_keys:
        event.listen(engine, "connect", lambda connection, _: connection.execute("PRAGMA foreign_keys=ON"))
    db.metadata.create_all(engine)
    return engine


def load_investigation(name):
    with open(os.path.join(here, "..", "data", "json", name, f"{name}.json")) as f:
        investigation = Investigation()
        investigation.from_dict(json.load(f))
    return investigation


def count(session, model, *criteria):
    return session.scalar(select(func.count()).select_from(model.get_table()).where(*criteria))


class TestToSQL(unittest.TestCase):
    def test_comments_on_assay_factor_value_and_annotation(self):
        investigation = load_investigation("BII-I-1")
        study = investigation.studies[0]
        for commentable in (study.assays[0], study.samples[0].factor_values[0], study.design_descriptors[0]):
            commentable.comments.append(Comment(name="test", value="value"))
        with Session(make_engine()) as session:
            session.add(investigation.to_sql(session))
            session.commit()
            self.assertEqual(count(session, Comment, Comment.get_table().name == "test"), 3)

    def test_foreign_keys_enforced(self):
        investigation = load_investigation("BII-I-1")
        processes = {p.id for s in investigation.studies for owner in [s] + s.assays for p in owner.process_sequence}
        with Session(make_engine(foreign_keys=True)) as session:
            session.add(investigation.to_sql(session))
            session.commit()
            self.assertEqual(count(session, Investigation), 1)
            self.assertEqual(count(session, Process), len(processes))

    def test_rollback_leaves_no_rows(self):
        investigation = load_investigation("BII-I-1")
        with Session(make_engine(foreign_keys=True)) as session:
            investigation.to_sql(session)
            session.rollback()
            self.assertEqual(count(session, Process), 0)
            self.assertEqual(count(session, Publication), 0)

    def test_publications_without_doi_stay_separate(self):
        with Session(make_engine(foreign_keys=True)) as session:
            for title in ("First", "Second"):
                session.add(Publication(title=title, status=OntologyAnnotation(term="published")).to_sql(session))
            session.commit()
            titles = session.scalars(select(Publication.get_table().title)).all()
            self.assertEqual(sorted(titles), ["First", "Second"])
