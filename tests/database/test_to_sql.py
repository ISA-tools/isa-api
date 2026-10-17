import json
import os
import unittest

from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session

from isatools.database import Comment, Investigation, db

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
