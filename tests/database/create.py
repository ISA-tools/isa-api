import os
from json import loads as json_loads

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from isatools.database import Base, Investigation


HERE = os.path.dirname(os.path.abspath(__file__))


def create_investigation(filename):
    with open(os.path.join(HERE, '..', "data", "json", filename, "%s.json" % filename)) as f:
        data = json_loads(f.read())
    investigation = Investigation()
    investigation.from_dict(data)
    return investigation


if __name__ == "__main__":
    engine = create_engine("sqlite:///test.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    investigation_ = create_investigation(filename="BII-S-3")
    investigation_.studies[0].assays = []

    session.add(investigation_.to_sql(session=session))
    session.commit()

    test = session.query(Investigation.get_table()).first()
    t = test.to_json()
    i = Investigation()
    i.from_dict(t)

    study_1 = i.studies[0]
    study_2 = investigation_.studies[0]

    # print('protocols')
    # print(study_1.protocols == study_2.protocols)
    #
    # print('characteristic_categories')
    # print(study_1.characteristic_categories == study_2.characteristic_categories)








