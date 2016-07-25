# ./binding_.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2016-07-25 14:27:49.656111 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace AbsentNamespace2

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
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 90, 50)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.sra = STD_ANON._CF_enumeration.addEnumeration(unicode_value='sra', tag='sra')
STD_ANON.srf = STD_ANON._CF_enumeration.addEnumeration(unicode_value='srf', tag='srf')
STD_ANON.sff = STD_ANON._CF_enumeration.addEnumeration(unicode_value='sff', tag='sff')
STD_ANON.fastq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='fastq', tag='fastq')
STD_ANON.fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='fasta', tag='fasta')
STD_ANON.tab = STD_ANON._CF_enumeration.addEnumeration(unicode_value='tab', tag='tab')
STD_ANON.n454_native = STD_ANON._CF_enumeration.addEnumeration(unicode_value='454_native', tag='n454_native')
STD_ANON.n454_native_seq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='454_native_seq', tag='n454_native_seq')
STD_ANON.n454_native_qual = STD_ANON._CF_enumeration.addEnumeration(unicode_value='454_native_qual', tag='n454_native_qual')
STD_ANON.Helicos_native = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Helicos_native', tag='Helicos_native')
STD_ANON.Illumina_native = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native', tag='Illumina_native')
STD_ANON.Illumina_native_seq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native_seq', tag='Illumina_native_seq')
STD_ANON.Illumina_native_prb = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native_prb', tag='Illumina_native_prb')
STD_ANON.Illumina_native_int = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native_int', tag='Illumina_native_int')
STD_ANON.Illumina_native_qseq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native_qseq', tag='Illumina_native_qseq')
STD_ANON.Illumina_native_scarf = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Illumina_native_scarf', tag='Illumina_native_scarf')
STD_ANON.SOLiD_native = STD_ANON._CF_enumeration.addEnumeration(unicode_value='SOLiD_native', tag='SOLiD_native')
STD_ANON.SOLiD_native_csfasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value='SOLiD_native_csfasta', tag='SOLiD_native_csfasta')
STD_ANON.SOLiD_native_qual = STD_ANON._CF_enumeration.addEnumeration(unicode_value='SOLiD_native_qual', tag='SOLiD_native_qual')
STD_ANON.PacBio_HDF5 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='PacBio_HDF5', tag='PacBio_HDF5')
STD_ANON.bam = STD_ANON._CF_enumeration.addEnumeration(unicode_value='bam', tag='bam')
STD_ANON.cram = STD_ANON._CF_enumeration.addEnumeration(unicode_value='cram', tag='cram')
STD_ANON.CompleteGenomics_native = STD_ANON._CF_enumeration.addEnumeration(unicode_value='CompleteGenomics_native', tag='CompleteGenomics_native')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 313, 50)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_)
STD_ANON_.phred = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='phred', tag='phred')
STD_ANON_.log_odds = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='log-odds', tag='log_odds')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 343, 50)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_2)
STD_ANON_2.ascii = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='ascii', tag='ascii')
STD_ANON_2.decimal = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='decimal', tag='decimal')
STD_ANON_2.hexadecimal = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='hexadecimal', tag='hexadecimal')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 375, 50)
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_3)
STD_ANON_3.emptyString = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='!', tag='emptyString')
STD_ANON_3.emptyString_ = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='@', tag='emptyString_')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 401, 50)
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_4)
STD_ANON_4.MD5 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='MD5', tag='MD5')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Complex type RunType with content type ELEMENT_ONLY
class RunType (pyxb.binding.basis.complexTypeDefinition):
    """
                A run contains a group of reads generated for a particular experiment.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RunType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 7, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace2_RunType_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 15, 12), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TITLE'), 'TITLE', '__AbsentNamespace2_RunType_TITLE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 16, 12), )

    
    TITLE = property(__TITLE.value, __TITLE.set, None, '\n                        Short text that can be used to define submissions in searches or in displays.\n                   ')

    
    # Element EXPERIMENT_REF uses Python identifier EXPERIMENT_REF
    __EXPERIMENT_REF = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF'), 'EXPERIMENT_REF', '__AbsentNamespace2_RunType_EXPERIMENT_REF', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 23, 12), )

    
    EXPERIMENT_REF = property(__EXPERIMENT_REF.value, __EXPERIMENT_REF.set, None, ' The EXPERIMENT_REF identifies the parent experiment.\n                        Experiment describes nucleic acid prepararation from biological sample,\n                        molecular strategies and selections used in preparation of libraries for\n                        sequencing.\n                   ')

    
    # Element SPOT_DESCRIPTOR uses Python identifier SPOT_DESCRIPTOR
    __SPOT_DESCRIPTOR = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SPOT_DESCRIPTOR'), 'SPOT_DESCRIPTOR', '__AbsentNamespace2_RunType_SPOT_DESCRIPTOR', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 39, 12), )

    
    SPOT_DESCRIPTOR = property(__SPOT_DESCRIPTOR.value, __SPOT_DESCRIPTOR.set, None, None)

    
    # Element PLATFORM uses Python identifier PLATFORM
    __PLATFORM = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PLATFORM'), 'PLATFORM', '__AbsentNamespace2_RunType_PLATFORM', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 41, 12), )

    
    PLATFORM = property(__PLATFORM.value, __PLATFORM.set, None, None)

    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PROCESSING'), 'PROCESSING', '__AbsentNamespace2_RunType_PROCESSING', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 43, 12), )

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, None)

    
    # Element RUN_TYPE uses Python identifier RUN_TYPE
    __RUN_TYPE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_TYPE'), 'RUN_TYPE', '__AbsentNamespace2_RunType_RUN_TYPE', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 45, 11), )

    
    RUN_TYPE = property(__RUN_TYPE.value, __RUN_TYPE.set, None, 'The type of the run. ')

    
    # Element DATA_BLOCK uses Python identifier DATA_BLOCK
    __DATA_BLOCK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DATA_BLOCK'), 'DATA_BLOCK', '__AbsentNamespace2_RunType_DATA_BLOCK', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 58, 16), )

    
    DATA_BLOCK = property(__DATA_BLOCK.value, __DATA_BLOCK.set, None, None)

    
    # Element RUN_LINKS uses Python identifier RUN_LINKS
    __RUN_LINKS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_LINKS'), 'RUN_LINKS', '__AbsentNamespace2_RunType_RUN_LINKS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 445, 12), )

    
    RUN_LINKS = property(__RUN_LINKS.value, __RUN_LINKS.set, None, '\n                            Links to resources related to this RUN or RUN set (publication, datasets, online databases).\n                        ')

    
    # Element RUN_ATTRIBUTES uses Python identifier RUN_ATTRIBUTES
    __RUN_ATTRIBUTES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTES'), 'RUN_ATTRIBUTES', '__AbsentNamespace2_RunType_RUN_ATTRIBUTES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 458, 12), )

    
    RUN_ATTRIBUTES = property(__RUN_ATTRIBUTES.value, __RUN_ATTRIBUTES.set, None, '\n                            Properties and attributes of a RUN.  These can be entered as free-form\n                            tag-value pairs. For certain studies, submitters may be asked to follow a\n                            community established ontology when describing the work.\n                        ')

    
    # Attribute run_date uses Python identifier run_date
    __run_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'run_date'), 'run_date', '__AbsentNamespace2_RunType_run_date', pyxb.binding.datatypes.dateTime)
    __run_date._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 476, 8)
    __run_date._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 476, 8)
    
    run_date = property(__run_date.value, __run_date.set, None, '\n                        ISO date when the run took place.\n                    ')

    
    # Attribute run_center uses Python identifier run_center
    __run_center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'run_center'), 'run_center', '__AbsentNamespace2_RunType_run_center', pyxb.binding.datatypes.string)
    __run_center._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 483, 8)
    __run_center._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 483, 8)
    
    run_center = property(__run_center.value, __run_center.set, None, '\n                        If applicable, the name of the contract sequencing center that executed the run.\n                        Example: 454MSC.\n                    ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__AbsentNamespace2_RunType_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    __alias._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 7, 8)
    
    alias = property(__alias.value, __alias.set, None, '\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'center_name'), 'center_name', '__AbsentNamespace2_RunType_center_name', pyxb.binding.datatypes.string)
    __center_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    __center_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 16, 8)
    
    center_name = property(__center_name.value, __center_name.set, None, '\n                    Owner authority of this document and namespace for submitter\'s name of this document.\n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'broker_name'), 'broker_name', '__AbsentNamespace2_RunType_broker_name', pyxb.binding.datatypes.string)
    __broker_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    __broker_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 25, 8)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, '\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace2_RunType_accession', pyxb.binding.datatypes.string)
    __accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    __accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 32, 8)
    
    accession = property(__accession.value, __accession.set, None, "\n                    The document's accession as assigned by the Home Archive.\n                ")

    _ElementMap.update({
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __TITLE.name() : __TITLE,
        __EXPERIMENT_REF.name() : __EXPERIMENT_REF,
        __SPOT_DESCRIPTOR.name() : __SPOT_DESCRIPTOR,
        __PLATFORM.name() : __PLATFORM,
        __PROCESSING.name() : __PROCESSING,
        __RUN_TYPE.name() : __RUN_TYPE,
        __DATA_BLOCK.name() : __DATA_BLOCK,
        __RUN_LINKS.name() : __RUN_LINKS,
        __RUN_ATTRIBUTES.name() : __RUN_ATTRIBUTES
    })
    _AttributeMap.update({
        __run_date.name() : __run_date,
        __run_center.name() : __run_center,
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession
    })
Namespace.addCategoryObject('typeBinding', 'RunType', RunType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """ The EXPERIMENT_REF identifies the parent experiment.
                        Experiment describes nucleic acid prepararation from biological sample,
                        molecular strategies and selections used in preparation of libraries for
                        sequencing.
                   """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 31, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace2_CTD_ANON_IDENTIFIERS', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 33, 24), )

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, None)

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refname'), 'refname', '__AbsentNamespace2_CTD_ANON_refname', pyxb.binding.datatypes.string)
    __refname._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    __refname._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 42, 8)
    
    refname = property(__refname.value, __refname.set, None, '\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refcenter'), 'refcenter', '__AbsentNamespace2_CTD_ANON_refcenter', pyxb.binding.datatypes.string)
    __refcenter._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    __refcenter._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.common.xsd', 50, 8)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, '\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accession'), 'accession', '__AbsentNamespace2_CTD_ANON_accession', pyxb.binding.datatypes.string)
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
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """The type of the run. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 49, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element REFERENCE_ALIGNMENT uses Python identifier REFERENCE_ALIGNMENT
    __REFERENCE_ALIGNMENT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT'), 'REFERENCE_ALIGNMENT', '__AbsentNamespace2_CTD_ANON__REFERENCE_ALIGNMENT', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 51, 24), )

    
    REFERENCE_ALIGNMENT = property(__REFERENCE_ALIGNMENT.value, __REFERENCE_ALIGNMENT.set, None, None)

    _ElementMap.update({
        __REFERENCE_ALIGNMENT.name() : __REFERENCE_ALIGNMENT
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
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 59, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILES uses Python identifier FILES
    __FILES = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FILES'), 'FILES', '__AbsentNamespace2_CTD_ANON_2_FILES', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 62, 28), )

    
    FILES = property(__FILES.value, __FILES.set, None, ' Data files associated with the run.')

    
    # Attribute member_name uses Python identifier member_name
    __member_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'member_name'), 'member_name', '__AbsentNamespace2_CTD_ANON_2_member_name', pyxb.binding.datatypes.string)
    __member_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 435, 24)
    __member_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 435, 24)
    
    member_name = property(__member_name.value, __member_name.set, None, '\n                                        Allow for an individual DATA_BLOCK to be associated with a member of a sample pool.\n                                    ')

    _ElementMap.update({
        __FILES.name() : __FILES
    })
    _AttributeMap.update({
        __member_name.name() : __member_name
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """ Data files associated with the run."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 66, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILE uses Python identifier FILE
    __FILE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FILE'), 'FILE', '__AbsentNamespace2_CTD_ANON_3_FILE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 68, 40), )

    
    FILE = property(__FILE.value, __FILE.set, None, None)

    _ElementMap.update({
        __FILE.name() : __FILE
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """
                            Links to resources related to this RUN or RUN set (publication, datasets, online databases).
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 451, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN_LINK uses Python identifier RUN_LINK
    __RUN_LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_LINK'), 'RUN_LINK', '__AbsentNamespace2_CTD_ANON_4_RUN_LINK', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 453, 24), )

    
    RUN_LINK = property(__RUN_LINK.value, __RUN_LINK.set, None, None)

    _ElementMap.update({
        __RUN_LINK.name() : __RUN_LINK
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """
                            Properties and attributes of a RUN.  These can be entered as free-form
                            tag-value pairs. For certain studies, submitters may be asked to follow a
                            community established ontology when describing the work.
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 466, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN_ATTRIBUTE uses Python identifier RUN_ATTRIBUTE
    __RUN_ATTRIBUTE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTE'), 'RUN_ATTRIBUTE', '__AbsentNamespace2_CTD_ANON_5_RUN_ATTRIBUTE', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 468, 24), )

    
    RUN_ATTRIBUTE = property(__RUN_ATTRIBUTE.value, __RUN_ATTRIBUTE.set, None, None)

    _ElementMap.update({
        __RUN_ATTRIBUTE.name() : __RUN_ATTRIBUTE
    })
    _AttributeMap.update({
        
    })



# Complex type RunSetType with content type ELEMENT_ONLY
class RunSetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type RunSetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RunSetType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 493, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN uses Python identifier RUN
    __RUN = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RUN'), 'RUN', '__AbsentNamespace2_RunSetType_RUN', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 495, 12), )

    
    RUN = property(__RUN.value, __RUN.set, None, None)

    _ElementMap.update({
        __RUN.name() : __RUN
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'RunSetType', RunSetType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 69, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'READ_LABEL'), 'READ_LABEL', '__AbsentNamespace2_CTD_ANON_6_READ_LABEL', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 71, 50), )

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, '\n                                                        The READ_LABEL can associate a certain file to a certain read_label defined in the SPOT_DESCRIPTOR.\n                                                    ')

    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'filename'), 'filename', '__AbsentNamespace2_CTD_ANON_6_filename', pyxb.binding.datatypes.string, required=True)
    __filename._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 80, 48)
    __filename._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 80, 48)
    
    filename = property(__filename.value, __filename.set, None, 'The name or relative pathname of a run data file.')

    
    # Attribute filetype uses Python identifier filetype
    __filetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'filetype'), 'filetype', '__AbsentNamespace2_CTD_ANON_6_filetype', STD_ANON, required=True)
    __filetype._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 86, 48)
    __filetype._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 86, 48)
    
    filetype = property(__filetype.value, __filetype.set, None, ' The run data file model.')

    
    # Attribute quality_scoring_system uses Python identifier quality_scoring_system
    __quality_scoring_system = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quality_scoring_system'), 'quality_scoring_system', '__AbsentNamespace2_CTD_ANON_6_quality_scoring_system', STD_ANON_)
    __quality_scoring_system._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 306, 48)
    __quality_scoring_system._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 306, 48)
    
    quality_scoring_system = property(__quality_scoring_system.value, __quality_scoring_system.set, None, '\n                                                    How the input data are scored for quality.\n                                                ')

    
    # Attribute quality_encoding uses Python identifier quality_encoding
    __quality_encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quality_encoding'), 'quality_encoding', '__AbsentNamespace2_CTD_ANON_6_quality_encoding', STD_ANON_2)
    __quality_encoding._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 336, 48)
    __quality_encoding._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 336, 48)
    
    quality_encoding = property(__quality_encoding.value, __quality_encoding.set, None, '\n                                                    Character used in representing the minimum quality value.\n                                                    Helps specify how to decode text rendering of quality data.\n                                                ')

    
    # Attribute ascii_offset uses Python identifier ascii_offset
    __ascii_offset = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ascii_offset'), 'ascii_offset', '__AbsentNamespace2_CTD_ANON_6_ascii_offset', STD_ANON_3)
    __ascii_offset._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 369, 48)
    __ascii_offset._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 369, 48)
    
    ascii_offset = property(__ascii_offset.value, __ascii_offset.set, None, '\n                                                    Character used in representing the minimum quality value.  Helps specify how to decode text rendering of quality data.\n                                                ')

    
    # Attribute checksum_method uses Python identifier checksum_method
    __checksum_method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'checksum_method'), 'checksum_method', '__AbsentNamespace2_CTD_ANON_6_checksum_method', STD_ANON_4, required=True)
    __checksum_method._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 395, 48)
    __checksum_method._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 395, 48)
    
    checksum_method = property(__checksum_method.value, __checksum_method.set, None, '\n                                                    Checksum method used.\n                                                ')

    
    # Attribute checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'checksum'), 'checksum', '__AbsentNamespace2_CTD_ANON_6_checksum', pyxb.binding.datatypes.string, required=True)
    __checksum._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 413, 48)
    __checksum._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 413, 48)
    
    checksum = property(__checksum.value, __checksum.set, None, '\n                                                    Checksum of uncompressed file.\n                                                ')

    
    # Attribute unencrypted_checksum uses Python identifier unencrypted_checksum
    __unencrypted_checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unencrypted_checksum'), 'unencrypted_checksum', '__AbsentNamespace2_CTD_ANON_6_unencrypted_checksum', pyxb.binding.datatypes.string)
    __unencrypted_checksum._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 421, 48)
    __unencrypted_checksum._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 421, 48)
    
    unencrypted_checksum = property(__unencrypted_checksum.value, __unencrypted_checksum.set, None, '\n                                                            Checksum of unenrypted file(used in conjunction with checksum of encrypted file).\n                                                        ')

    _ElementMap.update({
        __READ_LABEL.name() : __READ_LABEL
    })
    _AttributeMap.update({
        __filename.name() : __filename,
        __filetype.name() : __filetype,
        __quality_scoring_system.name() : __quality_scoring_system,
        __quality_encoding.name() : __quality_encoding,
        __ascii_offset.name() : __ascii_offset,
        __checksum_method.name() : __checksum_method,
        __checksum.name() : __checksum,
        __unencrypted_checksum.name() : __unencrypted_checksum
    })



RUN_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RUN_SET'), RunSetType, documentation='\n                RUN_SET serves as a container for a set of runs and a name space\n                for establishing referential integrity between them.\n            ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 499, 4))
Namespace.addCategoryObject('elementBinding', RUN_SET.name().localName(), RUN_SET)

RUN = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RUN'), RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 509, 4))
Namespace.addCategoryObject('elementBinding', RUN.name().localName(), RUN)



RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 15, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TITLE'), pyxb.binding.datatypes.string, scope=RunType, documentation='\n                        Short text that can be used to define submissions in searches or in displays.\n                   ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 16, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF'), CTD_ANON, scope=RunType, documentation=' The EXPERIMENT_REF identifies the parent experiment.\n                        Experiment describes nucleic acid prepararation from biological sample,\n                        molecular strategies and selections used in preparation of libraries for\n                        sequencing.\n                   ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 23, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SPOT_DESCRIPTOR'), _ImportedBinding_com.SpotDescriptorType, scope=RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 39, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PLATFORM'), _ImportedBinding_com.PlatformType, scope=RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 41, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PROCESSING'), _ImportedBinding_com.ProcessingType, scope=RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 43, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_TYPE'), CTD_ANON_, scope=RunType, documentation='The type of the run. ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 45, 11)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DATA_BLOCK'), CTD_ANON_2, scope=RunType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 58, 16)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_LINKS'), CTD_ANON_4, scope=RunType, documentation='\n                            Links to resources related to this RUN or RUN set (publication, datasets, online databases).\n                        ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 445, 12)))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTES'), CTD_ANON_5, scope=RunType, documentation='\n                            Properties and attributes of a RUN.  These can be entered as free-form\n                            tag-value pairs. For certain studies, submitters may be asked to follow a\n                            community established ontology when describing the work.\n                        ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 458, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 15, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 16, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 39, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 41, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 43, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 45, 11))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 58, 16))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 445, 12))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 458, 12))
    counters.add(cc_8)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 15, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'TITLE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 16, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'EXPERIMENT_REF')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 23, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'SPOT_DESCRIPTOR')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 39, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'PLATFORM')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 41, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'PROCESSING')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 43, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_TYPE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 45, 11))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'DATA_BLOCK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 58, 16))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_LINKS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 445, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(RunType._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 458, 12))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RunType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS'), _ImportedBinding_com.IdentifierType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 33, 24)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 33, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'IDENTIFIERS')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 33, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT'), _ImportedBinding_com.ReferenceSequenceType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 51, 24)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'REFERENCE_ALIGNMENT')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 51, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_2()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FILES'), CTD_ANON_3, scope=CTD_ANON_2, documentation=' Data files associated with the run.', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 62, 28)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'FILES')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 62, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_3()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FILE'), CTD_ANON_6, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 68, 40)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'FILE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 68, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_4()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_LINK'), _ImportedBinding_com.LinkType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 453, 24)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_LINK')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 453, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_5()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTE'), _ImportedBinding_com.AttributeType, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 468, 24)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN_ATTRIBUTE')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 468, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_6()




RunSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RUN'), RunType, scope=RunSetType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 495, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RunSetType._UseForTag(pyxb.namespace.ExpandedName(None, 'RUN')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 495, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RunSetType._Automaton = _BuildAutomaton_7()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'READ_LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, documentation='\n                                                        The READ_LABEL can associate a certain file to a certain read_label defined in the SPOT_DESCRIPTOR.\n                                                    ', location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 71, 50)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 71, 50))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'READ_LABEL')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/res/sra1.5/SRA.run.xsd', 71, 50))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_8()

