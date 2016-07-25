# ./binding_2.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2016-07-25 14:27:49.655420 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace AbsentNamespace3

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


# Complex type SampleType with content type ELEMENT_ONLY
class SampleType (pyxb.binding.basis.complexTypeDefinition):
    """
        A Sample defines an isolate of sequenceable material upon which
        sequencing experiments can be based.  The Sample object may be a surrogate for taxonomy
        accession or an anonymized individual identifier.  Or, it may fully specify
        provenance and isolation method of the starting material.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SampleType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 7, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace3_SampleType_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 18, 6), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TITLE'), 'TITLE', '__AbsentNamespace3_SampleType_TITLE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 20, 6), )

    
    TITLE = property(__TITLE.value, __TITLE.set, None, '\n           Short text that can be used to call out sample records in search results or in displays.\n         ')

    
    # Element SAMPLE_NAME uses Python identifier SAMPLE_NAME
    __SAMPLE_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_NAME'), 'SAMPLE_NAME', '__AbsentNamespace3_SampleType_SAMPLE_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 27, 6), )

    
    SAMPLE_NAME = property(__SAMPLE_NAME.value, __SAMPLE_NAME.set, None, None)

    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DESCRIPTION'), 'DESCRIPTION', '__AbsentNamespace3_SampleType_DESCRIPTION', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 73, 6), )

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, '\n            Free-form text describing the sample, its origin, and its method of isolation.\n          ')

    
    # Element SAMPLE_LINKS uses Python identifier SAMPLE_LINKS
    __SAMPLE_LINKS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINKS'), 'SAMPLE_LINKS', '__AbsentNamespace3_SampleType_SAMPLE_LINKS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 82, 6), )

    
    SAMPLE_LINKS = property(__SAMPLE_LINKS.value, __SAMPLE_LINKS.set, None, '\n            Links to resources related to this sample or sample set (publication, datasets, online databases).\n          ')

    
    # Element SAMPLE_ATTRIBUTES uses Python identifier SAMPLE_ATTRIBUTES
    __SAMPLE_ATTRIBUTES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTES'), 'SAMPLE_ATTRIBUTES', '__AbsentNamespace3_SampleType_SAMPLE_ATTRIBUTES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 95, 6), )

    
    SAMPLE_ATTRIBUTES = property(__SAMPLE_ATTRIBUTES.value, __SAMPLE_ATTRIBUTES.set, None, '\n            Properties and attributes of a sample.  These can be entered as free-form \n            tag-value pairs. For certain studies, submitters may be asked to follow a\n            community established ontology when describing the work.\n          ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace3_SampleType_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace3_SampleType_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace3_SampleType_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace3_SampleType_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __TITLE.name() : __TITLE,
        __SAMPLE_NAME.name() : __SAMPLE_NAME,
        __DESCRIPTION.name() : __DESCRIPTION,
        __SAMPLE_LINKS.name() : __SAMPLE_LINKS,
        __SAMPLE_ATTRIBUTES.name() : __SAMPLE_ATTRIBUTES
    })
    _AttributeMap.update({
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })
Namespace.addCategoryObject('typeBinding', 'SampleType', SampleType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 28, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TAXON_ID uses Python identifier TAXON_ID
    __TAXON_ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TAXON_ID'), 'TAXON_ID', '__AbsentNamespace3_CTD_ANON_TAXON_ID', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 30, 12), )

    
    TAXON_ID = property(__TAXON_ID.value, __TAXON_ID.set, None, '\n                  NCBI Taxonomy Identifier.  This is appropriate for individual organisms and\n                  some environmental samples.\n                ')

    
    # Element SCIENTIFIC_NAME uses Python identifier SCIENTIFIC_NAME
    __SCIENTIFIC_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SCIENTIFIC_NAME'), 'SCIENTIFIC_NAME', '__AbsentNamespace3_CTD_ANON_SCIENTIFIC_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 38, 12), )

    
    SCIENTIFIC_NAME = property(__SCIENTIFIC_NAME.value, __SCIENTIFIC_NAME.set, None, '\n                  Scientific name of sample that distinguishes its taxonomy.  Please use a \n                  name or synonym that is tracked in the INSDC Taxonomy database. \n                  Also, this field can be used to confirm the TAXON_ID setting.\n                ')

    
    # Element COMMON_NAME uses Python identifier COMMON_NAME
    __COMMON_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'COMMON_NAME'), 'COMMON_NAME', '__AbsentNamespace3_CTD_ANON_COMMON_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 47, 12), )

    
    COMMON_NAME = property(__COMMON_NAME.value, __COMMON_NAME.set, None, '\n                  GenBank common name of the organism.  Examples: human, mouse.\n                ')

    
    # Element ANONYMIZED_NAME uses Python identifier ANONYMIZED_NAME
    __ANONYMIZED_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ANONYMIZED_NAME'), 'ANONYMIZED_NAME', '__AbsentNamespace3_CTD_ANON_ANONYMIZED_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 54, 12), )

    
    ANONYMIZED_NAME = property(__ANONYMIZED_NAME.value, __ANONYMIZED_NAME.set, None, '\n                  Anonymous public name of the sample.   For example, HapMap human isolate NA12878.\n                ')

    
    # Element INDIVIDUAL_NAME uses Python identifier INDIVIDUAL_NAME
    __INDIVIDUAL_NAME = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'INDIVIDUAL_NAME'), 'INDIVIDUAL_NAME', '__AbsentNamespace3_CTD_ANON_INDIVIDUAL_NAME', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 61, 12), )

    
    INDIVIDUAL_NAME = property(__INDIVIDUAL_NAME.value, __INDIVIDUAL_NAME.set, None, '\n                  Individual name of the sample.  This field can be used to identify the individual identity of\n                  a sample where appropriate (this is usually NOT appropriate for human subjects).  Example:\n                  "Glennie" the platypus.  \n                ')

    _ElementMap.update({
        __TAXON_ID.name() : __TAXON_ID,
        __SCIENTIFIC_NAME.name() : __SCIENTIFIC_NAME,
        __COMMON_NAME.name() : __COMMON_NAME,
        __ANONYMIZED_NAME.name() : __ANONYMIZED_NAME,
        __INDIVIDUAL_NAME.name() : __INDIVIDUAL_NAME
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """
            Links to resources related to this sample or sample set (publication, datasets, online databases).
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 88, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SAMPLE_LINK uses Python identifier SAMPLE_LINK
    __SAMPLE_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINK'), 'SAMPLE_LINK', '__AbsentNamespace3_CTD_ANON__SAMPLE_LINK', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 90, 12), )

    
    SAMPLE_LINK = property(__SAMPLE_LINK.value, __SAMPLE_LINK.set, None, None)

    _ElementMap.update({
        __SAMPLE_LINK.name() : __SAMPLE_LINK
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """
            Properties and attributes of a sample.  These can be entered as free-form 
            tag-value pairs. For certain studies, submitters may be asked to follow a
            community established ontology when describing the work.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 103, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SAMPLE_ATTRIBUTE uses Python identifier SAMPLE_ATTRIBUTE
    __SAMPLE_ATTRIBUTE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTE'), 'SAMPLE_ATTRIBUTE', '__AbsentNamespace3_CTD_ANON_2_SAMPLE_ATTRIBUTE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 105, 12), )

    
    SAMPLE_ATTRIBUTE = property(__SAMPLE_ATTRIBUTE.value, __SAMPLE_ATTRIBUTE.set, None, None)

    _ElementMap.update({
        __SAMPLE_ATTRIBUTE.name() : __SAMPLE_ATTRIBUTE
    })
    _AttributeMap.update({
        
    })



# Complex type SampleSetType with content type ELEMENT_ONLY
class SampleSetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type SampleSetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SampleSetType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 114, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SAMPLE uses Python identifier SAMPLE
    __SAMPLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SAMPLE'), 'SAMPLE', '__AbsentNamespace3_SampleSetType_SAMPLE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 116, 6), )

    
    SAMPLE = property(__SAMPLE.value, __SAMPLE.set, None, None)

    _ElementMap.update({
        __SAMPLE.name() : __SAMPLE
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'SampleSetType', SampleSetType)


SAMPLE_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SAMPLE_SET'), SampleSetType, documentation='\n        SAMPLE_SET serves as a container for a set of samples and a name space\n        for establishing referential integrity between them. \n      ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 120, 2))
Namespace.addCategoryObject('elementBinding', SAMPLE_SET.name().localName(), SAMPLE_SET)

SAMPLE = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SAMPLE'), SampleType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 130, 2))
Namespace.addCategoryObject('elementBinding', SAMPLE.name().localName(), SAMPLE)



SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=SampleType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 18, 6)))

SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TITLE'), pyxb.binding.datatypes.string, scope=SampleType, documentation='\n           Short text that can be used to call out sample records in search results or in displays.\n         ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 20, 6)))

SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_NAME'), CTD_ANON, scope=SampleType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 27, 6)))

SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DESCRIPTION'), pyxb.binding.datatypes.string, scope=SampleType, documentation='\n            Free-form text describing the sample, its origin, and its method of isolation.\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 73, 6)))

SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINKS'), CTD_ANON_, scope=SampleType, documentation='\n            Links to resources related to this sample or sample set (publication, datasets, online databases).\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 82, 6)))

SampleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTES'), CTD_ANON_2, scope=SampleType, documentation='\n            Properties and attributes of a sample.  These can be entered as free-form \n            tag-value pairs. For certain studies, submitters may be asked to follow a\n            community established ontology when describing the work.\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 95, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 18, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 20, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 73, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 82, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 95, 6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 18, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'TITLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 20, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 27, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'DESCRIPTION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 73, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINKS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 82, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(SampleType._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 95, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SampleType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TAXON_ID'), pyxb.binding.datatypes.int, scope=CTD_ANON, documentation='\n                  NCBI Taxonomy Identifier.  This is appropriate for individual organisms and\n                  some environmental samples.\n                ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 30, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SCIENTIFIC_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                  Scientific name of sample that distinguishes its taxonomy.  Please use a \n                  name or synonym that is tracked in the INSDC Taxonomy database. \n                  Also, this field can be used to confirm the TAXON_ID setting.\n                ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 38, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'COMMON_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                  GenBank common name of the organism.  Examples: human, mouse.\n                ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 47, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ANONYMIZED_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                  Anonymous public name of the sample.   For example, HapMap human isolate NA12878.\n                ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 54, 12)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'INDIVIDUAL_NAME'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation='\n                  Individual name of the sample.  This field can be used to identify the individual identity of\n                  a sample where appropriate (this is usually NOT appropriate for human subjects).  Example:\n                  "Glennie" the platypus.  \n                ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 61, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'TAXON_ID')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 30, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 38, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'SCIENTIFIC_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 38, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 47, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'COMMON_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 47, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 54, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'ANONYMIZED_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 54, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 61, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'INDIVIDUAL_NAME')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 61, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 38, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 47, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 54, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 61, 12))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_2())
    sub_automata.append(_BuildAutomaton_3())
    sub_automata.append(_BuildAutomaton_4())
    sub_automata.append(_BuildAutomaton_5())
    sub_automata.append(_BuildAutomaton_6())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 29, 10)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINK'), _ImportedBinding_com.LinkType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 90, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 90, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_7()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTE'), _ImportedBinding_com.AttributeType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 105, 12)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE_ATTRIBUTE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 105, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_8()




SampleSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SAMPLE'), SampleType, scope=SampleSetType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 116, 6)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SampleSetType._UseForTag(pyxb.namespace.ExpandedName(None, 'SAMPLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.sample.xsd', 116, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SampleSetType._Automaton = _BuildAutomaton_9()

