"""
The isatools.database package contains the SQLAlchemy models for the ISA tools library.
It works by dynamically adding methods to the models defined in the isatools.model package.

The database model is highly sensitive to identifiers. We suggest serializing all your ISA-tab files to json
to enforce the generation of identifiers. This will ensure that the database model can be used to serialize the ISA
objects in SQLAlchemy.

Authors: D. Batista (@Terazus)

Example:
    >>> from isatools.database import Investigation, Base
    >>> investigation = Investigation()
    >>> to_insert = investigation.to_sql()
    Note: The to_insert object is an SQLAlchemy object ready to be added to an SQLAlchemy session using the shared Base.
    >>> investigation_table = investigation.get_table()
    Note: The investigation_table object is the SQLAlchemy table object derived for the investigation model.
"""

from isatools.database.utils import Base
from isatools.database.models import (
    Comment,
    Investigation,
    Study,
    Publication,
    OntologyAnnotation,
    OntologySource,
    Parameter,
    Person,
    Process,
    Protocol,
    Source,
    Characteristic
)



