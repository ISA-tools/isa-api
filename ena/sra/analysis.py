# ./sra_bindings.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2016-07-25 14:27:49.655881 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:94c23686-526b-11e6-9ec4-acbc328c3881')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import ena.sra._com as _ImportedBinding_com

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 28, 12)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.tab = STD_ANON._CF_enumeration.addEnumeration(unicode_value='tab', tag='tab')
STD_ANON.bam = STD_ANON._CF_enumeration.addEnumeration(unicode_value='bam', tag='bam')
STD_ANON.bai = STD_ANON._CF_enumeration.addEnumeration(unicode_value='bai', tag='bai')
STD_ANON.cram = STD_ANON._CF_enumeration.addEnumeration(unicode_value='cram', tag='cram')
STD_ANON.vcf = STD_ANON._CF_enumeration.addEnumeration(unicode_value='vcf', tag='vcf')
STD_ANON.vcf_aggregate = STD_ANON._CF_enumeration.addEnumeration(unicode_value='vcf_aggregate', tag='vcf_aggregate')
STD_ANON.tabix = STD_ANON._CF_enumeration.addEnumeration(unicode_value='tabix', tag='tabix')
STD_ANON.wig = STD_ANON._CF_enumeration.addEnumeration(unicode_value='wig', tag='wig')
STD_ANON.bed = STD_ANON._CF_enumeration.addEnumeration(unicode_value='bed', tag='bed')
STD_ANON.gff = STD_ANON._CF_enumeration.addEnumeration(unicode_value='gff', tag='gff')
STD_ANON.fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='fasta', tag='fasta')
STD_ANON.contig_fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='contig_fasta', tag='contig_fasta')
STD_ANON.contig_flatfile = STD_ANON._CF_enumeration.addEnumeration(unicode_value='contig_flatfile', tag='contig_flatfile')
STD_ANON.scaffold_fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='scaffold_fasta', tag='scaffold_fasta')
STD_ANON.scaffold_flatfile = STD_ANON._CF_enumeration.addEnumeration(unicode_value='scaffold_flatfile', tag='scaffold_flatfile')
STD_ANON.scaffold_agp = STD_ANON._CF_enumeration.addEnumeration(unicode_value='scaffold_agp', tag='scaffold_agp')
STD_ANON.chromosome_fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='chromosome_fasta', tag='chromosome_fasta')
STD_ANON.chromosome_flatfile = STD_ANON._CF_enumeration.addEnumeration(unicode_value='chromosome_flatfile', tag='chromosome_flatfile')
STD_ANON.chromosome_agp = STD_ANON._CF_enumeration.addEnumeration(unicode_value='chromosome_agp', tag='chromosome_agp')
STD_ANON.chromosome_list = STD_ANON._CF_enumeration.addEnumeration(unicode_value='chromosome_list', tag='chromosome_list')
STD_ANON.unlocalised_contig_list = STD_ANON._CF_enumeration.addEnumeration(unicode_value='unlocalised_contig_list', tag='unlocalised_contig_list')
STD_ANON.unlocalised_scaffold_list = STD_ANON._CF_enumeration.addEnumeration(unicode_value='unlocalised_scaffold_list', tag='unlocalised_scaffold_list')
STD_ANON.sample_list = STD_ANON._CF_enumeration.addEnumeration(unicode_value='sample_list', tag='sample_list')
STD_ANON.readme_file = STD_ANON._CF_enumeration.addEnumeration(unicode_value='readme_file', tag='readme_file')
STD_ANON.phenotype_file = STD_ANON._CF_enumeration.addEnumeration(unicode_value='phenotype_file', tag='phenotype_file')
STD_ANON.other = STD_ANON._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 80, 12)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_)
STD_ANON_.MD5 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='MD5', tag='MD5')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 220, 48)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_2)
STD_ANON_2.Whole_genome_sequencing = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='Whole genome sequencing', tag='Whole_genome_sequencing')
STD_ANON_2.Exome_sequencing = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='Exome sequencing', tag='Exome_sequencing')
STD_ANON_2.Genotyping_by_array = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='Genotyping by array', tag='Genotyping_by_array')
STD_ANON_2.transcriptomics = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='transcriptomics', tag='transcriptomics')
STD_ANON_2.Curation = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='Curation', tag='Curation')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 11, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 13, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace0_CTD_ANON_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace0_CTD_ANON_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace0_CTD_ANON_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })



# Complex type AnalysisSetType with content type ELEMENT_ONLY
class AnalysisSetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type AnalysisSetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnalysisSetType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 103, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS uses Python identifier ANALYSIS
    __ANALYSIS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS'), 'ANALYSIS', '__AbsentNamespace0_AnalysisSetType_ANALYSIS', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 105, 12), )

    
    ANALYSIS = property(__ANALYSIS.value, __ANALYSIS.set, None, None)

    _ElementMap.update({
        __ANALYSIS.name() : __ANALYSIS
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'AnalysisSetType', AnalysisSetType)


# Complex type AnalysisType with content type ELEMENT_ONLY
class AnalysisType (pyxb.binding.basis.complexTypeDefinition):
    """A SRA analysis object captures sequence analysis results including sequence alignments, sequence variations and sequence annotations.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnalysisType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 114, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_AnalysisType_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 120, 12), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TITLE'), 'TITLE', '__AbsentNamespace0_AnalysisType_TITLE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 121, 12), )

    
    TITLE = property(__TITLE.value, __TITLE.set, None, 'Title of the analyis object which will be displayed in\n                        database search results. ')

    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DESCRIPTION'), 'DESCRIPTION', '__AbsentNamespace0_AnalysisType_DESCRIPTION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 127, 12), )

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, 'Describes the analysis in detail.')

    
    # Element STUDY_REF uses Python identifier STUDY_REF
    __STUDY_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_REF'), 'STUDY_REF', '__AbsentNamespace0_AnalysisType_STUDY_REF', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 132, 12), )

    
    STUDY_REF = property(__STUDY_REF.value, __STUDY_REF.set, None, 'Establishes a relationship between the analysis and the\n                        parent study.')

    
    # Element SAMPLE_REF uses Python identifier SAMPLE_REF
    __SAMPLE_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_REF'), 'SAMPLE_REF', '__AbsentNamespace0_AnalysisType_SAMPLE_REF', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 144, 12), )

    
    SAMPLE_REF = property(__SAMPLE_REF.value, __SAMPLE_REF.set, None, 'One of more samples associated with the\n                        analysis.')

    
    # Element EXPERIMENT_REF uses Python identifier EXPERIMENT_REF
    __EXPERIMENT_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF'), 'EXPERIMENT_REF', '__AbsentNamespace0_AnalysisType_EXPERIMENT_REF', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 161, 12), )

    
    EXPERIMENT_REF = property(__EXPERIMENT_REF.value, __EXPERIMENT_REF.set, None, None)

    
    # Element RUN_REF uses Python identifier RUN_REF
    __RUN_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_REF'), 'RUN_REF', '__AbsentNamespace0_AnalysisType_RUN_REF', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 169, 12), )

    
    RUN_REF = property(__RUN_REF.value, __RUN_REF.set, None, 'One or more runs associated with the\n                        analysis.')

    
    # Element ANALYSIS_REF uses Python identifier ANALYSIS_REF
    __ANALYSIS_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_REF'), 'ANALYSIS_REF', '__AbsentNamespace0_AnalysisType_ANALYSIS_REF', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 186, 12), )

    
    ANALYSIS_REF = property(__ANALYSIS_REF.value, __ANALYSIS_REF.set, None, 'One or more runs associated with the\n                        analysis.')

    
    # Element ANALYSIS_TYPE uses Python identifier ANALYSIS_TYPE
    __ANALYSIS_TYPE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_TYPE'), 'ANALYSIS_TYPE', '__AbsentNamespace0_AnalysisType_ANALYSIS_TYPE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 203, 12), )

    
    ANALYSIS_TYPE = property(__ANALYSIS_TYPE.value, __ANALYSIS_TYPE.set, None, 'The type of the analysis. ')

    
    # Element FILES uses Python identifier FILES
    __FILES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FILES'), 'FILES', '__AbsentNamespace0_AnalysisType_FILES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 267, 16), )

    
    FILES = property(__FILES.value, __FILES.set, None, 'Files associated with the\n                                        analysis.')

    
    # Element ANALYSIS_LINKS uses Python identifier ANALYSIS_LINKS
    __ANALYSIS_LINKS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINKS'), 'ANALYSIS_LINKS', '__AbsentNamespace0_AnalysisType_ANALYSIS_LINKS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 282, 12), )

    
    ANALYSIS_LINKS = property(__ANALYSIS_LINKS.value, __ANALYSIS_LINKS.set, None, ' Links to resources related to this analysis.\n                    ')

    
    # Element ANALYSIS_ATTRIBUTES uses Python identifier ANALYSIS_ATTRIBUTES
    __ANALYSIS_ATTRIBUTES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTES'), 'ANALYSIS_ATTRIBUTES', '__AbsentNamespace0_AnalysisType_ANALYSIS_ATTRIBUTES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 293, 12), )

    
    ANALYSIS_ATTRIBUTES = property(__ANALYSIS_ATTRIBUTES.value, __ANALYSIS_ATTRIBUTES.set, None, 'Properties and attributes of an analysis. These can be\n                        entered as free-form tag-value pairs.')

    
    # Attribute analysis_center uses Python identifier analysis_center
    __analysis_center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'analysis_center'), 'analysis_center', '__AbsentNamespace0_AnalysisType_analysis_center', pyxb.binding.datatypes.string)
    __analysis_center._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 306, 8)
    __analysis_center._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 306, 8)
    
    analysis_center = property(__analysis_center.value, __analysis_center.set, None, 'If applicable, the center name of the institution responsible\n                    for this analysis. ')

    
    # Attribute analysis_date uses Python identifier analysis_date
    __analysis_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'analysis_date'), 'analysis_date', '__AbsentNamespace0_AnalysisType_analysis_date', pyxb.binding.datatypes.dateTime)
    __analysis_date._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 312, 8)
    __analysis_date._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 312, 8)
    
    analysis_date = property(__analysis_date.value, __analysis_date.set, None, 'The date when this analysis was produced. ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace0_AnalysisType_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace0_AnalysisType_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace0_AnalysisType_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_AnalysisType_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __TITLE.name() : __TITLE,
        __DESCRIPTION.name() : __DESCRIPTION,
        __STUDY_REF.name() : __STUDY_REF,
        __SAMPLE_REF.name() : __SAMPLE_REF,
        __EXPERIMENT_REF.name() : __EXPERIMENT_REF,
        __RUN_REF.name() : __RUN_REF,
        __ANALYSIS_REF.name() : __ANALYSIS_REF,
        __ANALYSIS_TYPE.name() : __ANALYSIS_TYPE,
        __FILES.name() : __FILES,
        __ANALYSIS_LINKS.name() : __ANALYSIS_LINKS,
        __ANALYSIS_ATTRIBUTES.name() : __ANALYSIS_ATTRIBUTES
    })
    _AttributeMap.update({
        __analysis_center.name() : __analysis_center,
        __analysis_date.name() : __analysis_date,
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })
Namespace.addCategoryObject('typeBinding', 'AnalysisType', AnalysisType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Establishes a relationship between the analysis and the
                        parent study."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 137, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON__IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 139, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace0_CTD_ANON__refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON__refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON__accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __refname.name() : __refname,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """One of more samples associated with the
                        analysis."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 149, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_2_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 151, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__AbsentNamespace0_CTD_ANON_2_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 154, 20)
    __label._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 154, 20)
    
    label = property(__label.value, __label.set, None, 'A label associating the sample with BAM (@RG/ID or @RG/SM) or VCF file samples.')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_2_refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_2_refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_2_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __label.name() : __label,
        __refname.name() : __refname,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 162, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_3_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 164, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_3_refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_3_refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_3_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __refname.name() : __refname,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """One or more runs associated with the
                        analysis."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 174, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_4_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 176, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__AbsentNamespace0_CTD_ANON_4_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 179, 20)
    __label._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 179, 20)
    
    label = property(__label.value, __label.set, None, 'A label associating the run with BAM (@RG/ID).')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_4_refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_4_refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_4_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __label.name() : __label,
        __refname.name() : __refname,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """One or more runs associated with the
                        analysis."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 191, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_5_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 193, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__AbsentNamespace0_CTD_ANON_5_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 196, 20)
    __label._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 196, 20)
    
    label = property(__label.value, __label.set, None, 'A label associating the run with BAM (@RG/ID).')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_5_refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_5_refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_5_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 57, 8)
    
    accession = property(__accession.value, __accession.set, None, '\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS
    })
    _AttributeMap.update({
        __label.name() : __label,
        __refname.name() : __refname,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """The type of the analysis. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 207, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element REFERENCE_ALIGNMENT uses Python identifier REFERENCE_ALIGNMENT
    __REFERENCE_ALIGNMENT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT'), 'REFERENCE_ALIGNMENT', '__AbsentNamespace0_CTD_ANON_6_REFERENCE_ALIGNMENT', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 209, 24), )

    
    REFERENCE_ALIGNMENT = property(__REFERENCE_ALIGNMENT.value, __REFERENCE_ALIGNMENT.set, None, '')

    
    # Element SEQUENCE_VARIATION uses Python identifier SEQUENCE_VARIATION
    __SEQUENCE_VARIATION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SEQUENCE_VARIATION'), 'SEQUENCE_VARIATION', '__AbsentNamespace0_CTD_ANON_6_SEQUENCE_VARIATION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 214, 24), )

    
    SEQUENCE_VARIATION = property(__SEQUENCE_VARIATION.value, __SEQUENCE_VARIATION.set, None, None)

    
    # Element SEQUENCE_ASSEMBLY uses Python identifier SEQUENCE_ASSEMBLY
    __SEQUENCE_ASSEMBLY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ASSEMBLY'), 'SEQUENCE_ASSEMBLY', '__AbsentNamespace0_CTD_ANON_6_SEQUENCE_ASSEMBLY', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 238, 24), )

    
    SEQUENCE_ASSEMBLY = property(__SEQUENCE_ASSEMBLY.value, __SEQUENCE_ASSEMBLY.set, None, None)

    
    # Element SEQUENCE_ANNOTATION uses Python identifier SEQUENCE_ANNOTATION
    __SEQUENCE_ANNOTATION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ANNOTATION'), 'SEQUENCE_ANNOTATION', '__AbsentNamespace0_CTD_ANON_6_SEQUENCE_ANNOTATION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 250, 24), )

    
    SEQUENCE_ANNOTATION = property(__SEQUENCE_ANNOTATION.value, __SEQUENCE_ANNOTATION.set, None, '')

    
    # Element REFERENCE_SEQUENCE uses Python identifier REFERENCE_SEQUENCE
    __REFERENCE_SEQUENCE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'REFERENCE_SEQUENCE'), 'REFERENCE_SEQUENCE', '__AbsentNamespace0_CTD_ANON_6_REFERENCE_SEQUENCE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 256, 24), )

    
    REFERENCE_SEQUENCE = property(__REFERENCE_SEQUENCE.value, __REFERENCE_SEQUENCE.set, None, None)

    
    # Element SAMPLE_PHENOTYPE uses Python identifier SAMPLE_PHENOTYPE
    __SAMPLE_PHENOTYPE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_PHENOTYPE'), 'SAMPLE_PHENOTYPE', '__AbsentNamespace0_CTD_ANON_6_SAMPLE_PHENOTYPE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 257, 24), )

    
    SAMPLE_PHENOTYPE = property(__SAMPLE_PHENOTYPE.value, __SAMPLE_PHENOTYPE.set, None, '')

    _ElementMap.update({
        __REFERENCE_ALIGNMENT.name() : __REFERENCE_ALIGNMENT,
        __SEQUENCE_VARIATION.name() : __SEQUENCE_VARIATION,
        __SEQUENCE_ASSEMBLY.name() : __SEQUENCE_ASSEMBLY,
        __SEQUENCE_ANNOTATION.name() : __SEQUENCE_ANNOTATION,
        __REFERENCE_SEQUENCE.name() : __REFERENCE_SEQUENCE,
        __SAMPLE_PHENOTYPE.name() : __SAMPLE_PHENOTYPE
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 239, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element NAME uses Python identifier NAME
    __NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NAME'), 'NAME', '__AbsentNamespace0_CTD_ANON_7_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 241, 36), )

    
    NAME = property(__NAME.value, __NAME.set, None, None)

    
    # Element PARTIAL uses Python identifier PARTIAL
    __PARTIAL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PARTIAL'), 'PARTIAL', '__AbsentNamespace0_CTD_ANON_7_PARTIAL', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 242, 36), )

    
    PARTIAL = property(__PARTIAL.value, __PARTIAL.set, None, None)

    
    # Element COVERAGE uses Python identifier COVERAGE
    __COVERAGE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'COVERAGE'), 'COVERAGE', '__AbsentNamespace0_CTD_ANON_7_COVERAGE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 243, 36), )

    
    COVERAGE = property(__COVERAGE.value, __COVERAGE.set, None, None)

    
    # Element PROGRAM uses Python identifier PROGRAM
    __PROGRAM = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PROGRAM'), 'PROGRAM', '__AbsentNamespace0_CTD_ANON_7_PROGRAM', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 244, 36), )

    
    PROGRAM = property(__PROGRAM.value, __PROGRAM.set, None, None)

    
    # Element PLATFORM uses Python identifier PLATFORM
    __PLATFORM = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PLATFORM'), 'PLATFORM', '__AbsentNamespace0_CTD_ANON_7_PLATFORM', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 245, 36), )

    
    PLATFORM = property(__PLATFORM.value, __PLATFORM.set, None, None)

    
    # Element MIN_GAP_LENGTH uses Python identifier MIN_GAP_LENGTH
    __MIN_GAP_LENGTH = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MIN_GAP_LENGTH'), 'MIN_GAP_LENGTH', '__AbsentNamespace0_CTD_ANON_7_MIN_GAP_LENGTH', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 246, 36), )

    
    MIN_GAP_LENGTH = property(__MIN_GAP_LENGTH.value, __MIN_GAP_LENGTH.set, None, None)

    _ElementMap.update({
        __NAME.name() : __NAME,
        __PARTIAL.name() : __PARTIAL,
        __COVERAGE.name() : __COVERAGE,
        __PROGRAM.name() : __PROGRAM,
        __PLATFORM.name() : __PLATFORM,
        __MIN_GAP_LENGTH.name() : __MIN_GAP_LENGTH
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 254, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 261, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Files associated with the
                                        analysis."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 272, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILE uses Python identifier FILE
    __FILE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FILE'), 'FILE', '__AbsentNamespace0_CTD_ANON_10_FILE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 275, 28), )

    
    FILE = property(__FILE.value, __FILE.set, None, None)

    _ElementMap.update({
        __FILE.name() : __FILE
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """ Links to resources related to this analysis.
                    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 287, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_LINK uses Python identifier ANALYSIS_LINK
    __ANALYSIS_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINK'), 'ANALYSIS_LINK', '__AbsentNamespace0_CTD_ANON_11_ANALYSIS_LINK', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 289, 24), )

    
    ANALYSIS_LINK = property(__ANALYSIS_LINK.value, __ANALYSIS_LINK.set, None, None)

    _ElementMap.update({
        __ANALYSIS_LINK.name() : __ANALYSIS_LINK
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Properties and attributes of an analysis. These can be
                        entered as free-form tag-value pairs."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 298, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_ATTRIBUTE uses Python identifier ANALYSIS_ATTRIBUTE
    __ANALYSIS_ATTRIBUTE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTE'), 'ANALYSIS_ATTRIBUTE', '__AbsentNamespace0_CTD_ANON_12_ANALYSIS_ATTRIBUTE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 300, 24), )

    
    ANALYSIS_ATTRIBUTE = property(__ANALYSIS_ATTRIBUTE.value, __ANALYSIS_ATTRIBUTE.set, None, None)

    _ElementMap.update({
        __ANALYSIS_ATTRIBUTE.name() : __ANALYSIS_ATTRIBUTE
    })
    _AttributeMap.update({
        
    })



# Complex type AnalysisFileType with content type ELEMENT_ONLY
class AnalysisFileType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type AnalysisFileType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnalysisFileType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 7, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CHECKLIST uses Python identifier CHECKLIST
    __CHECKLIST = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CHECKLIST'), 'CHECKLIST', '__AbsentNamespace0_AnalysisFileType_CHECKLIST', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 10, 12), )

    
    CHECKLIST = property(__CHECKLIST.value, __CHECKLIST.set, None, None)

    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'filename'), 'filename', '__AbsentNamespace0_AnalysisFileType_filename', pyxb.binding.datatypes.string, required=True)
    __filename._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 19, 8)
    __filename._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 19, 8)
    
    filename = property(__filename.value, __filename.set, None, 'The file name. ')

    
    # Attribute filetype uses Python identifier filetype
    __filetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'filetype'), 'filetype', '__AbsentNamespace0_AnalysisFileType_filetype', STD_ANON, required=True)
    __filetype._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 24, 8)
    __filetype._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 24, 8)
    
    filetype = property(__filetype.value, __filetype.set, None, 'The type of the file.')

    
    # Attribute checksum_method uses Python identifier checksum_method
    __checksum_method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'checksum_method'), 'checksum_method', '__AbsentNamespace0_AnalysisFileType_checksum_method', STD_ANON_, required=True)
    __checksum_method._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 76, 8)
    __checksum_method._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 76, 8)
    
    checksum_method = property(__checksum_method.value, __checksum_method.set, None, 'The checksum method. ')

    
    # Attribute checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'checksum'), 'checksum', '__AbsentNamespace0_AnalysisFileType_checksum', pyxb.binding.datatypes.string, required=True)
    __checksum._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 91, 8)
    __checksum._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 91, 8)
    
    checksum = property(__checksum.value, __checksum.set, None, 'The file checksum.')

    
    # Attribute unencrypted_checksum uses Python identifier unencrypted_checksum
    __unencrypted_checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unencrypted_checksum'), 'unencrypted_checksum', '__AbsentNamespace0_AnalysisFileType_unencrypted_checksum', pyxb.binding.datatypes.string)
    __unencrypted_checksum._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 96, 8)
    __unencrypted_checksum._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 96, 8)
    
    unencrypted_checksum = property(__unencrypted_checksum.value, __unencrypted_checksum.set, None, 'The checksum of the unencrypted file (used in conjunction with the checksum of an encrypted file).\n                ')

    _ElementMap.update({
        __CHECKLIST.name() : __CHECKLIST
    })
    _AttributeMap.update({
        __filename.name() : __filename,
        __filetype.name() : __filetype,
        __checksum_method.name() : __checksum_method,
        __checksum.name() : __checksum,
        __unencrypted_checksum.name() : __unencrypted_checksum
    })
Namespace.addCategoryObject('typeBinding', 'AnalysisFileType', AnalysisFileType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_13 (_ImportedBinding_com.ReferenceSequenceType):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 215, 28)
    _ElementMap = _ImportedBinding_com.ReferenceSequenceType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_com.ReferenceSequenceType._AttributeMap.copy()
    # Base type is _ImportedBinding_com.ReferenceSequenceType
    
    # Element EXPERIMENT_TYPE uses Python identifier EXPERIMENT_TYPE
    __EXPERIMENT_TYPE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_TYPE'), 'EXPERIMENT_TYPE', '__AbsentNamespace0_CTD_ANON_13_EXPERIMENT_TYPE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 219, 44), )

    
    EXPERIMENT_TYPE = property(__EXPERIMENT_TYPE.value, __EXPERIMENT_TYPE.set, None, None)

    
    # Element PROGRAM uses Python identifier PROGRAM
    __PROGRAM = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PROGRAM'), 'PROGRAM', '__AbsentNamespace0_CTD_ANON_13_PROGRAM', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 230, 44), )

    
    PROGRAM = property(__PROGRAM.value, __PROGRAM.set, None, None)

    
    # Element PLATFORM uses Python identifier PLATFORM
    __PLATFORM = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PLATFORM'), 'PLATFORM', '__AbsentNamespace0_CTD_ANON_13_PLATFORM', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 231, 44), )

    
    PLATFORM = property(__PLATFORM.value, __PLATFORM.set, None, None)

    
    # Element IMPUTATION uses Python identifier IMPUTATION
    __IMPUTATION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IMPUTATION'), 'IMPUTATION', '__AbsentNamespace0_CTD_ANON_13_IMPUTATION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 232, 44), )

    
    IMPUTATION = property(__IMPUTATION.value, __IMPUTATION.set, None, None)

    
    # Element ASSEMBLY (ASSEMBLY) inherited from {SRA.common}ReferenceSequenceType
    
    # Element SEQUENCE (SEQUENCE) inherited from {SRA.common}ReferenceSequenceType
    _ElementMap.update({
        __EXPERIMENT_TYPE.name() : __EXPERIMENT_TYPE,
        __PROGRAM.name() : __PROGRAM,
        __PLATFORM.name() : __PLATFORM,
        __IMPUTATION.name() : __IMPUTATION
    })
    _AttributeMap.update({
        
    })



ANALYSIS_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ANALYSIS_SET'), AnalysisSetType, documentation='A container of analysis objects. ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 108, 4))
Namespace.addCategoryObject('elementBinding', ANALYSIS_SET.name().localName(), ANALYSIS_SET)

ANALYSIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ANALYSIS'), AnalysisType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 113, 4))
Namespace.addCategoryObject('elementBinding', ANALYSIS.name().localName(), ANALYSIS)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 13, 24)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 13, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 13, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




AnalysisSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS'), AnalysisType, scope=AnalysisSetType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 105, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AnalysisSetType._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 105, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AnalysisSetType._Automaton = _BuildAutomaton_()




AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=AnalysisType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 120, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TITLE'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation='Title of the analyis object which will be displayed in\n                        database search results. ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 121, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DESCRIPTION'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation='Describes the analysis in detail.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 127, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_REF'), CTD_ANON_, scope=AnalysisType, documentation='Establishes a relationship between the analysis and the\n                        parent study.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 132, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_REF'), CTD_ANON_2, scope=AnalysisType, documentation='One of more samples associated with the\n                        analysis.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 144, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF'), CTD_ANON_3, scope=AnalysisType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 161, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_REF'), CTD_ANON_4, scope=AnalysisType, documentation='One or more runs associated with the\n                        analysis.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 169, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_REF'), CTD_ANON_5, scope=AnalysisType, documentation='One or more runs associated with the\n                        analysis.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 186, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_TYPE'), CTD_ANON_6, scope=AnalysisType, documentation='The type of the analysis. ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 203, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FILES'), CTD_ANON_10, scope=AnalysisType, documentation='Files associated with the\n                                        analysis.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 267, 16)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINKS'), CTD_ANON_11, scope=AnalysisType, documentation=' Links to resources related to this analysis.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 282, 12)))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTES'), CTD_ANON_12, scope=AnalysisType, documentation='Properties and attributes of an analysis. These can be\n                        entered as free-form tag-value pairs.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 293, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 120, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 132, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 144, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 161, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 169, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 186, 12))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 282, 12))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 293, 12))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 120, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'TITLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 121, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'DESCRIPTION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 127, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 132, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 144, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 161, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 169, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 186, 12))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_TYPE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 203, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'FILES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 267, 16))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINKS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 282, 12))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 293, 12))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AnalysisType._Automaton = _BuildAutomaton_2()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 139, 24)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 139, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 139, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_3()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 151, 24)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 151, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 151, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_4()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 164, 24)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 164, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 164, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_5()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 176, 24)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 176, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 176, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_6()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 193, 24)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 193, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 193, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_7()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT'), _ImportedBinding_com.ReferenceSequenceType, scope=CTD_ANON_6, documentation='', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 209, 24)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SEQUENCE_VARIATION'), CTD_ANON_13, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 214, 24)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ASSEMBLY'), CTD_ANON_7, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 238, 24)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ANNOTATION'), CTD_ANON_8, scope=CTD_ANON_6, documentation='', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 250, 24)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'REFERENCE_SEQUENCE'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 256, 24)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_PHENOTYPE'), CTD_ANON_9, scope=CTD_ANON_6, documentation='', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 257, 24)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 209, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'SEQUENCE_VARIATION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 214, 24))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ASSEMBLY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 238, 24))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'SEQUENCE_ANNOTATION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 250, 24))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'REFERENCE_SEQUENCE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 256, 24))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_PHENOTYPE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 257, 24))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_8()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 241, 36)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PARTIAL'), pyxb.binding.datatypes.boolean, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 242, 36)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'COVERAGE'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 243, 36)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PROGRAM'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 244, 36)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PLATFORM'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 245, 36)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MIN_GAP_LENGTH'), pyxb.binding.datatypes.integer, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 246, 36)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 246, 36))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 241, 36))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'PARTIAL')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 242, 36))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'COVERAGE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 243, 36))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'PROGRAM')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 244, 36))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'PLATFORM')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 245, 36))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'MIN_GAP_LENGTH')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 246, 36))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_9()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FILE'), AnalysisFileType, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 275, 28)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'FILE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 275, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_10()




CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINK'), _ImportedBinding_com.LinkType, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 289, 24)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 289, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_11()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTE'), _ImportedBinding_com.AttributeType, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 300, 24)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'ANALYSIS_ATTRIBUTE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 300, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_12()




AnalysisFileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CHECKLIST'), CTD_ANON, scope=AnalysisFileType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 10, 12)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnalysisFileType._UseForTag(pyxb.namespace.ExpandedName(None, 'CHECKLIST')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AnalysisFileType._Automaton = _BuildAutomaton_13()




CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_TYPE'), STD_ANON_2, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 219, 44)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PROGRAM'), pyxb.binding.datatypes.string, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 230, 44)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PLATFORM'), pyxb.binding.datatypes.string, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 231, 44)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IMPUTATION'), pyxb.binding.datatypes.boolean, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 232, 44)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 807, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 812, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 219, 44))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 230, 44))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 231, 44))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 232, 44))
    counters.add(cc_5)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'ASSEMBLY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 807, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'SEQUENCE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 812, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_TYPE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 219, 44))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'PROGRAM')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 230, 44))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'PLATFORM')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 231, 44))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'IMPUTATION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.analysis.xsd', 232, 44))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_13._Automaton = _BuildAutomaton_14()

