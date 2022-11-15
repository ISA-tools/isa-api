"""
The isatools.database package contains the SQLAlchemy models for the ISA tools library.
It works by dynamically adding methods to the models defined in the isatools.model package.

The database model is highly sensitive to identifiers. We suggest serializing all your ISA-tab files to json
to enforce the generation of identifiers. This will ensure that the database model can be used to serialize the ISA
objects in SQLAlchemy.

Authors: D. Batista (@Terazus)

Example:
    >>> from isatools.database import Investigation, Base
    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.orm import sessionmaker
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> investigation = Investigation()
    >>> to_insert = investigation.to_sql(session=session)
    >>> session.add(to_insert)
    >>> session.commit()
    >>> investigation_table = investigation.get_table()
    >>> session.query(investigation_table).get(to_insert.id)  # returns the object from the database
"""

from isatools.database.utils import Base
from isatools.database.models import Investigation
