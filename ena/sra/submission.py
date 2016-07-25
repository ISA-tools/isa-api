# ./binding_4.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2016-07-25 14:27:49.656557 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace AbsentNamespace5

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
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 80, 24)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.study = STD_ANON._CF_enumeration.addEnumeration(unicode_value='study', tag='study')
STD_ANON.experiment = STD_ANON._CF_enumeration.addEnumeration(unicode_value='experiment', tag='experiment')
STD_ANON.sample = STD_ANON._CF_enumeration.addEnumeration(unicode_value='sample', tag='sample')
STD_ANON.run = STD_ANON._CF_enumeration.addEnumeration(unicode_value='run', tag='run')
STD_ANON.analysis = STD_ANON._CF_enumeration.addEnumeration(unicode_value='analysis', tag='analysis')
STD_ANON.dataset = STD_ANON._CF_enumeration.addEnumeration(unicode_value='dataset', tag='dataset')
STD_ANON.policy = STD_ANON._CF_enumeration.addEnumeration(unicode_value='policy', tag='policy')
STD_ANON.dac = STD_ANON._CF_enumeration.addEnumeration(unicode_value='dac', tag='dac')
STD_ANON.project = STD_ANON._CF_enumeration.addEnumeration(unicode_value='project', tag='project')
STD_ANON.checklist = STD_ANON._CF_enumeration.addEnumeration(unicode_value='checklist', tag='checklist')
STD_ANON.sampleGroup = STD_ANON._CF_enumeration.addEnumeration(unicode_value='sampleGroup', tag='sampleGroup')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 112, 24)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_)
STD_ANON_.study = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='study', tag='study')
STD_ANON_.experiment = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='experiment', tag='experiment')
STD_ANON_.sample = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='sample', tag='sample')
STD_ANON_.run = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='run', tag='run')
STD_ANON_.analysis = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='analysis', tag='analysis')
STD_ANON_.dataset = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='dataset', tag='dataset')
STD_ANON_.policy = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='policy', tag='policy')
STD_ANON_.dac = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='dac', tag='dac')
STD_ANON_.project = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='project', tag='project')
STD_ANON_.checklist = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='checklist', tag='checklist')
STD_ANON_.sampleGroup = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='sampleGroup', tag='sampleGroup')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 210, 24)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_2)
STD_ANON_2.study = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='study', tag='study')
STD_ANON_2.experiment = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='experiment', tag='experiment')
STD_ANON_2.sample = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='sample', tag='sample')
STD_ANON_2.run = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='run', tag='run')
STD_ANON_2.analysis = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='analysis', tag='analysis')
STD_ANON_2.dataset = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='dataset', tag='dataset')
STD_ANON_2.policy = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='policy', tag='policy')
STD_ANON_2.dac = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='dac', tag='dac')
STD_ANON_2.project = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='project', tag='project')
STD_ANON_2.checklist = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='checklist', tag='checklist')
STD_ANON_2.sampleGroup = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='sampleGroup', tag='sampleGroup')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Complex type SubmissionType with content type ELEMENT_ONLY
class SubmissionType (pyxb.binding.basis.complexTypeDefinition):
    """
       A Submission type is used to describe an object that contains submission actions to be performed by the archive.
    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubmissionType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 8, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace5_SubmissionType_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 17, 6), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TITLE'), 'TITLE', '__AbsentNamespace5_SubmissionType_TITLE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 18, 6), )

    
    TITLE = property(__TITLE.value, __TITLE.set, None, '\n            Short text that can be used to define submissions in searches or in displays.\n          ')

    
    # Element CONTACTS uses Python identifier CONTACTS
    __CONTACTS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CONTACTS'), 'CONTACTS', '__AbsentNamespace5_SubmissionType_CONTACTS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 25, 6), )

    
    CONTACTS = property(__CONTACTS.value, __CONTACTS.set, None, None)

    
    # Element ACTIONS uses Python identifier ACTIONS
    __ACTIONS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ACTIONS'), 'ACTIONS', '__AbsentNamespace5_SubmissionType_ACTIONS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 57, 6), )

    
    ACTIONS = property(__ACTIONS.value, __ACTIONS.set, None, None)

    
    # Element SUBMISSION_LINKS uses Python identifier SUBMISSION_LINKS
    __SUBMISSION_LINKS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINKS'), 'SUBMISSION_LINKS', '__AbsentNamespace5_SubmissionType_SUBMISSION_LINKS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 235, 6), )

    
    SUBMISSION_LINKS = property(__SUBMISSION_LINKS.value, __SUBMISSION_LINKS.set, None, '\n            Archive created links to associated submissions.\n          ')

    
    # Element SUBMISSION_ATTRIBUTES uses Python identifier SUBMISSION_ATTRIBUTES
    __SUBMISSION_ATTRIBUTES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTES'), 'SUBMISSION_ATTRIBUTES', '__AbsentNamespace5_SubmissionType_SUBMISSION_ATTRIBUTES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 248, 6), )

    
    SUBMISSION_ATTRIBUTES = property(__SUBMISSION_ATTRIBUTES.value, __SUBMISSION_ATTRIBUTES.set, None, '\n            Archive assigned properties and attributes of a SUBMISSION.\n          ')

    
    # Attribute submission_date uses Python identifier submission_date
    __submission_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'submission_date'), 'submission_date', '__AbsentNamespace5_SubmissionType_submission_date', pyxb.binding.datatypes.dateTime)
    __submission_date._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 265, 4)
    __submission_date._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 265, 4)
    
    submission_date = property(__submission_date.value, __submission_date.set, None, '\n          Submitter assigned preparation date of this submission object.\n        ')

    
    # Attribute submission_comment uses Python identifier submission_comment
    __submission_comment = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'submission_comment'), 'submission_comment', '__AbsentNamespace5_SubmissionType_submission_comment', pyxb.binding.datatypes.string)
    __submission_comment._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 272, 4)
    __submission_comment._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 272, 4)
    
    submission_comment = property(__submission_comment.value, __submission_comment.set, None, '\n          Submitter assigned comment.\n        ')

    
    # Attribute lab_name uses Python identifier lab_name
    __lab_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lab_name'), 'lab_name', '__AbsentNamespace5_SubmissionType_lab_name', pyxb.binding.datatypes.string)
    __lab_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 279, 4)
    __lab_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 279, 4)
    
    lab_name = property(__lab_name.value, __lab_name.set, None, '\n          Laboratory name within submitting institution.\n        ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace5_SubmissionType_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace5_SubmissionType_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace5_SubmissionType_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace5_SubmissionType_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __TITLE.name() : __TITLE,
        __CONTACTS.name() : __CONTACTS,
        __ACTIONS.name() : __ACTIONS,
        __SUBMISSION_LINKS.name() : __SUBMISSION_LINKS,
        __SUBMISSION_ATTRIBUTES.name() : __SUBMISSION_ATTRIBUTES
    })
    _AttributeMap.update({
        __submission_date.name() : __submission_date,
        __submission_comment.name() : __submission_comment,
        __lab_name.name() : __lab_name,
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })
Namespace.addCategoryObject('typeBinding', 'SubmissionType', SubmissionType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 26, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CONTACT uses Python identifier CONTACT
    __CONTACT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CONTACT'), 'CONTACT', '__AbsentNamespace5_CTD_ANON_CONTACT', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 28, 12), )

    
    CONTACT = property(__CONTACT.value, __CONTACT.set, None, None)

    _ElementMap.update({
        __CONTACT.name() : __CONTACT
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 29, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace5_CTD_ANON__name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 30, 16)
    __name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 30, 16)
    
    name = property(__name.value, __name.set, None, '\n                      Name of contact person for this submission.\n                    ')

    
    # Attribute inform_on_status uses Python identifier inform_on_status
    __inform_on_status = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'inform_on_status'), 'inform_on_status', '__AbsentNamespace5_CTD_ANON__inform_on_status', pyxb.binding.datatypes.anyURI)
    __inform_on_status._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 37, 16)
    __inform_on_status._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 37, 16)
    
    inform_on_status = property(__inform_on_status.value, __inform_on_status.set, None, '\n                      Internet address of person or service to inform on any status changes for this submission.\n                    ')

    
    # Attribute inform_on_error uses Python identifier inform_on_error
    __inform_on_error = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'inform_on_error'), 'inform_on_error', '__AbsentNamespace5_CTD_ANON__inform_on_error', pyxb.binding.datatypes.anyURI)
    __inform_on_error._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 44, 16)
    __inform_on_error._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 44, 16)
    
    inform_on_error = property(__inform_on_error.value, __inform_on_error.set, None, '\n                      Internet address of person or service to inform on any errors for this submission.\n                    ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __inform_on_status.name() : __inform_on_status,
        __inform_on_error.name() : __inform_on_error
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 58, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ACTION uses Python identifier ACTION
    __ACTION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ACTION'), 'ACTION', '__AbsentNamespace5_CTD_ANON_2_ACTION', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 60, 12), )

    
    ACTION = property(__ACTION.value, __ACTION.set, None, 'Action to be executed by the archive.')

    _ElementMap.update({
        __ACTION.name() : __ACTION
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Action to be executed by the archive."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 64, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ADD uses Python identifier ADD
    __ADD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ADD'), 'ADD', '__AbsentNamespace5_CTD_ANON_3_ADD', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 66, 18), )

    
    ADD = property(__ADD.value, __ADD.set, None, 'Add an object to the archive.')

    
    # Element MODIFY uses Python identifier MODIFY
    __MODIFY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MODIFY'), 'MODIFY', '__AbsentNamespace5_CTD_ANON_3_MODIFY', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 98, 18), )

    
    MODIFY = property(__MODIFY.value, __MODIFY.set, None, 'Modify an object in the archive.')

    
    # Element CANCEL uses Python identifier CANCEL
    __CANCEL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CANCEL'), 'CANCEL', '__AbsentNamespace5_CTD_ANON_3_CANCEL', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 130, 18), )

    
    CANCEL = property(__CANCEL.value, __CANCEL.set, None, 'Cancel an object which has not been made public. Cancelled objects will not be made public.')

    
    # Element SUPPRESS uses Python identifier SUPPRESS
    __SUPPRESS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUPPRESS'), 'SUPPRESS', '__AbsentNamespace5_CTD_ANON_3_SUPPRESS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 142, 18), )

    
    SUPPRESS = property(__SUPPRESS.value, __SUPPRESS.set, None, 'Suppress an object which has been made public. Suppressed data will remain accessible by accession number.')

    
    # Element HOLD uses Python identifier HOLD
    __HOLD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'HOLD'), 'HOLD', '__AbsentNamespace5_CTD_ANON_3_HOLD', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 154, 18), )

    
    HOLD = property(__HOLD.value, __HOLD.set, None, 'Make the object public only when the hold date expires.')

    
    # Element RELEASE uses Python identifier RELEASE
    __RELEASE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RELEASE'), 'RELEASE', '__AbsentNamespace5_CTD_ANON_3_RELEASE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 175, 18), )

    
    RELEASE = property(__RELEASE.value, __RELEASE.set, None, 'The object will be released immediately to public.')

    
    # Element PROTECT uses Python identifier PROTECT
    __PROTECT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PROTECT'), 'PROTECT', '__AbsentNamespace5_CTD_ANON_3_PROTECT', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 191, 18), )

    
    PROTECT = property(__PROTECT.value, __PROTECT.set, None, 'This action is required for data submitted to European Genome-Phenome Archive (EGA). ')

    
    # Element VALIDATE uses Python identifier VALIDATE
    __VALIDATE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VALIDATE'), 'VALIDATE', '__AbsentNamespace5_CTD_ANON_3_VALIDATE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 197, 18), )

    
    VALIDATE = property(__VALIDATE.value, __VALIDATE.set, None, 'Validates the submitted XMLs without actually submitting them.')

    _ElementMap.update({
        __ADD.name() : __ADD,
        __MODIFY.name() : __MODIFY,
        __CANCEL.name() : __CANCEL,
        __SUPPRESS.name() : __SUPPRESS,
        __HOLD.name() : __HOLD,
        __RELEASE.name() : __RELEASE,
        __PROTECT.name() : __PROTECT,
        __VALIDATE.name() : __VALIDATE
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Cancel an object which has not been made public. Cancelled objects will not be made public."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 134, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute target uses Python identifier target
    __target = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'target'), 'target', '__AbsentNamespace5_CTD_ANON_4_target', pyxb.binding.datatypes.string, required=True)
    __target._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 135, 22)
    __target._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 135, 22)
    
    target = property(__target.value, __target.set, None, 'Accession or refname of the object that is being cancelled.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __target.name() : __target
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Suppress an object which has been made public. Suppressed data will remain accessible by accession number."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 146, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute target uses Python identifier target
    __target = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'target'), 'target', '__AbsentNamespace5_CTD_ANON_5_target', pyxb.binding.datatypes.string, required=True)
    __target._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 147, 22)
    __target._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 147, 22)
    
    target = property(__target.value, __target.set, None, 'Accession or refname of the object that is being suppressed.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __target.name() : __target
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Make the object public only when the hold date expires."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 158, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute target uses Python identifier target
    __target = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'target'), 'target', '__AbsentNamespace5_CTD_ANON_6_target', pyxb.binding.datatypes.string)
    __target._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 159, 22)
    __target._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 159, 22)
    
    target = property(__target.value, __target.set, None, '\n                                    Accession or refname of the object that is being made public\n                                    when the hold date expires. If not specified then\n                                    all objects in the submission will be assigned the hold date.\n                          ')

    
    # Attribute HoldUntilDate uses Python identifier HoldUntilDate
    __HoldUntilDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'HoldUntilDate'), 'HoldUntilDate', '__AbsentNamespace5_CTD_ANON_6_HoldUntilDate', pyxb.binding.datatypes.date)
    __HoldUntilDate._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 168, 22)
    __HoldUntilDate._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 168, 22)
    
    HoldUntilDate = property(__HoldUntilDate.value, __HoldUntilDate.set, None, 'The date when the submission will be made public.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __target.name() : __target,
        __HoldUntilDate.name() : __HoldUntilDate
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """The object will be released immediately to public."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 179, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute target uses Python identifier target
    __target = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'target'), 'target', '__AbsentNamespace5_CTD_ANON_7_target', pyxb.binding.datatypes.string)
    __target._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 180, 22)
    __target._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 180, 22)
    
    target = property(__target.value, __target.set, None, '\n                                    Accession or refname of the object that is made public.\n                                    If not specified then all objects in the submission will\n                                    made public.\n                          ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __target.name() : __target
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """This action is required for data submitted to European Genome-Phenome Archive (EGA). """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 195, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """
            Archive created links to associated submissions.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 241, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SUBMISSION_LINK uses Python identifier SUBMISSION_LINK
    __SUBMISSION_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINK'), 'SUBMISSION_LINK', '__AbsentNamespace5_CTD_ANON_9_SUBMISSION_LINK', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 243, 12), )

    
    SUBMISSION_LINK = property(__SUBMISSION_LINK.value, __SUBMISSION_LINK.set, None, None)

    _ElementMap.update({
        __SUBMISSION_LINK.name() : __SUBMISSION_LINK
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """
            Archive assigned properties and attributes of a SUBMISSION.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 254, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SUBMISSION_ATTRIBUTE uses Python identifier SUBMISSION_ATTRIBUTE
    __SUBMISSION_ATTRIBUTE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTE'), 'SUBMISSION_ATTRIBUTE', '__AbsentNamespace5_CTD_ANON_10_SUBMISSION_ATTRIBUTE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 256, 12), )

    
    SUBMISSION_ATTRIBUTE = property(__SUBMISSION_ATTRIBUTE.value, __SUBMISSION_ATTRIBUTE.set, None, None)

    _ElementMap.update({
        __SUBMISSION_ATTRIBUTE.name() : __SUBMISSION_ATTRIBUTE
    })
    _AttributeMap.update({
        
    })



# Complex type SubmissionSetType with content type ELEMENT_ONLY
class SubmissionSetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type SubmissionSetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubmissionSetType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 290, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SUBMISSION uses Python identifier SUBMISSION
    __SUBMISSION = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SUBMISSION'), 'SUBMISSION', '__AbsentNamespace5_SubmissionSetType_SUBMISSION', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 292, 6), )

    
    SUBMISSION = property(__SUBMISSION.value, __SUBMISSION.set, None, None)

    _ElementMap.update({
        __SUBMISSION.name() : __SUBMISSION
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'SubmissionSetType', SubmissionSetType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Add an object to the archive."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 70, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute source uses Python identifier source
    __source = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source'), 'source', '__AbsentNamespace5_CTD_ANON_11_source', pyxb.binding.datatypes.string, required=True)
    __source._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 71, 22)
    __source._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 71, 22)
    
    source = property(__source.value, __source.set, None, 'Filename or relative path to the XML file being submitted.')

    
    # Attribute schema uses Python identifier schema
    __schema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'schema'), 'schema', '__AbsentNamespace5_CTD_ANON_11_schema', STD_ANON, required=True)
    __schema._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 76, 22)
    __schema._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 76, 22)
    
    schema = property(__schema.value, __schema.set, None, 'The type of the XML file being submitted.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __source.name() : __source,
        __schema.name() : __schema
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Modify an object in the archive."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 102, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute source uses Python identifier source
    __source = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source'), 'source', '__AbsentNamespace5_CTD_ANON_12_source', pyxb.binding.datatypes.string, required=True)
    __source._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 103, 22)
    __source._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 103, 22)
    
    source = property(__source.value, __source.set, None, 'Filename or relative path to the XML file being updated.')

    
    # Attribute schema uses Python identifier schema
    __schema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'schema'), 'schema', '__AbsentNamespace5_CTD_ANON_12_schema', STD_ANON_, required=True)
    __schema._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 108, 22)
    __schema._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 108, 22)
    
    schema = property(__schema.value, __schema.set, None, 'The type of the XML file being updated.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __source.name() : __source,
        __schema.name() : __schema
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Validates the submitted XMLs without actually submitting them."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 201, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute source uses Python identifier source
    __source = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source'), 'source', '__AbsentNamespace5_CTD_ANON_13_source', pyxb.binding.datatypes.string, required=True)
    __source._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 202, 22)
    __source._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 202, 22)
    
    source = property(__source.value, __source.set, None, 'Filename or relative path to the XML file being validated.')

    
    # Attribute schema uses Python identifier schema
    __schema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'schema'), 'schema', '__AbsentNamespace5_CTD_ANON_13_schema', STD_ANON_2, required=True)
    __schema._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 207, 22)
    __schema._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 207, 22)
    
    schema = property(__schema.value, __schema.set, None, 'The type of the XML file being validated.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __source.name() : __source,
        __schema.name() : __schema
    })



SUBMISSION_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SUBMISSION_SET'), SubmissionSetType, documentation='\n      An SUBMISSION_SET is a container for a set of studies and a common namespace.\n    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 296, 2))
Namespace.addCategoryObject('elementBinding', SUBMISSION_SET.name().localName(), SUBMISSION_SET)

SUBMISSION = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SUBMISSION'), SubmissionType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 305, 2))
Namespace.addCategoryObject('elementBinding', SUBMISSION.name().localName(), SUBMISSION)



SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=SubmissionType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 17, 6)))

SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TITLE'), pyxb.binding.datatypes.string, scope=SubmissionType, documentation='\n            Short text that can be used to define submissions in searches or in displays.\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 18, 6)))

SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CONTACTS'), CTD_ANON, scope=SubmissionType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 25, 6)))

SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ACTIONS'), CTD_ANON_2, scope=SubmissionType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 57, 6)))

SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINKS'), CTD_ANON_9, scope=SubmissionType, documentation='\n            Archive created links to associated submissions.\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 235, 6)))

SubmissionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTES'), CTD_ANON_10, scope=SubmissionType, documentation='\n            Archive assigned properties and attributes of a SUBMISSION.\n          ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 248, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 17, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 18, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 25, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 57, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 235, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 248, 6))
    counters.add(cc_5)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 17, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'TITLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 18, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'CONTACTS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 25, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'ACTIONS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 57, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINKS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 235, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(SubmissionType._UseForTag(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 248, 6))
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
SubmissionType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CONTACT'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 28, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'CONTACT')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 28, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ACTION'), CTD_ANON_3, scope=CTD_ANON_2, documentation='Action to be executed by the archive.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 60, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'ACTION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 60, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ADD'), CTD_ANON_11, scope=CTD_ANON_3, documentation='Add an object to the archive.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 66, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MODIFY'), CTD_ANON_12, scope=CTD_ANON_3, documentation='Modify an object in the archive.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 98, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CANCEL'), CTD_ANON_4, scope=CTD_ANON_3, documentation='Cancel an object which has not been made public. Cancelled objects will not be made public.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 130, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUPPRESS'), CTD_ANON_5, scope=CTD_ANON_3, documentation='Suppress an object which has been made public. Suppressed data will remain accessible by accession number.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 142, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'HOLD'), CTD_ANON_6, scope=CTD_ANON_3, documentation='Make the object public only when the hold date expires.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 154, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RELEASE'), CTD_ANON_7, scope=CTD_ANON_3, documentation='The object will be released immediately to public.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 175, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PROTECT'), CTD_ANON_8, scope=CTD_ANON_3, documentation='This action is required for data submitted to European Genome-Phenome Archive (EGA). ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 191, 18)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VALIDATE'), CTD_ANON_13, scope=CTD_ANON_3, documentation='Validates the submitted XMLs without actually submitting them.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 197, 18)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'ADD')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 66, 18))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'MODIFY')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 98, 18))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'CANCEL')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 130, 18))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'SUPPRESS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 142, 18))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'HOLD')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 154, 18))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'RELEASE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 175, 18))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'PROTECT')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 191, 18))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'VALIDATE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 197, 18))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions = []
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINK'), _ImportedBinding_com.LinkType, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 243, 12)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'SUBMISSION_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 243, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_4()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTE'), _ImportedBinding_com.AttributeType, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 256, 12)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'SUBMISSION_ATTRIBUTE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 256, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_5()




SubmissionSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SUBMISSION'), SubmissionType, scope=SubmissionSetType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 292, 6)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubmissionSetType._UseForTag(pyxb.namespace.ExpandedName(None, 'SUBMISSION')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.submission.xsd', 292, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SubmissionSetType._Automaton = _BuildAutomaton_6()

