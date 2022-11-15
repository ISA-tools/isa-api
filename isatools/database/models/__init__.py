from isatools.database.models.comment import (
    CommentModel as Comment, Comment as CommentTable, make_comment_methods
)
from isatools.database.models.publication import (
    PublicationModel as Publication, Publication as PublicationTable, make_publication_methods
)
from isatools.database.models.investigation import (
    InvestigationModel as Investigation, Investigation as InvestigationTable, make_investigation_methods
)
from isatools.database.models.study import (
    StudyModel as Study, Study as StudyTable, make_study_methods
)
from isatools.database.models.ontology_annotation import (
    OntologyAnnotationModel as OntologyAnnotation, OntologyAnnotation as OntologyAnnotationTable,
    make_ontology_annotation_methods
)
from isatools.database.models.ontology_source import (
    OntologySourceModel as OntologySource, OntologySource as OntologySourceTable, make_ontology_source_methods
)
from isatools.database.models.parameter import (
    ParameterModel as Parameter, Parameter as ParameterTable, make_parameter_methods
)
from isatools.database.models.person import (
    PersonModel as Person, Person as PersonTable, make_person_methods
)
from isatools.database.models.process import (
    ProcessModel as Process, Process as ProcessTable, make_process_methods
)
from isatools.database.models.protocol import (
    ProtocolModel as Protocol, Protocol as ProtocolTable, make_protocol_methods
)
from isatools.database.models.source import (
    SourceModel as Source, Source as SourceTable, make_source_methods
)
from isatools.database.models.characteristic import (
    CharacteristicModel as Characteristic, Characteristic as CharacteristicTable, make_characteristic_methods
)
from isatools.database.models.study_factor import (
    StudyFactorModel as Factor, StudyFactor as FactorTable, make_study_factor_methods
)
from isatools.database.models.sample import (
    SampleModel as Sample, Sample as SampleTable, make_sample_methods
)
from isatools.database.models.factor_value import (
    FactorValueModel as FactorValue, FactorValue as FactorValueTable, make_factor_value_methods
)
from isatools.database.models.material import (
    MaterialModel as Material, Material as MaterialTable, make_material_methods
)
from isatools.database.models.parameter_value import (
    ParameterValueModel as ParameterValue, ParameterValue as ParameterValueTable, make_parameter_value_methods
)
from isatools.database.models.assay import (
    AssayModel as Assay, Assay as AssayTable, make_assay_methods
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

    # assays
    make_assay_methods()

    # investigation methods
    make_study_methods()
    make_investigation_methods()


__make_methods()
