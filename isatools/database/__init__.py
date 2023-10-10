"""
The isatools database package contains the SQLAlchemy models for the ISA tools library.
It works by dynamically adding methods to the models defined in the isatools.model package.

The database model is highly sensitive to identifiers. We suggest serializing all your ISA-tab files to json
to enforce the generation of identifiers. This will ensure that the database model can be used to serialize the ISA
objects in SQLAlchemy.

Authors: D. Batista (@Terazus)
"""

from isatools.database.utils import app, db
from isatools.database.models import (
    Comment, Publication, Investigation, Study, OntologyAnnotation, OntologySource,
    Parameter, Person, Process, Protocol, Source, Characteristic, Factor, Sample,
    FactorValue, Material, ParameterValue, Assay, Datafile as DataFile
)
