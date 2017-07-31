<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY nbsp "&#160;">
  <!ENTITY copy "&#169;">
]>

<!--xsl stylesheet prototype for rendering SRA XML documents to ISA-Tab representation:

Authors: 
Philippe Rocca-Serra, University of Oxford e-Research Centre (philippe.rocca-serra@oerc.ox.ac.uk);
Alfie Abdul-Rahman, University of Oxford e-Research Centre (alfie.abdulrahman@oerc.ox.ac.uk) 

test datasets:
SRA030397 -> targeted metagenomics application
SRA000266 -> targeted metagenomics application
ERA148766 -> 
SRA095866 ->

representing submission 

SRA schema version considered:

 <xsl:import-schema schema-location="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.submission.xsd"/>
 <xsl:import-schema schema-location="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.study.xsd"/>
 <xsl:import-schema schema-location="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd"/>
 <xsl:import-schema schema-location="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.experiment.xsd"/>
 <xsl:import-schema schema-location="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.run.xsd"/>

-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:isa="http://www.isa-tools.org/"
 exclude-result-prefixes="isa" version="2.0">
 <xsl:import href="extract-studies-rice.xsl"/>
 <xsl:import href="isa-functions.xsl"/>
 <xsl:output method="text" encoding="UTF-8"/>
 <xsl:strip-space elements="*"/>

 <!-- The input parameter from the command line -->
 <xsl:param name="acc-number" required="yes"/>
 <xsl:param name="outputdir" required="yes"/>

 <xsl:key name="protocols" match="LIBRARY_CONSTRUCTION_PROTOCOL" use="."/>
 <xsl:key name="sampletaglookupid" match="/ROOT/SAMPLE/SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE/TAG" use="."/>
 <xsl:key name="expprotlookupid" match="/ROOT/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_CONSTRUCTION_PROTOCOL" use="."/>

 <xsl:variable name="url" select="concat('http://www.ebi.ac.uk/ena/data/view/', $acc-number, '&amp;display=xml')"/>
 
 <xsl:variable name="experiments-sources-strategies">
  <xsl:call-template name="process-lib-strategies-sources">
   <xsl:with-param name="acc-number" select="$acc-number"/>
  </xsl:call-template>
 </xsl:variable>
 
 <xsl:variable name="distinct-exp-sources-strategies">
  <xsl:call-template name="generate-distinct-exp-sources-strategies">
   <xsl:with-param name="exp-sources-strategies" select="$experiments-sources-strategies"/>
  </xsl:call-template>
 </xsl:variable>

 <xsl:variable name="samples-characteristics">
  <xsl:call-template name="process-samples-attributes">
   <xsl:with-param name="acc-number" select="$acc-number"/>
  </xsl:call-template>
 </xsl:variable>
 
 <xsl:variable name="distinct-characteristic-terms">
  <xsl:call-template name="generate-distinct-characteristic-terms">
   <xsl:with-param name="characteristics" select="$samples-characteristics"/>
  </xsl:call-template>
 </xsl:variable>
 
 <xsl:variable name="distinct-exp-protocol-descriptions">
  <xsl:call-template name="generate-distinct-protocols-description">
   <xsl:with-param name="protocol" select="$experiments-sources-strategies"/>
  </xsl:call-template>
 </xsl:variable> 
 
 <xsl:template match="/">
  <xsl:apply-templates select="document($url)" mode="go"/>
 </xsl:template>
 
 <xsl:template match="ROOT" mode="go">
  <xsl:variable name="broker-name" select="if (@broker_name) then @broker_name else ''"/> 
  <xsl:apply-templates>
   <xsl:with-param name="broker-name" select="$broker-name" tunnel="yes"/>
  </xsl:apply-templates>
  <xsl:call-template name="generate-assay-files"/>
  <xsl:apply-templates select="STUDY/STUDY_LINKS"/>
 </xsl:template>
 
 <xsl:template match="STUDY">
  <xsl:param name="broker-name" required="yes" tunnel="yes"/>
  <xsl:variable name="study" select="following-sibling::ID"/>
  <xsl:result-document href="{concat($outputdir,'/', $acc-number, '/', 'i_', $acc-number, '.txt')}" method="text">
   <xsl:text>#SRA Document:</xsl:text>    <xsl:value-of select="isa:quotes($acc-number)"/><xsl:text>&#10;</xsl:text>
   <xsl:text>"ONTOLOGY SOURCE REFERENCE"&#10;</xsl:text>
   <xsl:value-of select="isa:single-name-value('Term Source Name', 'OBI')"/>
   <xsl:value-of select="isa:single-name-value('Term Source File', 'http://purl.obolibrary.org/obo/OBI.owl')"/>
   <xsl:value-of select="isa:single-name-value('Term Source Version', '1')"/>
   <xsl:value-of select="isa:single-name-value('Term Source Description', 'Controlled Terminology for SRA/ENA schema')"/>"INVESTIGATION"
"Investigation Identifier"&#9;""
"Investigation Title"&#9;""
"Investigation Description"&#9;""
"Investigation Submission Date"&#9;""
"Investigation Public Release Date"&#9;""
"INVESTIGATION PUBLICATIONS"
"Investigation PubMed ID"&#9;""
"Investigation Publication DOI"&#9;""
"Investigation Publication Author List"&#9;""
"Investigation Publication Title"&#9;""
"Investigation Publication Status"&#9;""
"Investigation Publication Status Term Accession Number"&#9;""
"Investigation Publication Status Term Source REF"&#9;""
"INVESTIGATION CONTACTS"
"Investigation Person Last Name"&#9;""
"Investigation Person First Name"&#9;""
"Investigation Person Mid Initials"&#9;""
"Investigation Person Email"&#9;""
"Investigation Person Phone"&#9;""
"Investigation Person Fax"&#9;""
"Investigation Person Address"&#9;""
"Investigation Person Affiliation"&#9;""
"Investigation Person Roles"&#9;""
"Investigation Person Roles Term Accession Number"&#9;""
"Investigation Person Roles Term Source REF"&#9;""
"STUDY"
<xsl:value-of select="isa:single-name-value('Comment[SRA broker]', $broker-name)"/>
   <xsl:call-template name="generate-rest-of-study"/>
   <!--<xsl:apply-templates select="document(concat('http://www.ebi.ac.uk/ena/data/view/',$study,'&amp;display=xml'))/ROOT/STUDY"/>-->
   <xsl:text>&#10;"STUDY CONTACTS"&#10;</xsl:text>
   <xsl:value-of select="isa:single-name-value('Comment[SRA broker]', $broker-name)"/>
   <xsl:value-of select="isa:single-name-value('Study Person Last Name', substring-before(CONTACTS/CONTACT/@name,' '))"/>
   <xsl:value-of select="isa:single-name-value('Study Person First Name', substring-after(CONTACTS/CONTACT/@name,' '))"/>
   <xsl:value-of select="isa:single-name-value('Study Person Mid Initials', '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Email', CONTACTS/CONTACT/@inform_on_status)"/>
   <xsl:value-of select="isa:single-name-value('Study Person Phone', if (CONTACTS/CONTACT) then '-' else '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Fax', if (CONTACTS/CONTACT) then '-' else '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Address', '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Affiliation', '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Roles', '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Roles Term Accession Number', '')"/>
   <xsl:value-of select="isa:single-name-value('Study Person Roles Term Source REF', '')"/>
  </xsl:result-document>
 </xsl:template>

 <xsl:template match="STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(.,'NA-SAMPLE')]">
  <xsl:result-document href="{concat($outputdir,'/',$acc-number, '/', 's_', $acc-number, '.txt')}" method="text">
   <xsl:variable name="samples-ids" select="following-sibling::ID"/>
   <xsl:call-template name="generate-study-header"/>
   <xsl:text>"Sample Name"&#10;</xsl:text>
   <xsl:for-each select="tokenize($samples-ids, ',')">
    <xsl:apply-templates select="document(concat('http://www.ebi.ac.uk/ena/data/view/', . , '&amp;display=xml'))/ROOT/SAMPLE"/>
   </xsl:for-each>
  </xsl:result-document>
 </xsl:template>
 
 <xsl:template name="generate-study-header">
  <xsl:text>"Source Name"&#9;</xsl:text>
  <xsl:text>"Characteristics[Primary Accession Number]"&#9;</xsl:text>
  <xsl:text>"Comment[Common Name]"&#9;</xsl:text>
  <xsl:text>"Comment[Scientific Name]"&#9;</xsl:text>
  <xsl:text>"Characteristics[Taxonomic ID]"&#9;</xsl:text>
  <xsl:text>"Characteristics[Description]"&#9;</xsl:text>
  <xsl:for-each select="$distinct-characteristic-terms/terms/term">
   <xsl:value-of select="isa:quotes(concat('Characteristics[', ., ']'))"/> <xsl:text>&#9;</xsl:text>
  </xsl:for-each>
 </xsl:template>
 
 <xsl:template name="generate-assay-files">
  <xsl:apply-templates select="$distinct-exp-sources-strategies/experiments" mode="distinct-exp"/>
 </xsl:template>
 
 <xsl:template match="experiments/experiment" mode="distinct-exp">
  <xsl:result-document href="{concat($outputdir,'/', $acc-number, '/', 'a_', lower-case(@library-strategy), '-', lower-case(@library-source), '-',  @acc-number, '.txt')}" method="text">
   <xsl:variable name="my-exp" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', @acc-number, '&amp;display=xml'))"/>
 <!--  <xsl:value-of select="$my-exp"/> -->
   
   <!-- Create the header -->
   <xsl:text>"Sample Name"&#9;</xsl:text>
   <xsl:text>"Protocol REF"&#9;</xsl:text>
   <xsl:text>"Parameter Value[library strategy]"&#9;</xsl:text>
   <xsl:text>"Parameter Value[library source]"&#9;</xsl:text>
   <xsl:text>"Parameter Value[library selection]"&#9;</xsl:text>
   <xsl:text>"Parameter Value[library layout]"&#9;</xsl:text>
   
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'target_taxon: ')]) > 0) 
    then 'Parameter Value[target_taxon]&#9;' else ''"/>
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'target_gene: ')]) > 0) 
    then 'Parameter Value[target_gene]&#9;' else ''"/>
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'target_subfragment: ')]) > 0) 
    then 'Parameter Value[target_subfragment]&#9;' else ''"/> 
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'mid: ')]) > 0) 
    then 'Parameter Value[multiplex identifier]&#9;' else ''"/>   
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'pcr_primers: ')]) > 0) 
    then 'Parameter Value[pcr_primers]&#9;' else ''"/>   
   <xsl:value-of select="if (count($my-exp/ROOT/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION[contains(., 'pcr_cond: ')]) > 0) 
    then 'Parameter Value[pcr_conditions]&#9;' else ''"/>
   
   <xsl:text>"Labeled Extract Name"&#9;</xsl:text>
   <xsl:text>"Protocol REF"&#9;</xsl:text>
   <xsl:text>"Parameter Value[read information {index;type;class;base coord}]"&#9;</xsl:text>
   <xsl:text>"Parameter Value[sequencing instrument]"&#9;</xsl:text>
   <xsl:text>"Performer"&#9;</xsl:text>
   <xsl:text>"Date"&#9;</xsl:text>
   <xsl:text>"Assay Name"&#9;</xsl:text>
   <xsl:text>"Raw Data File"&#9;</xsl:text>
   <xsl:text>"Comment[File checksum]"&#9;</xsl:text>
   <xsl:text>"Comment[File checksum method]"&#10;</xsl:text>
   <xsl:apply-templates select="exp">
    <xsl:with-param name="my-exp" select="$my-exp"/>
   </xsl:apply-templates>
  </xsl:result-document>
 </xsl:template>
 
 <xsl:template match="exp">
  <xsl:param name="my-exp" required="yes"/>
  <xsl:apply-templates select="$my-exp/ROOT/EXPERIMENT[@accession = current()/@accession]"/>
  <!--<xsl:value-of select="$my-exp"/><xsl:text>THERE&#9;</xsl:text>-->
<!--    <xsl:value-of select="$my-exp/ROOT/EXPERIMENT[@accession = current()/@accession]"></xsl:value-of><xsl:text>&#9;</xsl:text>-->
  <!--  -->
 </xsl:template>
 
 <xsl:template name="generate-rest-of-study">
  <xsl:variable name="sra-isa-mapping" select="document('sra-isa-measurement_type_mapping.xml')"/>
 
  <xsl:value-of select="isa:single-name-value('Study Identifier', @accession)"/>
  <xsl:value-of select="isa:single-name-value('Study Title', DESCRIPTOR/STUDY_TITLE)"/>
  <xsl:value-of select="isa:single-name-value('Study Submission Date', SRA/SUBMISSION/@submission_date)"/> 
  <xsl:value-of select="isa:single-name-value('Study Public Release Date', SRA/SUBMISSION/@submission_date)"/> 
  
  <xsl:text>"Study Description"&#9;</xsl:text>
  <xsl:value-of select="isa:quotes(DESCRIPTOR/STUDY_ABSTRACT)"/>
  <xsl:value-of select="isa:quotes(substring-before(DESCRIPTOR/STUDY_DESCRIPTION,'\r'))"/>
  <xsl:text>&#10;</xsl:text>
  
  <xsl:text>"Study File Name"&#9;</xsl:text>
  <xsl:value-of select="isa:quotes(concat('s_', $acc-number, '.txt'))"/><xsl:text>&#10;</xsl:text>
  <xsl:text>"STUDY DESIGN DESCRIPTORS"&#10;</xsl:text>

  <xsl:apply-templates select="DESCRIPTOR/STUDY_TYPE"/>

  <xsl:value-of select="isa:single-name-value('Study Design Type Term Accession Number', '')"/>
  <xsl:value-of select="isa:single-name-value('Study Design Type Term Source REF', '')"/>
  
  <xsl:text>"STUDY PUBLICATIONS"&#10;</xsl:text>
  <xsl:text>"Study PubMed ID"</xsl:text>
  <xsl:choose>
   <xsl:when test="count(STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(., 'pubmed')]) > 0">
    <xsl:apply-templates select="STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(., 'pubmed')]"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:text>&#9;""</xsl:text>
   </xsl:otherwise>
  </xsl:choose>

  <xsl:variable name="study-pub-count" select="count(STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(., 'pubmed')])"/>
  <xsl:variable name="study-pub-headings">
   <headings>
    <heading>Study Publication DOI</heading>
    <heading>Study Publication Author List</heading>
    <heading>Study Publication Title</heading>
    <heading>Study Publication Status</heading>
    <heading>Study Publication Status Term Accession Number</heading>
    <heading>Study Publication Status Term Source REF</heading>
   </headings>
  </xsl:variable>
  <xsl:call-template name="create-list-items">
   <xsl:with-param name="headings" select="$study-pub-headings"/>
   <xsl:with-param name="iterations" select="$study-pub-count"/>
  </xsl:call-template>
  
  <xsl:text>&#10;"STUDY FACTORS"&#10;</xsl:text>
  <xsl:value-of select="isa:single-name-value('Study Factor Name', '')"/>
  <xsl:value-of select="isa:single-name-value('Study Factor Type', '')"/>
  <xsl:value-of select="isa:single-name-value('Study Factor Type Term Accession Number', '')"/>
  <xsl:value-of select="isa:single-name-value('Study Factor Type Term Source REF', '')"/>
  
  <xsl:text>"STUDY ASSAYS"&#10;</xsl:text>
  <xsl:text>"Study Assay Measurement Type"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="if ($sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]) then concat('&#9;&quot;', $sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]/@isa, '&quot;') else concat('&#9;&quot;','other','&quot;')"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>

  <xsl:text>"Study Assay Measurement Type Term Accession Number"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="if ($sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]) then concat('&#9;&quot;', $sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]/@accnum, '&quot;') else '&#9;&quot;&quot;'"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>

  <xsl:text>"Study Assay Measurement Type Term Source REF"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="if ($sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]) then concat('&#9;&quot;', $sra-isa-mapping/mapping/pairs/measurement[lower-case(@SRA_strategy)=lower-case(current()/@library-strategy)]/@resource, '&quot;') else '&#9;&quot;&quot;'"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>

  <xsl:text>"Study Assay Technology Type"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="concat('&#9;', '&quot;nucleic acid sequencing&quot;')"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>

  <xsl:text>"Study Assay Technology Type Term Accession Number"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="concat('&#9;', '&quot;&quot;')"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>

  <xsl:text>"Study Assay Technology Type Term Source REF"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="concat('&#9;', '&quot;&quot;')"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>
  
  <xsl:value-of select="isa:single-name-value('Study Assay Technology Platform', '')"/>
  
  <xsl:text>"Study Assay File Name"</xsl:text>
  <xsl:for-each select="$distinct-exp-sources-strategies/experiments/experiment[1]">
   <xsl:value-of select="concat('&#9;&quot;a_', $acc-number, '.txt&quot;')"/>
  </xsl:for-each>
  <xsl:text>&#10;</xsl:text>
  
  <xsl:text>"STUDY PROTOCOLS"&#10;</xsl:text>
  <xsl:text>"Study Protocol Name"</xsl:text>
  <xsl:for-each select="$distinct-exp-protocol-descriptions/descriptions/description">
   <xsl:value-of select="concat('&#9;', isa:quotes('library preparation'))"/>
  </xsl:for-each>
  <xsl:text>&#9;"nucleic acid sequencing"&#10;</xsl:text>
  <xsl:text>"Study Protocol Type"</xsl:text>
  <xsl:for-each select="$distinct-exp-protocol-descriptions/descriptions/description">
   <xsl:value-of select="concat('&#9;', isa:quotes('library preparation'))"/>
  </xsl:for-each>
  <xsl:text>&#9;"nucleic acid sequencing"</xsl:text>
  <xsl:variable name="study-protocol-count" select="count($distinct-exp-protocol-descriptions/descriptions/description)"/>
  <xsl:variable name="study-protocol-headings-1">
   <headings>
    <heading>Study Protocol Type Term Accession Number</heading>
    <heading>Study Protocol Type Term Source REF</heading>
   </headings>
  </xsl:variable>
  <xsl:call-template name="create-list-items">
   <xsl:with-param name="headings" select="$study-protocol-headings-1"/>
   <xsl:with-param name="iterations" select="$study-protocol-count + 1"/>
  </xsl:call-template>
  <xsl:text>&#10;</xsl:text>
  <xsl:text>"Study Protocol Description"</xsl:text>
  <xsl:for-each select="$distinct-exp-protocol-descriptions/descriptions/description">
   <xsl:value-of select="concat('&#9;', isa:quotes(@protocoldescription))"/>
  </xsl:for-each>
  <xsl:text>&#9;""</xsl:text>
  <xsl:variable name="study-protocol-headings-2">
   <headings>
    <heading>Study Protocol URI</heading>
    <heading>Study Protocol Version</heading>
    <heading>Study Protocol Parameters Name</heading>
    <heading>Study Protocol Parameters Term Accession Number</heading>
    <heading>Study Protocol Parameters Term Source REF</heading>
    <heading>Study Protocol Components Name</heading>
    <heading>Study Protocol Components Type</heading>
    <heading>Study Protocol Components Type Term Accession Number</heading>
    <heading>Study Protocol Components Type Term Source REF</heading>
   </headings>
  </xsl:variable>
  <xsl:call-template name="create-list-items">
   <xsl:with-param name="headings" select="$study-protocol-headings-2"/>
   <xsl:with-param name="iterations" select="$study-protocol-count + 1"/>
  </xsl:call-template>
 </xsl:template>
 
 <xsl:template name="create-list-items">
  <xsl:param name="headings" required="yes"/>
  <xsl:param name="iterations" required="yes"/>
  <xsl:for-each select="$headings/headings/heading">
   <xsl:value-of select="concat('&#10;', isa:quotes(.))"/>
   <xsl:for-each select="1 to $iterations">
    <xsl:text>&#9;""</xsl:text>
   </xsl:for-each>
   <xsl:if test="$iterations = 0">
    <xsl:text>&#9;""</xsl:text>
   </xsl:if> 
  </xsl:for-each>
  
 </xsl:template>

 <xsl:template match="DESCRIPTOR/STUDY_TYPE">
  <xsl:text>"Study Design Type"&#9;</xsl:text>
  <xsl:value-of select="isa:quotes(@existing_study_type)"/>
  <xsl:text>&#10;</xsl:text>
 </xsl:template>

 <xsl:template match="STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(., 'pubmed')]">
  <xsl:text>&#9;</xsl:text>
  <xsl:value-of select="isa:quotes(following-sibling::ID/.)"/>
 </xsl:template>

 <xsl:template match="SAMPLE">
  <!-- Source Name -->
  <xsl:value-of select="isa:quotes-tab(@alias)"/>
  <!-- Characteristics[Primary Accession Number] -->
  <xsl:value-of select="isa:quotes-tab(@accession)"/>
  
  <xsl:value-of select="isa:quotes-tab(./SAMPLE_NAME/COMMON_NAME)"/>
  <xsl:value-of select="isa:quotes-tab(./SAMPLE_NAME/SCIENTIFIC_NAME)"/>
  <xsl:value-of select="isa:quotes-tab(./SAMPLE_NAME/TAXON_ID)"/>
  <xsl:value-of select="isa:quotes-tab(/DESCRIPTION)"/>
  
  <xsl:variable name="my-sample" select="./SAMPLE_ATTRIBUTES"/>
  <xsl:for-each select="$distinct-characteristic-terms/terms/term">
   <xsl:variable name="my-term" select="current()"/>
   <xsl:value-of select="if ($my-sample/SAMPLE_ATTRIBUTE/TAG[.=$my-term]) then $my-sample/SAMPLE_ATTRIBUTE/TAG[.=$my-term]/following-sibling::VALUE else ''"/>
<!--   <xsl:value-of select="isa:quotes(if ($my-sample/SAMPLE_ATTRIBUTE/TAG[.=$my-term]) then $my-sample/SAMPLE_ATTRIBUTE/TAG[.=$my-term]/following-sibling::VALUE else '')"/>-->
   <xsl:text>&#9;</xsl:text>
  </xsl:for-each>
 
  <xsl:value-of select="isa:quotes-tab(@accession)"/>
  <xsl:text>&#10;</xsl:text>
 </xsl:template>
 
 <xsl:template match="@alias | @accession | @refname">
  <xsl:value-of select="isa:quotes(.)"/>
 </xsl:template>
 
 <xsl:template match="COMMON_NAME | SCIENTIFIC_NAME | TAXON_ID">
  <xsl:value-of select="isa:quotes(.)"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESCRIPTION">
  <xsl:value-of select="isa:quotes(substring-before(.,'&#xa;'))"/>
 </xsl:template>
 
 <xsl:template match="EXPERIMENT">
 <!-- <xsl:apply-templates select="DESIGN/SAMPLE_DESCRIPTOR/@refname"/>-->
  <xsl:apply-templates select="DESIGN/SAMPLE_DESCRIPTOR/@accession"/>
  <xsl:text>&#9;</xsl:text>

  <xsl:text>"library preparation"&#9;</xsl:text>

  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY"/>
  
  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE"/>
  
  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SELECTION"/>
  
  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/SINGLE"/>
  
  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED"/>
  
  <xsl:apply-templates select="DESIGN/DESIGN_DESCRIPTION[contains(., 'target_taxon: ')]" mode="target-taxon"/>
 
  <xsl:apply-templates select="DESIGN/LIBRARY_DESCRIPTOR/TARGETED_LOCI/LOCUS"/>

  <xsl:apply-templates select="DESIGN/DESIGN_DESCRIPTION[contains(.,'target_subfragment: ')]" mode="target-subfragment"/>
  
  <xsl:apply-templates select="DESIGN/DESIGN_DESCRIPTION[contains(.,'mid: ')]" mode="mid"/>

  <xsl:apply-templates select="DESIGN/DESIGN_DESCRIPTION[contains(.,'pcr_primers: ')]" mode="pcr-primers"/>
  
  <xsl:apply-templates select="DESIGN/DESIGN_DESCRIPTION[contains(.,'pcr_cond: ')]" mode="pcr-cond"/>

  <xsl:apply-templates select="DESIGN/SAMPLE_DESCRIPTOR/@accession"/>
  <xsl:text>&#9;</xsl:text>

  <xsl:text>"nucleic acid sequencing"</xsl:text>
  <xsl:text>&#9;</xsl:text>

  <xsl:apply-templates select="DESIGN/SPOT_DESCRIPTOR"/>
  <xsl:text>&#9;</xsl:text>
   
  <xsl:apply-templates select="PLATFORM//INSTRUMENT_MODEL"/>

  <!-- a TAB as placeholder for Performer-->
  <xsl:text>""&#9;</xsl:text>
  <!-- another TAB as placeholder for Date-->
  <xsl:text>""&#9;</xsl:text>

  <xsl:apply-templates select="@accession"/>
  <xsl:text>&#9;</xsl:text>

  <xsl:choose>
   <xsl:when test="EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK">
    <xsl:apply-templates select="EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK/DB[contains(., 'ENA-FASTQ-FILES')]"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:text>&#9;</xsl:text>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:text>"md5"&#10;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY | DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE | DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SELECTION">
  <xsl:value-of select="isa:quotes(.)"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/SINGLE">
  <xsl:value-of select="isa:quotes('single')"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED">
   <xsl:value-of select="isa:quotes('paired')"/>
   <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/DESIGN_DESCRIPTION[contains(., 'target_taxon: ')]" mode="target-taxon">
  <xsl:value-of select="isa:quotes(substring-before(substring-after(.,'target_taxon: '),'target_gene:'))"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/LIBRARY_DESCRIPTOR/TARGETED_LOCI/LOCUS">
   <xsl:choose>
   <xsl:when test="./PROBE_SET/DB">
    <xsl:variable name="db" select="."></xsl:variable>
    <xsl:variable name="db_id" select="following-sibling::ID/."></xsl:variable>
    <xsl:value-of select="isa:quotes(concat(@locus_name,' (',$db,'.',$db_id,')'))"/>
    <xsl:text>&#9;</xsl:text>
  </xsl:when>
  <xsl:otherwise>
   <xsl:value-of select="isa:quotes(@locus_name)"/>
   <xsl:text>&#9;</xsl:text>
  </xsl:otherwise>
 </xsl:choose>
 </xsl:template>
 
 <xsl:template match="DESIGN/SPOT_DESCRIPTOR">
    <xsl:for-each select="./SPOT_DECODE_SPEC/READ_SPEC">
     <xsl:text>{</xsl:text> <xsl:value-of select="READ_INDEX/."/><xsl:text>;</xsl:text><xsl:value-of select="READ_CLASS/."/>
     <xsl:text>;</xsl:text><xsl:value-of select="READ_TYPE/."/><xsl:text>;</xsl:text><xsl:value-of select="BASE_COORD/."/><xsl:text>}</xsl:text>
    </xsl:for-each>
 </xsl:template>
 
 <xsl:template match="DESIGN/DESIGN_DESCRIPTION[contains(.,'target_subfragment: ')]" mode="target-subfragment">
  <xsl:value-of select="isa:quotes(substring-before(substring-after(.,'target_subfragment: '),'mid:'))"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/DESIGN_DESCRIPTION[contains(.,'mid: ')]" mode="mid">
  <xsl:value-of select="isa:quotes(substring-before(substring-after(.,'mid: '),'pcr_primers:'))"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/DESIGN_DESCRIPTION[contains(.,'pcr_primers: ')]" mode="pcr-primers">
  <xsl:value-of select="isa:quotes(substring-before(substring-after(.,'pcr_primers: '),'pcr_cond:'))"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="DESIGN/DESIGN_DESCRIPTION[contains(.,'pcr_cond: ')]" mode="pcr-cond">
  <xsl:value-of select="isa:quotes(substring-after(.,'pcr_cond: '))"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>
 
 <xsl:template match="PLATFORM//INSTRUMENT_MODEL">
  <xsl:value-of select="isa:quotes(.)"/>
  <xsl:text>&#9;</xsl:text>
 </xsl:template>

 <!-- If it is more than one line then we concatenate with a semi-colon -->
 <!-- http://www.ebi.ac.uk/ena/data/warehouse/filereport?accession=SRX201979&result=read_run&fields=fastq_ftp,fastq_md5 -->
 <xsl:template match="EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK/DB[contains(., 'ENA-FASTQ-FILES')]">
  <xsl:variable name="file" select="following-sibling::ID/."/>
  <xsl:if test="contains($file,'&amp;result=read_run&amp;fields=run_accession,fastq_ftp')">
   <xsl:variable name="base" select="substring-before($file,'&amp;result=read_run&amp;fields=run_accession,fastq_ftp')"/>
   <xsl:variable name="link" select="concat($base,'&amp;result=read_run&amp;fields=fastq_ftp,fastq_md5')"/>
   <xsl:variable name="parsedlink" select="unparsed-text($link)"/>
   
   <xsl:variable name="rawdatafile-structure">
    <xsl:call-template name="generate-rawdatafile-structure">
     <xsl:with-param name="parsedlink" select="$parsedlink"/>
    </xsl:call-template>
   </xsl:variable>
   
   <xsl:text>"</xsl:text>
   <xsl:for-each select="$rawdatafile-structure/links/link">
    <xsl:choose>
     <xsl:when test="following-sibling::node()">
      <xsl:value-of select="concat(@raw-data-file, ';')"/>  
     </xsl:when>
     <xsl:otherwise>
      <xsl:value-of select="@raw-data-file"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:for-each>
   <xsl:text>"</xsl:text>
   <xsl:text>&#9;</xsl:text>
   
   <xsl:text>"</xsl:text>
   <xsl:for-each select="$rawdatafile-structure/links/link">
    <xsl:choose>
     <xsl:when test="following-sibling::node()">
      <xsl:value-of select="concat(@file-checksum, ';')"/>  
     </xsl:when>
     <xsl:otherwise>
      <xsl:value-of select="@file-checksum"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:for-each>
   <xsl:text>"</xsl:text>
   <xsl:text>&#9;</xsl:text>
  </xsl:if>
   
 </xsl:template>
 
 <xsl:template match="text() | @*"/>  
</xsl:stylesheet>