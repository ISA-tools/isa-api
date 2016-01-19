# ./tabconfig.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96d8d03236bd7376673f67788ab6b46d9b372f75
# Generated 2016-01-19 16:35:25.134581 by PyXB version 1.2.4 using Python 3.5.0.final.0
# Namespace http://www.ebi.ac.uk/bii/isatab_configuration#

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a3cbf3b8-beca-11e5-8158-acbc328c3881')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ebi.ac.uk/bii/isatab_configuration#', create_if_missing=True)
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


# Atomic simple type: {http://www.ebi.ac.uk/bii/isatab_configuration#}RangeType
class RangeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RangeType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 125, 4)
    _Documentation = None
RangeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=RangeType, enum_prefix=None)
RangeType.less_than = RangeType._CF_enumeration.addEnumeration(unicode_value='less-than', tag='less_than')
RangeType.less_equal_than = RangeType._CF_enumeration.addEnumeration(unicode_value='less-equal-than', tag='less_equal_than')
RangeType.greater_than = RangeType._CF_enumeration.addEnumeration(unicode_value='greater-than', tag='greater_than')
RangeType.greater_equal_than = RangeType._CF_enumeration.addEnumeration(unicode_value='greater-equal-than', tag='greater_equal_than')
RangeType.between = RangeType._CF_enumeration.addEnumeration(unicode_value='between', tag='between')
RangeType._InitializeFacetMap(RangeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'RangeType', RangeType)

# Atomic simple type: {http://www.ebi.ac.uk/bii/isatab_configuration#}IsaTabAssayType
class IsaTabAssayType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """Every assay type must be mapped to one of the types defined in the ISATAB specification. If a
                certain endpoint/technology is specified in the
                ISA Configuration, but the ISATAB Assay Type (i.e.: the value of this attribute) is not, then the ISA
                configuration is used for performing
                the validation and the internal IL configuration is used to see if there is an ISATAB type that
                corresponds to the pair.
                If the pair is not even defined in the ISA Configuration, then the import layer will try to use the
                values defined in its internal
                configuration (i.e.: the ISA Configuration overrides the IL configuration). If all the above fails, then
                the assay is completely ignored.
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IsaTabAssayType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 135, 4)
    _Documentation = 'Every assay type must be mapped to one of the types defined in the ISATAB specification. If a\n                certain endpoint/technology is specified in the\n                ISA Configuration, but the ISATAB Assay Type (i.e.: the value of this attribute) is not, then the ISA\n                configuration is used for performing\n                the validation and the internal IL configuration is used to see if there is an ISATAB type that\n                corresponds to the pair.\n                If the pair is not even defined in the ISA Configuration, then the import layer will try to use the\n                values defined in its internal\n                configuration (i.e.: the ISA Configuration overrides the IL configuration). If all the above fails, then\n                the assay is completely ignored.\n            '
IsaTabAssayType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=IsaTabAssayType, enum_prefix=None)
IsaTabAssayType.generic_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='generic_assay', tag='generic_assay')
IsaTabAssayType.transcriptomics_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='transcriptomics_assay', tag='transcriptomics_assay')
IsaTabAssayType.ms_spec_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='ms_spec_assay', tag='ms_spec_assay')
IsaTabAssayType.nano_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='nano_assay', tag='nano_assay')
IsaTabAssayType.nmr_spec_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='nmr_spec_assay', tag='nmr_spec_assay')
IsaTabAssayType.gel_electrophoresis_assay = IsaTabAssayType._CF_enumeration.addEnumeration(unicode_value='gel_electrophoresis_assay', tag='gel_electrophoresis_assay')
IsaTabAssayType._InitializeFacetMap(IsaTabAssayType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'IsaTabAssayType', IsaTabAssayType)

# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}FieldType with content type ELEMENT_ONLY
class FieldType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}FieldType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FieldType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 9, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationdescription', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 11, 12), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}default-value uses Python identifier default_value
    __default_value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'default-value'), 'default_value', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationdefault_value', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 12, 12), )

    
    default_value = property(__default_value.value, __default_value.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}value-format uses Python identifier value_format
    __value_format = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'value-format'), 'value_format', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationvalue_format', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 13, 12), )

    
    value_format = property(__value_format.value, __value_format.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}list-values uses Python identifier list_values
    __list_values = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'list-values'), 'list_values', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationlist_values', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 14, 12), )

    
    list_values = property(__list_values.value, __list_values.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}generated-value-template uses Python identifier generated_value_template
    __generated_value_template = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'generated-value-template'), 'generated_value_template', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationgenerated_value_template', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 15, 12), )

    
    generated_value_template = property(__generated_value_template.value, __generated_value_template.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}value-range uses Python identifier value_range
    __value_range = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'value-range'), 'value_range', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationvalue_range', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 17, 12), )

    
    value_range = property(__value_range.value, __value_range.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}recommended-ontologies uses Python identifier recommended_ontologies
    __recommended_ontologies = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies'), 'recommended_ontologies', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_httpwww_ebi_ac_ukbiiisatab_configurationrecommended_ontologies', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 80, 4), )

    
    recommended_ontologies = property(__recommended_ontologies.value, __recommended_ontologies.set, None, None)

    
    # Attribute header uses Python identifier header
    __header = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'header'), 'header', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_header', pyxb.binding.datatypes.string)
    __header._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 19, 8)
    __header._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 19, 8)
    
    header = property(__header.value, __header.set, None, None)

    
    # Attribute data-type uses Python identifier data_type
    __data_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'data-type'), 'data_type', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_data_type', pyxb.binding.datatypes.string)
    __data_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 20, 8)
    __data_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 20, 8)
    
    data_type = property(__data_type.value, __data_type.set, None, None)

    
    # Attribute section uses Python identifier section
    __section = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'section'), 'section', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_section', pyxb.binding.datatypes.string)
    __section._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 21, 8)
    __section._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 21, 8)
    
    section = property(__section.value, __section.set, None, None)

    
    # Attribute is-hidden uses Python identifier is_hidden
    __is_hidden = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-hidden'), 'is_hidden', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_is_hidden', pyxb.binding.datatypes.boolean)
    __is_hidden._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 22, 8)
    __is_hidden._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 22, 8)
    
    is_hidden = property(__is_hidden.value, __is_hidden.set, None, None)

    
    # Attribute is-file-field uses Python identifier is_file_field
    __is_file_field = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-file-field'), 'is_file_field', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_is_file_field', pyxb.binding.datatypes.boolean)
    __is_file_field._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 23, 8)
    __is_file_field._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 23, 8)
    
    is_file_field = property(__is_file_field.value, __is_file_field.set, None, None)

    
    # Attribute is-multiple-value uses Python identifier is_multiple_value
    __is_multiple_value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-multiple-value'), 'is_multiple_value', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_is_multiple_value', pyxb.binding.datatypes.boolean)
    __is_multiple_value._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 24, 8)
    __is_multiple_value._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 24, 8)
    
    is_multiple_value = property(__is_multiple_value.value, __is_multiple_value.set, None, None)

    
    # Attribute is-required uses Python identifier is_required
    __is_required = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-required'), 'is_required', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_is_required', pyxb.binding.datatypes.boolean)
    __is_required._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 25, 8)
    __is_required._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 25, 8)
    
    is_required = property(__is_required.value, __is_required.set, None, None)

    
    # Attribute is-forced-ontology uses Python identifier is_forced_ontology
    __is_forced_ontology = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-forced-ontology'), 'is_forced_ontology', '__httpwww_ebi_ac_ukbiiisatab_configuration_FieldType_is_forced_ontology', pyxb.binding.datatypes.boolean)
    __is_forced_ontology._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 26, 8)
    __is_forced_ontology._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 26, 8)
    
    is_forced_ontology = property(__is_forced_ontology.value, __is_forced_ontology.set, None, None)

    _ElementMap.update({
        __description.name() : __description,
        __default_value.name() : __default_value,
        __value_format.name() : __value_format,
        __list_values.name() : __list_values,
        __generated_value_template.name() : __generated_value_template,
        __value_range.name() : __value_range,
        __recommended_ontologies.name() : __recommended_ontologies
    })
    _AttributeMap.update({
        __header.name() : __header,
        __data_type.name() : __data_type,
        __section.name() : __section,
        __is_hidden.name() : __is_hidden,
        __is_file_field.name() : __is_file_field,
        __is_multiple_value.name() : __is_multiple_value,
        __is_required.name() : __is_required,
        __is_forced_ontology.name() : __is_forced_ontology
    })
Namespace.addCategoryObject('typeBinding', 'FieldType', FieldType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}RecommendedOntologiesType with content type ELEMENT_ONLY
class RecommendedOntologiesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}RecommendedOntologiesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RecommendedOntologiesType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 29, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}ontology uses Python identifier ontology
    __ontology = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ontology'), 'ontology', '__httpwww_ebi_ac_ukbiiisatab_configuration_RecommendedOntologiesType_httpwww_ebi_ac_ukbiiisatab_configurationontology', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 31, 12), )

    
    ontology = property(__ontology.value, __ontology.set, None, None)

    _ElementMap.update({
        __ontology.name() : __ontology
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'RecommendedOntologiesType', RecommendedOntologiesType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}OntologyType with content type ELEMENT_ONLY
class OntologyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}OntologyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OntologyType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 35, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}branch uses Python identifier branch
    __branch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'branch'), 'branch', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyType_httpwww_ebi_ac_ukbiiisatab_configurationbranch', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 37, 12), )

    
    branch = property(__branch.value, __branch.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyType_id', pyxb.binding.datatypes.string)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 39, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 39, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute abbreviation uses Python identifier abbreviation
    __abbreviation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'abbreviation'), 'abbreviation', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyType_abbreviation', pyxb.binding.datatypes.string)
    __abbreviation._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 40, 8)
    __abbreviation._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 40, 8)
    
    abbreviation = property(__abbreviation.value, __abbreviation.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 41, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 41, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyType_version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 42, 8)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 42, 8)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __branch.name() : __branch
    })
    _AttributeMap.update({
        __id.name() : __id,
        __abbreviation.name() : __abbreviation,
        __name.name() : __name,
        __version.name() : __version
    })
Namespace.addCategoryObject('typeBinding', 'OntologyType', OntologyType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}BranchType with content type EMPTY
class BranchType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}BranchType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BranchType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 45, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_ebi_ac_ukbiiisatab_configuration_BranchType_id', pyxb.binding.datatypes.string)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 46, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 46, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpwww_ebi_ac_ukbiiisatab_configuration_BranchType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 47, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 47, 8)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __name.name() : __name
    })
Namespace.addCategoryObject('typeBinding', 'BranchType', BranchType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}StructuredFieldType with content type EMPTY
class StructuredFieldType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}StructuredFieldType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StructuredFieldType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 52, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpwww_ebi_ac_ukbiiisatab_configuration_StructuredFieldType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 53, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 53, 8)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name
    })
Namespace.addCategoryObject('typeBinding', 'StructuredFieldType', StructuredFieldType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}ProtocolFieldType with content type EMPTY
class ProtocolFieldType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}ProtocolFieldType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProtocolFieldType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 58, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute protocol-type uses Python identifier protocol_type
    __protocol_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'protocol-type'), 'protocol_type', '__httpwww_ebi_ac_ukbiiisatab_configuration_ProtocolFieldType_protocol_type', pyxb.binding.datatypes.string)
    __protocol_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 59, 8)
    __protocol_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 59, 8)
    
    protocol_type = property(__protocol_type.value, __protocol_type.set, None, None)

    
    # Attribute data-type uses Python identifier data_type
    __data_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'data-type'), 'data_type', '__httpwww_ebi_ac_ukbiiisatab_configuration_ProtocolFieldType_data_type', pyxb.binding.datatypes.string)
    __data_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 60, 8)
    __data_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 60, 8)
    
    data_type = property(__data_type.value, __data_type.set, None, None)

    
    # Attribute is-required uses Python identifier is_required
    __is_required = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-required'), 'is_required', '__httpwww_ebi_ac_ukbiiisatab_configuration_ProtocolFieldType_is_required', pyxb.binding.datatypes.boolean)
    __is_required._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 61, 8)
    __is_required._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 61, 8)
    
    is_required = property(__is_required.value, __is_required.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __protocol_type.name() : __protocol_type,
        __data_type.name() : __data_type,
        __is_required.name() : __is_required
    })
Namespace.addCategoryObject('typeBinding', 'ProtocolFieldType', ProtocolFieldType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}UnitFieldType with content type ELEMENT_ONLY
class UnitFieldType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}UnitFieldType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UnitFieldType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 67, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_httpwww_ebi_ac_ukbiiisatab_configurationdescription', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 69, 12), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}list-values uses Python identifier list_values
    __list_values = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'list-values'), 'list_values', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_httpwww_ebi_ac_ukbiiisatab_configurationlist_values', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 70, 12), )

    
    list_values = property(__list_values.value, __list_values.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}default-value uses Python identifier default_value
    __default_value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'default-value'), 'default_value', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_httpwww_ebi_ac_ukbiiisatab_configurationdefault_value', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 72, 12), )

    
    default_value = property(__default_value.value, __default_value.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}recommended-ontologies uses Python identifier recommended_ontologies
    __recommended_ontologies = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies'), 'recommended_ontologies', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_httpwww_ebi_ac_ukbiiisatab_configurationrecommended_ontologies', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 80, 4), )

    
    recommended_ontologies = property(__recommended_ontologies.value, __recommended_ontologies.set, None, None)

    
    # Attribute data-type uses Python identifier data_type
    __data_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'data-type'), 'data_type', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_data_type', pyxb.binding.datatypes.string)
    __data_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 74, 8)
    __data_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 74, 8)
    
    data_type = property(__data_type.value, __data_type.set, None, None)

    
    # Attribute is-multiple-value uses Python identifier is_multiple_value
    __is_multiple_value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-multiple-value'), 'is_multiple_value', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_is_multiple_value', pyxb.binding.datatypes.boolean)
    __is_multiple_value._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 75, 8)
    __is_multiple_value._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 75, 8)
    
    is_multiple_value = property(__is_multiple_value.value, __is_multiple_value.set, None, None)

    
    # Attribute is-required uses Python identifier is_required
    __is_required = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-required'), 'is_required', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_is_required', pyxb.binding.datatypes.boolean)
    __is_required._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 76, 8)
    __is_required._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 76, 8)
    
    is_required = property(__is_required.value, __is_required.set, None, None)

    
    # Attribute is-forced-ontology uses Python identifier is_forced_ontology
    __is_forced_ontology = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'is-forced-ontology'), 'is_forced_ontology', '__httpwww_ebi_ac_ukbiiisatab_configuration_UnitFieldType_is_forced_ontology', pyxb.binding.datatypes.boolean)
    __is_forced_ontology._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 77, 8)
    __is_forced_ontology._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 77, 8)
    
    is_forced_ontology = property(__is_forced_ontology.value, __is_forced_ontology.set, None, None)

    _ElementMap.update({
        __description.name() : __description,
        __list_values.name() : __list_values,
        __default_value.name() : __default_value,
        __recommended_ontologies.name() : __recommended_ontologies
    })
    _AttributeMap.update({
        __data_type.name() : __data_type,
        __is_multiple_value.name() : __is_multiple_value,
        __is_required.name() : __is_required,
        __is_forced_ontology.name() : __is_forced_ontology
    })
Namespace.addCategoryObject('typeBinding', 'UnitFieldType', UnitFieldType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}IsaTabConfigFileType with content type ELEMENT_ONLY
class IsaTabConfigFileType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}IsaTabConfigFileType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IsaTabConfigFileType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 118, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}isatab-configuration uses Python identifier isatab_configuration
    __isatab_configuration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isatab-configuration'), 'isatab_configuration', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigFileType_httpwww_ebi_ac_ukbiiisatab_configurationisatab_configuration', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 90, 4), )

    
    isatab_configuration = property(__isatab_configuration.value, __isatab_configuration.set, None, None)

    _ElementMap.update({
        __isatab_configuration.name() : __isatab_configuration
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'IsaTabConfigFileType', IsaTabConfigFileType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}OntologyEntryType with content type EMPTY
class OntologyEntryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}OntologyEntryType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OntologyEntryType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 159, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute term-label uses Python identifier term_label
    __term_label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'term-label'), 'term_label', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_term_label', pyxb.binding.datatypes.string, required=True)
    __term_label._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 160, 8)
    __term_label._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 160, 8)
    
    term_label = property(__term_label.value, __term_label.set, None, None)

    
    # Attribute term-accession uses Python identifier term_accession
    __term_accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'term-accession'), 'term_accession', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_term_accession', pyxb.binding.datatypes.string)
    __term_accession._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 161, 8)
    __term_accession._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 161, 8)
    
    term_accession = property(__term_accession.value, __term_accession.set, None, None)

    
    # Attribute source-abbreviation uses Python identifier source_abbreviation
    __source_abbreviation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source-abbreviation'), 'source_abbreviation', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_source_abbreviation', pyxb.binding.datatypes.string)
    __source_abbreviation._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 162, 8)
    __source_abbreviation._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 162, 8)
    
    source_abbreviation = property(__source_abbreviation.value, __source_abbreviation.set, None, None)

    
    # Attribute source-title uses Python identifier source_title
    __source_title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source-title'), 'source_title', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_source_title', pyxb.binding.datatypes.string)
    __source_title._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 163, 8)
    __source_title._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 163, 8)
    
    source_title = property(__source_title.value, __source_title.set, None, None)

    
    # Attribute source-version uses Python identifier source_version
    __source_version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source-version'), 'source_version', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_source_version', pyxb.binding.datatypes.string)
    __source_version._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 164, 8)
    __source_version._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 164, 8)
    
    source_version = property(__source_version.value, __source_version.set, None, None)

    
    # Attribute source-uri uses Python identifier source_uri
    __source_uri = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'source-uri'), 'source_uri', '__httpwww_ebi_ac_ukbiiisatab_configuration_OntologyEntryType_source_uri', pyxb.binding.datatypes.string)
    __source_uri._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 165, 8)
    __source_uri._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 165, 8)
    
    source_uri = property(__source_uri.value, __source_uri.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __term_label.name() : __term_label,
        __term_accession.name() : __term_accession,
        __source_abbreviation.name() : __source_abbreviation,
        __source_title.name() : __source_title,
        __source_version.name() : __source_version,
        __source_uri.name() : __source_uri
    })
Namespace.addCategoryObject('typeBinding', 'OntologyEntryType', OntologyEntryType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}ValueRangeType with content type EMPTY
class ValueRangeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}ValueRangeType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ValueRangeType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 82, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpwww_ebi_ac_ukbiiisatab_configuration_ValueRangeType_type', RangeType)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 83, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 83, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'min'), 'min', '__httpwww_ebi_ac_ukbiiisatab_configuration_ValueRangeType_min', pyxb.binding.datatypes.string)
    __min._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 85, 8)
    __min._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 85, 8)
    
    min = property(__min.value, __min.set, None, None)

    
    # Attribute max uses Python identifier max
    __max = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'max'), 'max', '__httpwww_ebi_ac_ukbiiisatab_configuration_ValueRangeType_max', pyxb.binding.datatypes.string)
    __max._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 86, 8)
    __max._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 86, 8)
    
    max = property(__max.value, __max.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __min.name() : __min,
        __max.name() : __max
    })
Namespace.addCategoryObject('typeBinding', 'ValueRangeType', ValueRangeType)


# Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}IsaTabConfigurationType with content type ELEMENT_ONLY
class IsaTabConfigurationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ebi.ac.uk/bii/isatab_configuration#}IsaTabConfigurationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IsaTabConfigurationType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 92, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}field uses Python identifier field
    __field = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'field'), 'field', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationfield', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 7, 4), )

    
    field = property(__field.value, __field.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}structured-field uses Python identifier structured_field
    __structured_field = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'structured-field'), 'structured_field', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationstructured_field', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 50, 4), )

    
    structured_field = property(__structured_field.value, __structured_field.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}protocol-field uses Python identifier protocol_field
    __protocol_field = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'protocol-field'), 'protocol_field', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationprotocol_field', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 56, 4), )

    
    protocol_field = property(__protocol_field.value, __protocol_field.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}unit-field uses Python identifier unit_field
    __unit_field = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'unit-field'), 'unit_field', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationunit_field', True, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 65, 4), )

    
    unit_field = property(__unit_field.value, __unit_field.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}measurement uses Python identifier measurement
    __measurement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'measurement'), 'measurement', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationmeasurement', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 94, 12), )

    
    measurement = property(__measurement.value, __measurement.set, None, None)

    
    # Element {http://www.ebi.ac.uk/bii/isatab_configuration#}technology uses Python identifier technology
    __technology = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'technology'), 'technology', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_httpwww_ebi_ac_ukbiiisatab_configurationtechnology', False, pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 95, 12), )

    
    technology = property(__technology.value, __technology.set, None, None)

    
    # Attribute table-name uses Python identifier table_name
    __table_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'table-name'), 'table_name', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_table_name', pyxb.binding.datatypes.string, required=True)
    __table_name._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 103, 8)
    __table_name._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 103, 8)
    
    table_name = property(__table_name.value, __table_name.set, None, None)

    
    # Attribute isatab-assay-type uses Python identifier isatab_assay_type
    __isatab_assay_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isatab-assay-type'), 'isatab_assay_type', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_isatab_assay_type', IsaTabAssayType)
    __isatab_assay_type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 104, 8)
    __isatab_assay_type._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 104, 8)
    
    isatab_assay_type = property(__isatab_assay_type.value, __isatab_assay_type.set, None, None)

    
    # Attribute isatab-conversion-target uses Python identifier isatab_conversion_target
    __isatab_conversion_target = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isatab-conversion-target'), 'isatab_conversion_target', '__httpwww_ebi_ac_ukbiiisatab_configuration_IsaTabConfigurationType_isatab_conversion_target', pyxb.binding.datatypes.string)
    __isatab_conversion_target._DeclarationLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 105, 8)
    __isatab_conversion_target._UseLocation = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 105, 8)
    
    isatab_conversion_target = property(__isatab_conversion_target.value, __isatab_conversion_target.set, None, 'The conversion target. This is used by the converter to decide if a certain assay type\n                    can be converted into an omics-specific format or not.\n                    Current supported values are: magetab, prideml, ena. More targets can be added by extending the\n                    converter.\n                ')

    _ElementMap.update({
        __field.name() : __field,
        __structured_field.name() : __structured_field,
        __protocol_field.name() : __protocol_field,
        __unit_field.name() : __unit_field,
        __measurement.name() : __measurement,
        __technology.name() : __technology
    })
    _AttributeMap.update({
        __table_name.name() : __table_name,
        __isatab_assay_type.name() : __isatab_assay_type,
        __isatab_conversion_target.name() : __isatab_conversion_target
    })
Namespace.addCategoryObject('typeBinding', 'IsaTabConfigurationType', IsaTabConfigurationType)


field = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'field'), FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 7, 4))
Namespace.addCategoryObject('elementBinding', field.name().localName(), field)

structured_field = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'structured-field'), StructuredFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 50, 4))
Namespace.addCategoryObject('elementBinding', structured_field.name().localName(), structured_field)

protocol_field = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'protocol-field'), ProtocolFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 56, 4))
Namespace.addCategoryObject('elementBinding', protocol_field.name().localName(), protocol_field)

unit_field = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'unit-field'), UnitFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 65, 4))
Namespace.addCategoryObject('elementBinding', unit_field.name().localName(), unit_field)

recommended_ontologies = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies'), RecommendedOntologiesType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 80, 4))
Namespace.addCategoryObject('elementBinding', recommended_ontologies.name().localName(), recommended_ontologies)

isatab_config_file = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isatab-config-file'), IsaTabConfigFileType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 116, 4))
Namespace.addCategoryObject('elementBinding', isatab_config_file.name().localName(), isatab_config_file)

isatab_configuration = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isatab-configuration'), IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 90, 4))
Namespace.addCategoryObject('elementBinding', isatab_configuration.name().localName(), isatab_configuration)



FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), pyxb.binding.datatypes.string, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 11, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'default-value'), pyxb.binding.datatypes.string, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 12, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'value-format'), pyxb.binding.datatypes.string, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 13, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'list-values'), pyxb.binding.datatypes.string, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 14, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'generated-value-template'), pyxb.binding.datatypes.string, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 15, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'value-range'), ValueRangeType, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 17, 12)))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies'), RecommendedOntologiesType, scope=FieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 80, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 11, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 11, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 12, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'default-value')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 12, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 13, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'value-format')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 13, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 14, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'list-values')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 14, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 15, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'generated-value-template')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 15, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 16, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 16, 12))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 17, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'value-range')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 17, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 11, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 12, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 13, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 14, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 15, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 16, 12))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 17, 12))
    counters.add(cc_6)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_())
    sub_automata.append(_BuildAutomaton_2())
    sub_automata.append(_BuildAutomaton_3())
    sub_automata.append(_BuildAutomaton_4())
    sub_automata.append(_BuildAutomaton_5())
    sub_automata.append(_BuildAutomaton_6())
    sub_automata.append(_BuildAutomaton_7())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 10, 8)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FieldType._Automaton = _BuildAutomaton()




RecommendedOntologiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ontology'), OntologyType, scope=RecommendedOntologiesType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 31, 12)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 30, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 31, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(RecommendedOntologiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ontology')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
RecommendedOntologiesType._Automaton = _BuildAutomaton_8()




OntologyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'branch'), BranchType, scope=OntologyType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 37, 12)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 36, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 37, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(OntologyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'branch')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 37, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
OntologyType._Automaton = _BuildAutomaton_9()




UnitFieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), pyxb.binding.datatypes.string, scope=UnitFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 69, 12)))

UnitFieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'list-values'), pyxb.binding.datatypes.string, scope=UnitFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 70, 12)))

UnitFieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'default-value'), pyxb.binding.datatypes.string, scope=UnitFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 72, 12)))

UnitFieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies'), RecommendedOntologiesType, scope=UnitFieldType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 80, 4)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(UnitFieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 69, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=st_0)

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 70, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UnitFieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'list-values')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 70, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 71, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UnitFieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recommended-ontologies')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 71, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 72, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UnitFieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'default-value')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 72, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 70, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 71, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 72, 12))
    counters.add(cc_2)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_11())
    sub_automata.append(_BuildAutomaton_12())
    sub_automata.append(_BuildAutomaton_13())
    sub_automata.append(_BuildAutomaton_14())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 68, 8)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
UnitFieldType._Automaton = _BuildAutomaton_10()




IsaTabConfigFileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isatab-configuration'), IsaTabConfigurationType, scope=IsaTabConfigFileType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 90, 4)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 119, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigFileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isatab-configuration')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 120, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
IsaTabConfigFileType._Automaton = _BuildAutomaton_15()




IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'field'), FieldType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 7, 4)))

IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'structured-field'), StructuredFieldType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 50, 4)))

IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'protocol-field'), ProtocolFieldType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 56, 4)))

IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'unit-field'), UnitFieldType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 65, 4)))

IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'measurement'), OntologyEntryType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 94, 12)))

IsaTabConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'technology'), OntologyEntryType, scope=IsaTabConfigurationType, location=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 95, 12)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 96, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'measurement')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 94, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'technology')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 95, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'field')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 97, 16))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'protocol-field')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 98, 16))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'structured-field')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 99, 16))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IsaTabConfigurationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'unit-field')), pyxb.utils.utility.Location('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isatab_configurator.xsd', 100, 16))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IsaTabConfigurationType._Automaton = _BuildAutomaton_16()

