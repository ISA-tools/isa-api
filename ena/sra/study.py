# ./binding_3.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2016-07-25 14:27:49.655643 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace AbsentNamespace4

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
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 38, 16)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.Whole_Genome_Sequencing = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Whole Genome Sequencing', tag='Whole_Genome_Sequencing')
STD_ANON.Metagenomics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Metagenomics', tag='Metagenomics')
STD_ANON.Transcriptome_Analysis = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Transcriptome Analysis', tag='Transcriptome_Analysis')
STD_ANON.Resequencing = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Resequencing', tag='Resequencing')
STD_ANON.Epigenetics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Epigenetics', tag='Epigenetics')
STD_ANON.Synthetic_Genomics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Synthetic Genomics', tag='Synthetic_Genomics')
STD_ANON.Forensic_or_Paleo_genomics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Forensic or Paleo-genomics', tag='Forensic_or_Paleo_genomics')
STD_ANON.Gene_Regulation_Study = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Gene Regulation Study', tag='Gene_Regulation_Study')
STD_ANON.Cancer_Genomics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Cancer Genomics', tag='Cancer_Genomics')
STD_ANON.Population_Genomics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Population Genomics', tag='Population_Genomics')
STD_ANON.RNASeq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='RNASeq', tag='RNASeq')
STD_ANON.Exome_Sequencing = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Exome Sequencing', tag='Exome_Sequencing')
STD_ANON.Pooled_Clone_Sequencing = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Pooled Clone Sequencing', tag='Pooled_Clone_Sequencing')
STD_ANON.Other = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Other', tag='Other')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Complex type StudyType with content type ELEMENT_ONLY
class StudyType (pyxb.binding.basis.complexTypeDefinition):
    """
          A Study is a container for a sequencing investigation that may comprise multiple experiments.
          The Study has an overall goal, but is otherwise minimally defined in the SRA.
          A Study is composed of a descriptor, zero or more experiments, and zero or more analyses.
          The submitter may decorate the Study with web links and properties.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StudyType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 8, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace4_StudyType_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 20, 6), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Element DESCRIPTOR uses Python identifier DESCRIPTOR
    __DESCRIPTOR = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DESCRIPTOR'), 'DESCRIPTOR', '__AbsentNamespace4_StudyType_DESCRIPTOR', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 22, 6), )

    
    DESCRIPTOR = property(__DESCRIPTOR.value, __DESCRIPTOR.set, None, None)

    
    # Element STUDY_LINKS uses Python identifier STUDY_LINKS
    __STUDY_LINKS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_LINKS'), 'STUDY_LINKS', '__AbsentNamespace4_StudyType_STUDY_LINKS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 225, 8), )

    
    STUDY_LINKS = property(__STUDY_LINKS.value, __STUDY_LINKS.set, None, '\n                  Links to resources related to this study (publication, datasets, online databases).\n              ')

    
    # Element STUDY_ATTRIBUTES uses Python identifier STUDY_ATTRIBUTES
    __STUDY_ATTRIBUTES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTES'), 'STUDY_ATTRIBUTES', '__AbsentNamespace4_StudyType_STUDY_ATTRIBUTES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 238, 8), )

    
    STUDY_ATTRIBUTES = property(__STUDY_ATTRIBUTES.value, __STUDY_ATTRIBUTES.set, None, '\n               Properties and attributes of the study.  These can be entered as free-form\n               tag-value pairs. For certain studies, submitters may be asked to follow a\n               community established ontology when describing the work.\n            ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace4_StudyType_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace4_StudyType_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace4_StudyType_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace4_StudyType_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __DESCRIPTOR.name() : __DESCRIPTOR,
        __STUDY_LINKS.name() : __STUDY_LINKS,
        __STUDY_ATTRIBUTES.name() : __STUDY_ATTRIBUTES
    })
    _AttributeMap.update({
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })
Namespace.addCategoryObject('typeBinding', 'StudyType', StudyType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 23, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STUDY_TITLE uses Python identifier STUDY_TITLE
    __STUDY_TITLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_TITLE'), 'STUDY_TITLE', '__AbsentNamespace4_CTD_ANON_STUDY_TITLE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 25, 12), )

    
    STUDY_TITLE = property(__STUDY_TITLE.value, __STUDY_TITLE.set, None, '\n                        Title of the study as would be used in a publication.\n                    ')

    
    # Element STUDY_TYPE uses Python identifier STUDY_TYPE
    __STUDY_TYPE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_TYPE'), 'STUDY_TYPE', '__AbsentNamespace4_CTD_ANON_STUDY_TYPE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 32, 12), )

    
    STUDY_TYPE = property(__STUDY_TYPE.value, __STUDY_TYPE.set, None, 'The STUDY_TYPE presents a controlled vocabulary for expressing the overall purpose of the study.')

    
    # Element STUDY_ABSTRACT uses Python identifier STUDY_ABSTRACT
    __STUDY_ABSTRACT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_ABSTRACT'), 'STUDY_ABSTRACT', '__AbsentNamespace4_CTD_ANON_STUDY_ABSTRACT', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 151, 12), )

    
    STUDY_ABSTRACT = property(__STUDY_ABSTRACT.value, __STUDY_ABSTRACT.set, None, '\n                        Briefly describes the goals, purpose, and scope of the Study.  This need not be listed if it can be\n                        inherited from a referenced publication.\n                    ')

    
    # Element CENTER_NAME uses Python identifier CENTER_NAME
    __CENTER_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CENTER_NAME'), 'CENTER_NAME', '__AbsentNamespace4_CTD_ANON_CENTER_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 159, 12), )

    
    CENTER_NAME = property(__CENTER_NAME.value, __CENTER_NAME.set, None, '\n                        DEPRECATED.  Use STUDY@center_name instead.\n                        Controlled vocabulary identifying the sequencing center, core facility, consortium, or laboratory responsible for the study.\n                    ')

    
    # Element CENTER_PROJECT_NAME uses Python identifier CENTER_PROJECT_NAME
    __CENTER_PROJECT_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CENTER_PROJECT_NAME'), 'CENTER_PROJECT_NAME', '__AbsentNamespace4_CTD_ANON_CENTER_PROJECT_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 167, 12), )

    
    CENTER_PROJECT_NAME = property(__CENTER_PROJECT_NAME.value, __CENTER_PROJECT_NAME.set, None, "\n                        Submitter defined project name.  This field is intended for backward tracking of the study record to the submitter's LIMS.\n                    ")

    
    # Element PROJECT_ID uses Python identifier PROJECT_ID
    __PROJECT_ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PROJECT_ID'), 'PROJECT_ID', '__AbsentNamespace4_CTD_ANON_PROJECT_ID', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 174, 12), )

    
    PROJECT_ID = property(__PROJECT_ID.value, __PROJECT_ID.set, None, '\n                        DEPRECATED (use RELATED_STUDIES.STUDY instead).\n                        The required PROJECT_ID accession is generated by the Genome Project database at NCBI\n                        and will be valid also at the other archival institutions.\n                    ')

    
    # Element RELATED_STUDIES uses Python identifier RELATED_STUDIES
    __RELATED_STUDIES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RELATED_STUDIES'), 'RELATED_STUDIES', '__AbsentNamespace4_CTD_ANON_RELATED_STUDIES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 183, 12), )

    
    RELATED_STUDIES = property(__RELATED_STUDIES.value, __RELATED_STUDIES.set, None, None)

    
    # Element STUDY_DESCRIPTION uses Python identifier STUDY_DESCRIPTION
    __STUDY_DESCRIPTION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_DESCRIPTION'), 'STUDY_DESCRIPTION', '__AbsentNamespace4_CTD_ANON_STUDY_DESCRIPTION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 214, 12), )

    
    STUDY_DESCRIPTION = property(__STUDY_DESCRIPTION.value, __STUDY_DESCRIPTION.set, None, '\n                        More extensive free-form description of the study.\n                    ')

    _ElementMap.update({
        __STUDY_TITLE.name() : __STUDY_TITLE,
        __STUDY_TYPE.name() : __STUDY_TYPE,
        __STUDY_ABSTRACT.name() : __STUDY_ABSTRACT,
        __CENTER_NAME.name() : __CENTER_NAME,
        __CENTER_PROJECT_NAME.name() : __CENTER_PROJECT_NAME,
        __PROJECT_ID.name() : __PROJECT_ID,
        __RELATED_STUDIES.name() : __RELATED_STUDIES,
        __STUDY_DESCRIPTION.name() : __STUDY_DESCRIPTION
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 184, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RELATED_STUDY uses Python identifier RELATED_STUDY
    __RELATED_STUDY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RELATED_STUDY'), 'RELATED_STUDY', '__AbsentNamespace4_CTD_ANON__RELATED_STUDY', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 186, 20), )

    
    RELATED_STUDY = property(__RELATED_STUDY.value, __RELATED_STUDY.set, None, None)

    _ElementMap.update({
        __RELATED_STUDY.name() : __RELATED_STUDY
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 187, 22)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RELATED_LINK uses Python identifier RELATED_LINK
    __RELATED_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RELATED_LINK'), 'RELATED_LINK', '__AbsentNamespace4_CTD_ANON_2_RELATED_LINK', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 189, 26), )

    
    RELATED_LINK = property(__RELATED_LINK.value, __RELATED_LINK.set, None, "\n                                Related study or project record from a list of supported databases.\n                                The study's information is derived from this project record rather\n                                than stored as first class information.\n                              ")

    
    # Element IS_PRIMARY uses Python identifier IS_PRIMARY
    __IS_PRIMARY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IS_PRIMARY'), 'IS_PRIMARY', '__AbsentNamespace4_CTD_ANON_2_IS_PRIMARY', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 198, 26), )

    
    IS_PRIMARY = property(__IS_PRIMARY.value, __IS_PRIMARY.set, None, '\n                                Whether this study object is designated as the primary source\n                                of the study or project information.\n                              ')

    _ElementMap.update({
        __RELATED_LINK.name() : __RELATED_LINK,
        __IS_PRIMARY.name() : __IS_PRIMARY
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """
                  Links to resources related to this study (publication, datasets, online databases).
              """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 231, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STUDY_LINK uses Python identifier STUDY_LINK
    __STUDY_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_LINK'), 'STUDY_LINK', '__AbsentNamespace4_CTD_ANON_3_STUDY_LINK', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 233, 14), )

    
    STUDY_LINK = property(__STUDY_LINK.value, __STUDY_LINK.set, None, None)

    _ElementMap.update({
        __STUDY_LINK.name() : __STUDY_LINK
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """
               Properties and attributes of the study.  These can be entered as free-form
               tag-value pairs. For certain studies, submitters may be asked to follow a
               community established ontology when describing the work.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 246, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STUDY_ATTRIBUTE uses Python identifier STUDY_ATTRIBUTE
    __STUDY_ATTRIBUTE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTE'), 'STUDY_ATTRIBUTE', '__AbsentNamespace4_CTD_ANON_4_STUDY_ATTRIBUTE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 248, 14), )

    
    STUDY_ATTRIBUTE = property(__STUDY_ATTRIBUTE.value, __STUDY_ATTRIBUTE.set, None, None)

    _ElementMap.update({
        __STUDY_ATTRIBUTE.name() : __STUDY_ATTRIBUTE
    })
    _AttributeMap.update({
        
    })



# Complex type StudySetType with content type ELEMENT_ONLY
class StudySetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type StudySetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StudySetType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 258, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STUDY uses Python identifier STUDY
    __STUDY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'STUDY'), 'STUDY', '__AbsentNamespace4_StudySetType_STUDY', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 260, 6), )

    
    STUDY = property(__STUDY.value, __STUDY.set, None, None)

    _ElementMap.update({
        __STUDY.name() : __STUDY
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'StudySetType', StudySetType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """The STUDY_TYPE presents a controlled vocabulary for expressing the overall purpose of the study."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 36, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute existing_study_type uses Python identifier existing_study_type
    __existing_study_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'existing_study_type'), 'existing_study_type', '__AbsentNamespace4_CTD_ANON_5_existing_study_type', STD_ANON, required=True)
    __existing_study_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 37, 14)
    __existing_study_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 37, 14)
    
    existing_study_type = property(__existing_study_type.value, __existing_study_type.set, None, None)

    
    # Attribute new_study_type uses Python identifier new_study_type
    __new_study_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'new_study_type'), 'new_study_type', '__AbsentNamespace4_CTD_ANON_5_new_study_type', pyxb.binding.datatypes.string)
    __new_study_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 142, 16)
    __new_study_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 142, 16)
    
    new_study_type = property(__new_study_type.value, __new_study_type.set, None, '\n                      To propose a new term, select Other and enter a new study type.\n                    ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __existing_study_type.name() : __existing_study_type,
        __new_study_type.name() : __new_study_type
    })



STUDY_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'STUDY_SET'), StudySetType, documentation='\n      An STUDY_SET is a container for a set of studies and a common namespace.\n    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 264, 0))
Namespace.addCategoryObject('elementBinding', STUDY_SET.name().localName(), STUDY_SET)

STUDY = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'STUDY'), StudyType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 273, 0))
Namespace.addCategoryObject('elementBinding', STUDY.name().localName(), STUDY)



StudyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=StudyType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 20, 6)))

StudyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DESCRIPTOR'), CTD_ANON, scope=StudyType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 22, 6)))

StudyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_LINKS'), CTD_ANON_3, scope=StudyType, documentation='\n                  Links to resources related to this study (publication, datasets, online databases).\n              ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 225, 8)))

StudyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTES'), CTD_ANON_4, scope=StudyType, documentation='\n               Properties and attributes of the study.  These can be entered as free-form\n               tag-value pairs. For certain studies, submitters may be asked to follow a\n               community established ontology when describing the work.\n            ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 238, 8)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 20, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 225, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 238, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StudyType._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 20, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StudyType._UseForTag(pyxb.namespace.ExpandedName(None, 'DESCRIPTOR')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 22, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(StudyType._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_LINKS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 225, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(StudyType._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 238, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
StudyType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_TITLE'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                        Title of the study as would be used in a publication.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 25, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_TYPE'), CTD_ANON_5, scope=CTD_ANON, documentation='The STUDY_TYPE presents a controlled vocabulary for expressing the overall purpose of the study.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 32, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_ABSTRACT'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                        Briefly describes the goals, purpose, and scope of the Study.  This need not be listed if it can be\n                        inherited from a referenced publication.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 151, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CENTER_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                        DEPRECATED.  Use STUDY@center_name instead.\n                        Controlled vocabulary identifying the sequencing center, core facility, consortium, or laboratory responsible for the study.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 159, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CENTER_PROJECT_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation="\n                        Submitter defined project name.  This field is intended for backward tracking of the study record to the submitter's LIMS.\n                    ", location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 167, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PROJECT_ID'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON, documentation='\n                        DEPRECATED (use RELATED_STUDIES.STUDY instead).\n                        The required PROJECT_ID accession is generated by the Genome Project database at NCBI\n                        and will be valid also at the other archival institutions.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 174, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RELATED_STUDIES'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 183, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_DESCRIPTION'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                        More extensive free-form description of the study.\n                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 214, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_TITLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 25, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=st_0)

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_TYPE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 32, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=st_0)

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 151, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_ABSTRACT')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 151, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 159, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'CENTER_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 159, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 167, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'CENTER_PROJECT_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 167, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 174, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'PROJECT_ID')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 174, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 183, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'RELATED_STUDIES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 183, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 214, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_DESCRIPTION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 214, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 24, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 151, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 159, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 167, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 174, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 183, 12))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 214, 12))
    counters.add(cc_6)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_2())
    sub_automata.append(_BuildAutomaton_3())
    sub_automata.append(_BuildAutomaton_4())
    sub_automata.append(_BuildAutomaton_5())
    sub_automata.append(_BuildAutomaton_6())
    sub_automata.append(_BuildAutomaton_7())
    sub_automata.append(_BuildAutomaton_8())
    sub_automata.append(_BuildAutomaton_9())
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 24, 10)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RELATED_STUDY'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 186, 20)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'RELATED_STUDY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 186, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_10()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RELATED_LINK'), _ImportedBinding_com.XRefType, scope=CTD_ANON_2, documentation="\n                                Related study or project record from a list of supported databases.\n                                The study's information is derived from this project record rather\n                                than stored as first class information.\n                              ", location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 189, 26)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IS_PRIMARY'), pyxb.binding.datatypes.boolean, scope=CTD_ANON_2, documentation='\n                                Whether this study object is designated as the primary source\n                                of the study or project information.\n                              ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 198, 26)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'RELATED_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 189, 26))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'IS_PRIMARY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 198, 26))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_11()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_LINK'), _ImportedBinding_com.LinkType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 233, 14)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 233, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_12()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTE'), _ImportedBinding_com.AttributeType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 248, 14)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY_ATTRIBUTE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 248, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_13()




StudySetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'STUDY'), StudyType, scope=StudySetType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 260, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StudySetType._UseForTag(pyxb.namespace.ExpandedName(None, 'STUDY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.study.xsd', 260, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
StudySetType._Automaton = _BuildAutomaton_14()

