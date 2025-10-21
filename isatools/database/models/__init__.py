from isatools.database.models.assay import Assay as AssayTable
from isatools.database.models.assay import AssayModel as Assay
from isatools.database.models.assay import make_assay_methods
from isatools.database.models.characteristic import (
    Characteristic as CharacteristicTable,
)
from isatools.database.models.characteristic import (
    CharacteristicModel as Characteristic,
)
from isatools.database.models.characteristic import (
    make_characteristic_methods,
)
from isatools.database.models.comment import Comment as CommentTable
from isatools.database.models.comment import CommentModel as Comment
from isatools.database.models.comment import make_comment_methods
from isatools.database.models.datafile import (
    Datafile as DatafileTable,
)
from isatools.database.models.datafile import (
    DataFileModel as Datafile,
)
from isatools.database.models.datafile import (
    make_datafile_methods,
)
from isatools.database.models.factor_value import (
    FactorValue as FactorValueTable,
)
from isatools.database.models.factor_value import (
    FactorValueModel as FactorValue,
)
from isatools.database.models.factor_value import (
    make_factor_value_methods,
)
from isatools.database.models.investigation import (
    Investigation as InvestigationTable,
)
from isatools.database.models.investigation import (
    InvestigationModel as Investigation,
)
from isatools.database.models.investigation import (
    make_investigation_methods,
)
from isatools.database.models.material import (
    Material as MaterialTable,
)
from isatools.database.models.material import (
    MaterialModel as Material,
)
from isatools.database.models.material import (
    make_material_methods,
)
from isatools.database.models.ontology_annotation import (
    OntologyAnnotation as OntologyAnnotationTable,
)
from isatools.database.models.ontology_annotation import (
    OntologyAnnotationModel as OntologyAnnotation,
)
from isatools.database.models.ontology_annotation import (
    make_ontology_annotation_methods,
)
from isatools.database.models.ontology_source import (
    OntologySource as OntologySourceTable,
)
from isatools.database.models.ontology_source import (
    OntologySourceModel as OntologySource,
)
from isatools.database.models.ontology_source import (
    make_ontology_source_methods,
)
from isatools.database.models.parameter import (
    Parameter as ParameterTable,
)
from isatools.database.models.parameter import (
    ParameterModel as Parameter,
)
from isatools.database.models.parameter import (
    make_parameter_methods,
)
from isatools.database.models.parameter_value import (
    ParameterValue as ParameterValueTable,
)
from isatools.database.models.parameter_value import (
    ParameterValueModel as ParameterValue,
)
from isatools.database.models.parameter_value import (
    make_parameter_value_methods,
)
from isatools.database.models.person import Person as PersonTable
from isatools.database.models.person import PersonModel as Person
from isatools.database.models.person import make_person_methods
from isatools.database.models.process import Process as ProcessTable
from isatools.database.models.process import ProcessModel as Process
from isatools.database.models.process import make_process_methods
from isatools.database.models.protocol import (
    Protocol as ProtocolTable,
)
from isatools.database.models.protocol import (
    ProtocolModel as Protocol,
)
from isatools.database.models.protocol import (
    make_protocol_methods,
)
from isatools.database.models.publication import (
    Publication as PublicationTable,
)
from isatools.database.models.publication import (
    PublicationModel as Publication,
)
from isatools.database.models.publication import (
    make_publication_methods,
)
from isatools.database.models.sample import Sample as SampleTable
from isatools.database.models.sample import SampleModel as Sample
from isatools.database.models.sample import make_sample_methods
from isatools.database.models.source import Source as SourceTable
from isatools.database.models.source import SourceModel as Source
from isatools.database.models.source import make_source_methods
from isatools.database.models.study import Study as StudyTable
from isatools.database.models.study import StudyModel as Study
from isatools.database.models.study import make_study_methods
from isatools.database.models.study_factor import (
    StudyFactor as FactorTable,
)
from isatools.database.models.study_factor import (
    StudyFactorModel as Factor,
)
from isatools.database.models.study_factor import (
    make_study_factor_methods,
)


def __make_methods():
    # base methods
    make_comment_methods()
    make_ontology_source_methods()
    make_ontology_annotation_methods()
    make_publication_methods()
    make_person_methods()

    # studies methods
    make_parameter_methods()
    make_parameter_value_methods()
    make_process_methods()
    make_protocol_methods()
    make_study_factor_methods()
    make_factor_value_methods()

    # materials methods
    make_characteristic_methods()
    make_source_methods()
    make_sample_methods()
    make_material_methods()
    make_datafile_methods()

    # assays
    make_assay_methods()

    # investigation methods
    make_study_methods()
    make_investigation_methods()


__make_methods()
