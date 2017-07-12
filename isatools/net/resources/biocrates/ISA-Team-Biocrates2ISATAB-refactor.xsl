<?xml version="1.0" encoding="UTF-8"?>

<!--
***************************README********************************************** 
Date: 2014-10-15

Content: xsl stylesheet for Biocrates XML documents complying with schema xmlns="http://www.biocrates.com/metstat/result/xml_1.0"

Task: 
Creates 'ISA-Tab File' required for a submission to EMBL-EBI Metabolights repository [1] of Metabolomics Data
from Biocrates XML documents compliant to Biocrates xsd 1.0 [2].

Note: 
This is an XSL 2.0 transformation and requires Saxon-PE-9.5.1.5 to run.

Biocrates test files:
demo_data.xml
2014-07-15_Conc.xml

   
    
Author: Philippe Rocca-Serra
ORCID:
Affiliation: ISA Team, University of Oxford e-Reseach Centre
Email: philippe.rocca-serra@oerc.ox.ac.uk
WebSite: http://isa-tools.org
Code Repository: https://github.com/ISA-tools
    
Licence: CC-BY-SA 4.0
Version: rc1.0
DOI:
    
    
***************************README**********************************************
-->


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:isa="http://www.isa-tools.org/"
    exclude-result-prefixes="isa" xpath-default-namespace="http://www.biocrates.com/metstat/result/xml_1.0"> 
 
    <xsl:import href="../sra/isa-functions.xsl"/> 
   
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:strip-space elements="*"/>
    
    <!-- declaring all keys for lookups -->
    <xsl:key name="metabolitelookupid"  match="metabolite"  use="@identifier"/>
    <xsl:key name="metabolite_by_platebarcode" match="metabolitePlateInfo" use="concat(@plateBarcode, ancestor::metabolite[1]/@identifier)"/>
    <xsl:key name="platebarcode_by_metabolite" match="metabolite" use="child::metabolitePlateInfo[1]/@plateBarcode"/>
    <xsl:key name="samplelookupid"  match="sample"  use="@identifier"/>
    <xsl:key name="samplefeaturelookupid"  match="data/plate/well/sample/sampleInfoExport"  use="@feature"/>
    <xsl:key name="samplevaluelookupid"  match="//data/plate/well/sample/sampleInfoExport"  use="@value"/>
    <xsl:key name="measure_by_metabolite" match="measure" use="@metabolite"/>   
    <xsl:key name="plateInfo" match="plate" use="@plateBarcode"/>   
    <xsl:key name="run_polarity" match="injection" use="@polarity"/>   
   
    <xsl:key name="injection" match="injection" use="@polarity"/>
    <xsl:key name="platebarcodelookupid" match="plate" use="@plateBarcode"/>

    <!-- keys and variables needed for the muenchian transform/muenchian grouping --> 
    <xsl:key name="feature-by-sample" match="sampleInfoExport" use="ancestor::sample[1]/@identifier"/>
    <xsl:key name="sampleinfo-features" match="sampleInfoExport" use="@feature"/>
    <xsl:variable name="sampleinfo-features" select="/data/sample/sampleInfoExport[generate-id()=generate-id(key('sampleinfo-features', @feature)[1])]/@feature"/> 
    
    <!--Note: muenchian transform 
    <xsl:variable name="sampleinfoexport" select="key('feature-by-sample', @identifier)"/>
    <xsl:for-each select="$sampleinfo-features">              
        <xsl:value-of select="$sampleinfoexport[@feature = current()]/@value"/><xsl:text>&#9;</xsl:text>
    </xsl:for-each> -->
    
    <xsl:key name="measure-by-injection" match="measure" use="ancestor::injection[1]/@rawDataFileName"/>
    <xsl:key name="injection-measures" match="measure" use="@metabolite"/>
    <xsl:variable name="injection-measures" select="/data/plate/well/injection/measure[generate-id()=generate-id(key('injection-measures', @metabolite)[1])]/@metabolite"/>
    <xsl:key name="run-metabolites" match="measure" use="@metabolite"/>
    <xsl:key name="usedOPlist" match="plate" use="@usedOP"/>

    <!-- declaring variable for relevant processing templates -->
    <xsl:variable name="positiveModeCount" select="data/plate/well/injection[lower-case(@polarity)='positive']"/>
    <xsl:variable name="negativeModeCount" select="data/plate/well/injection[lower-case(@polarity)='negative']"/>
    <!-- a variable to hold the maximum number of 'sampleInfoExport' associated to any given 'sample' -->
    <!-- $max is used for padding empty cell in the s_study.txt as some 'sample' have no such attributes -->
    <xsl:variable name="max" select="max(data/plate/well/sample/count(sampleInfoExport))" as="xs:integer"/> 
    
    <xsl:template match="/">
     <xsl:apply-templates/>
    </xsl:template>      
    
<xsl:template match="data">
    <xsl:variable name="investigationfile" select="concat('output/',data,'i_inv_biocrates.txt')[normalize-space()]"></xsl:variable>
    <xsl:value-of select="$investigationfile[normalize-space()]"/>     
    <!-- this is used to generated separate output files -->
    <xsl:result-document href="{$investigationfile}">
        <xsl:copy-of select=".[normalize-space()]"/>
        <xsl:call-template name="generate-header-comments"/>
        <!-- creates ISA i_investigation file -->
        <xsl:call-template name="generate-ontology-section"/>
        <xsl:call-template name="generate-investigation-section"/>
        
        <!-- TODO: Put the "STUDY" section in its own template name for code readabiltity -->
<xsl:text>&#10;"STUDY"&#10;</xsl:text>
        <xsl:value-of select="isa:single-name-value('Study Identifier', /data/project[1]/@identifier)"/>
        <xsl:value-of select="isa:single-name-value('Study Title', /data/project[1]/@ProjectName)"/>
        <xsl:value-of select="isa:single-name-value('Study Submission Date', '')"/>
        <xsl:value-of select="isa:single-name-value('Study Public Release Date', '')"/>
        <xsl:value-of select="isa:single-name-value('Study Description', '')"/>
        <xsl:value-of select="isa:single-name-value('Study File Name', 's_study_biocrates.txt')"/>
    
<xsl:text>"STUDY DESIGN DESCRIPTORS"
"Study Design Type"
"Study Design Type Term Accession Number"
"Study Design Type Term Source REF"
"STUDY PUBLICATIONS"
"Study PubMed ID"
"Study Publication DOI"
"Study Publication Author List"
"Study Publication Title"
"Study Publication Status"
"Study Publication Status Term Accession Number"
"Study Publication Status Term Source REF"
"STUDY FACTORS"
"Study Factor Name"
"Study Factor Type"
"Study Factor Type Term Accession Number"
"Study Factor Type Term Source REF"
"STUDY ASSAYS"
"Study Assay Measurement Type"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:value-of select="if (count($positiveModeCount) > 0) then concat(isa:quotes('metabolite profiling'), '&#9;') else ''"/>
    <xsl:value-of select="if (count($negativeModeCount) > 0) then concat(isa:quotes('metabolite profiling'), '&#9;') else ''"/>     
<xsl:text>
"Study Assay Measurement Type Term Source REF"</xsl:text>
<xsl:text>&#9;</xsl:text>
    <xsl:value-of select="if (count($positiveModeCount) > 0) then concat(isa:quotes('OBI'), '&#9;') else ''"/>
    <xsl:value-of select="if (count($negativeModeCount) > 0) then concat(isa:quotes('OBI'), '&#9;') else ''"/>         
<xsl:text>
"Study Assay Measurement Type Term Accession Number"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:value-of select="if (count($positiveModeCount) > 0) then concat(isa:quotes('http://purl.obolibrary.org/obo/OBI_0000366'), '&#9;') else ''"/>
    <xsl:value-of select="if (count($negativeModeCount) > 0) then concat(isa:quotes('http://purl.obolibrary.org/obo/OBI_0000366'), '&#9;') else ''"/>             
<xsl:text>
"Study Assay Technology Type"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">     
        <xsl:text>"mass spectrometry"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"mass spectrometry"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if> 
<xsl:text>
"Study Assay Technology Type Term Source REF"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">      
        <xsl:text>"OBI"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"OBI"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>    
<xsl:text>
"Study Assay Technology Type Term Accession Number"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">       
        <xsl:text>"http://purl.obolibrary.org/obo/OBI_0000470"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"http://purl.obolibrary.org/obo/OBI_0000470"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>      
<xsl:text>
"Study Assay Technology Platform"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">        
        <xsl:text>"Biocrates"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"Biocrates"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>      
<xsl:text>
"Study Assay File Name"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <!-- TODO: Tidy up (same as above) -->    
    <xsl:if test="count($positiveModeCount) > 0">       
        <xsl:text>"a_biocrates_assay_positive_mode.txt"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"a_biocrates_assay_negative_mode.txt"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if> 
<xsl:text>
</xsl:text>
<xsl:text>"STUDY PROTOCOLS"
"Study Protocol Name"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:text>"sample collection"&#9;</xsl:text>
    <xsl:text>"extraction/derivatization"&#9;</xsl:text>
        
        <xsl:for-each select="/data/plate[generate-id(.)=generate-id(key('usedOPlist', @usedOP)[1])]/@usedOP">              
            <xsl:value-of select="isa:quotes(.)"/>  <xsl:text>&#9;</xsl:text>      
        </xsl:for-each> 
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">       
        <xsl:text>"MS acquisition in positive mode"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <!-- TODO: Tidy up (same as above) -->    
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"MS acquisition in negative mode"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if> 
    <xsl:text>"biocrates analysis"&#9;</xsl:text>
"Study Protocol Type"<xsl:text>&#9;</xsl:text>
    <xsl:text>"specimen collection"&#9;</xsl:text>
    <xsl:text>"material separation"&#9;</xsl:text>
        <xsl:for-each select="/data/plate[generate-id(.)=generate-id(key('usedOPlist', @usedOP)[1])]/@usedOP">              
            <xsl:text>"sample preparation for assay"&#9;</xsl:text>        
        </xsl:for-each>
    <!-- TODO: Tidy up (same as above) -->
    <xsl:if test="count($positiveModeCount) > 0">       
        <xsl:text>"data collection"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if>   
    <!-- TODO: Tidy up (same as above) -->    
    <xsl:if test="count($negativeModeCount) > 0">
        <xsl:text>"data collection"</xsl:text>
        <xsl:text>&#9;</xsl:text>
    </xsl:if> 
    <xsl:text>"data transformation"&#9;</xsl:text>
<xsl:text>    
"Study Protocol Type Term Accession Number"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:text>"http://purl.obolibrary.org/obo/OBI_0000659"&#9;</xsl:text>
    <xsl:text>"http://purl.obolibrary.org/obo/OBI_0302884"&#9;</xsl:text>
    <xsl:for-each select="/data/plate[generate-id(.)=generate-id(key('usedOPlist', @usedOP)[1])]/@usedOP">              
            <xsl:text>"http://purl.obolibrary.org/obo/OBI_0000073"&#9;</xsl:text>        
    </xsl:for-each>
        <!-- TODO: Tidy up (same as above) -->
        <xsl:if test="count($positiveModeCount) > 0">       
            <xsl:text>"http://purl.obolibrary.org/obo/OBI_0600013"</xsl:text>
            <xsl:text>&#9;</xsl:text>
        </xsl:if>
        <!-- TODO: Tidy up (same as above) -->
        <xsl:if test="count($negativeModeCount) > 0">
            <xsl:text>"http://purl.obolibrary.org/obo/OBI_0600013"</xsl:text>
            <xsl:text>&#9;</xsl:text>
        </xsl:if> 
        <xsl:text>"http://purl.obolibrary.org/obo/OBI_0200000"&#9;</xsl:text>
<xsl:text>        
"Study Protocol Type Term Source REF"</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:text>"OBI"&#9;</xsl:text>
    <xsl:text>"OBI"&#9;</xsl:text>
    <xsl:for-each select="/data/plate[generate-id(.)=generate-id(key('usedOPlist', @usedOP)[1])]/@usedOP">              
            <xsl:text>"OBI"&#9;</xsl:text>        
    </xsl:for-each>
        <!-- TODO: Tidy up (same as above) -->
        <xsl:if test="count($positiveModeCount) > 0">       
            <xsl:text>"OBI"</xsl:text>
            <xsl:text>&#9;</xsl:text>
        </xsl:if>
        <!-- TODO: Tidy up (same as above) -->
        <xsl:if test="count($negativeModeCount) > 0">
            <xsl:text>"OBI"</xsl:text>
            <xsl:text>&#9;</xsl:text>
        </xsl:if> 
        <xsl:text>"OBI"&#9;</xsl:text>
<xsl:text>
"Study Protocol Description"
"Study Protocol URI"
"Study Protocol Version"
"Study Protocol Parameters Name"
"Study Protocol Parameters Name Term Accession Number"
"Study Protocol Parameters Name Term Source REF"
"Study Protocol Components Name"
"Study Protocol Components Type"
"Study Protocol Components Type Term Accession Number"
"Study Protocol Components Type Term Source REF"
"STUDY CONTACTS"  
"Study Person Last Name"</xsl:text> 
        <xsl:apply-templates select="contact" mode="lastname"/>        
<xsl:text>
"Study Person First Name"</xsl:text>
        <xsl:apply-templates select="contact" mode="firstname"/>
 <xsl:text>       
"Study Person Mid Initials"
"Study Person Email"</xsl:text> 
        <xsl:apply-templates select="contact" mode="email"/>
 <xsl:text> 
"Study Person Phone"</xsl:text> 
        <xsl:apply-templates select="contact" mode="phone"/>
 <xsl:text> 
"Study Person Fax"
"Study Person Address"</xsl:text> 
    <xsl:apply-templates select="contact" mode="address"/>
 <xsl:text> 
"Study Person Affiliation"</xsl:text> 
        <xsl:apply-templates select="contact" mode="affiliation"/>        
 <xsl:text> 
"Study Person Roles"
"Study Person Roles Term Accession Number"
"Study Person Roles Term Source REF"
</xsl:text>

</xsl:result-document>
    
    <!-- template invocation to create ISA s_study table -->
    <xsl:call-template name="study"/>
<xsl:text>
</xsl:text>
    <!-- template invocation to create ISA a_assay table for positive mode acquisition -->
    <xsl:call-template name="assay-positiveMode"/>
<xsl:text>
</xsl:text>
    <!-- template invocation to create ISA a_assay table for negative mode acquisition-->
    <xsl:call-template name="assay-negativeMode"/>
    <xsl:text>
</xsl:text>

    <!-- template invocation to create ISA Derived Data Matrix 
    <xsl:call-template name="metabolite_desc_posi"/>
    <xsl:call-template name="metabolite_desc_nega"/>  --> 

</xsl:template>
    
    <xsl:template name="generate-header-comments">
        <!--BEGIN a block of commented lines to record some provenance information -->
        <!-- this information may be used by Metabolights -->
        <xsl:value-of select="isa:single-name-value('#BIOCRATES software version:', @swVersion)"/>
        <xsl:value-of select="isa:single-name-value('#BIOCRATES document filename:', base-uri())"/>
        <xsl:value-of select="isa:single-name-value('#BIOCRATES export date:', substring-before(@dateExport,'T'))"/>
        <xsl:text>"#ISATab transformation by: Isatools-Biocrates2ISATab.xsl"</xsl:text>
        <!-- END of the comment block -->
    </xsl:template>
    
    <xsl:template name="generate-ontology-section">
        <xsl:text>&#10;"ONTOLOGY SOURCE REFERENCE"&#10;</xsl:text>
        <xsl:text>"Term Source Name"&#9;"OBI"&#9;"PSI-MS"&#9;"UBERON"&#9;"NCBITax"&#10;</xsl:text> 
        <xsl:text>"Term Source File"&#9;"http://purl.org/obo/obi.owl"&#9;"http://psi-ms.sf.net"&#9;"http://purl.org/obo/uberon.owl"&#9;"http://purl.org/obo/NCBITax.owl"&#10;</xsl:text>
        <xsl:text>"Term Source Version"&#9;"1"&#9;"1"&#9;"1"&#9;"1"&#10;</xsl:text>
        <xsl:text>"Term Source Description"&#9;"The Ontology for Biomedical Investigation"&#9;"PSI Mass Spectrometry"&#9;"Uber-anatomy ontology"&#9;"NCBI Taxonomy"</xsl:text>        
    </xsl:template>
    
    <xsl:template name="generate-investigation-section">
        <!-- TODO: Need to add the blank quotes if there is no values. For example: "Investigation Identifier:" "".
            Perhaps this can be done using <xsl:value-of select="isa:single-name-value('Investigation Identifier', '')"/>
        -->
        <xsl:text>
"INVESTIGATION"
"Investigation Identifier"
"Investigation Title"
"Investigation Description"
"Investigation Submission Date"
"Investigation Public Release Date"
"INVESTIGATION PUBLICATIONS"
"Investigation PubMed ID"
"Investigation Publication DOI"
"Investigation Publication Author List"
"Investigation Publication Title"
"Investigation Publication Status"
"Investigation Publication Status Term Accession Number"
"Investigation Publication Status Term Source REF"
"INVESTIGATION CONTACTS"
"Investigation Person Last Name"
"Investigation Person First Name"
"Investigation Person Mid Initials"
"Investigation Person Email"
"Investigation Person Phone"
"Investigation Person Fax"
"Investigation Person Address"
"Investigation Person Affiliation"
"Investigation Person Roles"
"Investigation Person Roles Term Accession Number"
"Investigation Person Roles Term Source REF"</xsl:text>
    </xsl:template>

<xsl:template  match="contact" mode="lastname">
    <xsl:value-of select="if (@ContactPerson != '') then concat('&#9;',isa:quotes(substring-before(@ContactPerson,' '))) else (concat('&#9;&quot;','&quot;'))"/>
</xsl:template>
    
<xsl:template  match="contact" mode="firstname">
    <xsl:value-of select="if (@ContactPerson != '') then concat('&#9;',isa:quotes(substring-after(@ContactPerson,' '))) else (concat('&#9;&quot;','&quot;'))"/>
</xsl:template>

<xsl:template  match="contact" mode="affiliation">
    <xsl:value-of select="if (@CompanyName != '') then concat('&#9;',isa:quotes(@CompanyName)) else (concat('&#9;&quot;','&quot;'))"/>
</xsl:template>
    
<xsl:template match="contact" mode="address" >
    <xsl:value-of select="concat('&#9;',isa:quotes(concat(@Street,', ',@City,', ',@ZipCode,', ',@Country)))"/>  
</xsl:template>

<xsl:template match="contact" mode="phone" >
    <xsl:value-of select="if (@Phone != '') then concat('&#9;',isa:quotes(@Phone)) else (concat('&#9;&quot;','&quot;'))"/>  
</xsl:template>
    
<xsl:template match="contact" mode="email" >
    <xsl:value-of select="if (@Email != '') then concat('&#9;',isa:quotes(@Email)) else (concat('&#9;&quot;','&quot;'))"/>  
</xsl:template> 
    
    

<!-- ****************************************************** -->
<xsl:template match="metabolite" name="metabolite_desc_posi">

    <xsl:variable name="datafile" select="concat('output/',data,'maf-positive.txt')[normalize-space()]"></xsl:variable>
    <xsl:value-of select="$datafile[normalize-space()]" /> 
    <xsl:result-document href="{$datafile}">
        <xsl:copy-of select=".[normalize-space()]"></xsl:copy-of>  

        <!-- formatting follows MzTAB & EMBL-EBI Metabolights Metabolite Assignment File specifications -->
        <xsl:text>database_identifier</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>chemical_formula</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>smiles</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>inchi</xsl:text><xsl:text>&#9;</xsl:text> 
        <xsl:text>metabolite identification</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Comment[chemical class]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Comment[protocol]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Comment[internal standard]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Comment[scan type]</xsl:text><xsl:text>&#9;</xsl:text> 
        
        <!-- creates a set of Quantitation Type headers for each of the samples -->
        <!-- TODO: I think this for-each can be replace by xsl:template -->
        <xsl:for-each select="//injection[lower-case(@polarity) ='positive']">
            
            <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
            <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::well/@sample !=''">
                    <xsl:choose>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                        </xsl:when>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                    <!-- <xsl:text>none reported</xsl:text> -->
                </xsl:otherwise>
            </xsl:choose> 
            <xsl:text>[signal intensity]&#9;</xsl:text>
            <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
            <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::well/@sample !=''">
                    <xsl:choose>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                        </xsl:when>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                    <!-- <xsl:text>none reported</xsl:text> --> 
                </xsl:otherwise>
            </xsl:choose> 
            <xsl:text>[concentration(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
            <xsl:text>)]&#9;</xsl:text>
            
            <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
            <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::well/@sample !=''">
                    <xsl:choose>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                        </xsl:when>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                    <!-- <xsl:text>none reported</xsl:text> --> 
                </xsl:otherwise>
            </xsl:choose> 
            <xsl:text>[signal intensity Internal Std]&#9;</xsl:text>
            
            <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
            <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::well/@sample !=''">
                    <xsl:choose>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                        </xsl:when>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                    <!-- <xsl:text>none reported</xsl:text> --> 
                </xsl:otherwise>
            </xsl:choose> 
            <xsl:text>[concentration Internal Std(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
            <xsl:text>)]&#9;</xsl:text>
            
            <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
            <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
            <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::well/@sample !=''">
                    <xsl:choose>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                        </xsl:when>
                        <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                    <!-- <xsl:text>none reported</xsl:text> -->
                </xsl:otherwise>
            </xsl:choose> 
            <xsl:text>[status]&#9;</xsl:text>   
            
        </xsl:for-each>    
        <xsl:text>
</xsl:text> 
        
        <!-- now add actual measurements for each metabolite for the relevant runs -->
        <xsl:for-each select="//measure[generate-id() = generate-id(key('measure_by_metabolite', @metabolite)[1])]">
            <xsl:if test="ancestor::injection[lower-case(@polarity) ='positive']" >
                
                <xsl:choose>
                    <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@CHEBI !=''">
                        <xsl:text>CHEBI:</xsl:text>
                        <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@CHEBI"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text>&#9;</xsl:text>
                <xsl:choose>
                    <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@IUPAC !=''">
                        <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@IUPAC"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text>&#9;</xsl:text>
                <xsl:choose>
                    <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@SMILES!=''">
                        <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@SMILES"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                <!-- <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@HMDB"/> --> 
                
                <xsl:text>&#9;</xsl:text>
                <xsl:choose>
                    <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@INCHI!=''">
                        <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@INCHI"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                
                <xsl:text>&#9;</xsl:text>
                
                <xsl:choose>
                    <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@molecule!=''">                          
                        <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@molecule"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="@metabolite"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@metaboliteClass"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@protocol"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@internalStd"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@scanType"/>
                <xsl:text>&#9;</xsl:text> 
                <xsl:for-each select="key('measure_by_metabolite', @metabolite)">
                    <xsl:value-of select="@intensity"/>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:value-of select="@concentration"/>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:value-of select="@intensityIstd"/>
                    <xsl:text>&#9;</xsl:text>    
                    <xsl:value-of select="@concentrationIstd"/> 
                    <xsl:text>&#9;</xsl:text>   
                    <xsl:value-of select="@status"/>
                    <xsl:text>&#9;</xsl:text>
                </xsl:for-each>
                <xsl:text>
</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:result-document>
</xsl:template> 


<!--    <xsl:text>Metabolite ID</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>Chemical Class</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>protocol</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>internal standard</xsl:text><xsl:text>&#9;</xsl:text>
       
    <xsl:for-each select="//run">
        <xsl:if test="contains(lower-case(@polarity),'posi')">
        <xsl:text>intensity[</xsl:text> 
        <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@runNumber"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@injectionNumber"/>
        <xsl:text>]&#9;</xsl:text>
        <xsl:text>concentration(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
        <xsl:text>)[</xsl:text>
        <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@runNumber"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@injectionNumber"/>
        <xsl:text>]&#9;</xsl:text>
        <xsl:text>intensity Internal Std[</xsl:text>
        <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@runNumber"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@injectionNumber"/>
        <xsl:text>]&#9;</xsl:text>
        <xsl:text>concentration Internal Std(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
        <xsl:text>)[</xsl:text>
        <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@runNumber"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@injectionNumber"/>
        <xsl:text>]&#9;</xsl:text>
        <xsl:text>status[</xsl:text>       
        <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@runNumber"/><xsl:text>_</xsl:text>
        <xsl:value-of select="@injectionNumber"/>
        <xsl:text>]&#9;</xsl:text>
        <xsl:value-of select="@injectionTime"/><xsl:text>_</xsl:text>
        </xsl:if>
    </xsl:for-each>    
<xsl:text>
</xsl:text> 
    
    <xsl:for-each select="//measure[generate-id() = generate-id(key('measure_by_metabolite', @metabolite)[1])]">
        <xsl:if test="ancestor::run[lower-case(@polarity) ='positive']" >
        <xsl:value-of select="@metabolite"/>
        <xsl:text>&#9;</xsl:text>
        <xsl:value-of select="key('metabolitelookupid',@metabolite)/@metaboliteClass"/>
        <xsl:text>&#9;</xsl:text>
        <xsl:value-of select="key('metabolitelookupid',@metabolite)/@protocol"/>
        <xsl:text>&#9;</xsl:text>
        <xsl:value-of select="key('metabolitelookupid',@metabolite)/@internalStd"/>
        <xsl:text>&#9;</xsl:text>        
        <xsl:for-each select="key('measure_by_metabolite', @metabolite)">
            <xsl:value-of select="@intensity"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:value-of select="@concentration"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:value-of select="@intensityIstd"/>
            <xsl:text>&#9;</xsl:text>    
            <xsl:value-of select="@concentrationIstd"/> 
            <xsl:text>&#9;</xsl:text>   
            <xsl:value-of select="@status"/>
            <xsl:text>&#9;</xsl:text>
        </xsl:for-each>
<xsl:text>
</xsl:text>
        </xsl:if>
    </xsl:for-each>
    </xsl:result-document>
</xsl:template> -->


<!-- ****************************************************** -->
<xsl:template match="metabolite" name="metabolite_desc_nega">
    <xsl:variable name="usedOP" select="@usedOP"/>
        <xsl:variable name="datafile" select="concat('output/',$usedOP,'-maf-negative.txt')[normalize-space()]"></xsl:variable>
        <xsl:value-of select="$datafile[normalize-space()]" /> 
        <xsl:result-document href="{$datafile}">
            <xsl:copy-of select=".[normalize-space()]"/>
            
            <!-- formatting follows MzTAB & EMBL-EBI Metabolights Metabolite Assignment File specifications -->
            <xsl:text>database_identifier</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>chemical_formula</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>smiles</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>inchi</xsl:text><xsl:text>&#9;</xsl:text> 
            <xsl:text>metabolite identification</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>Comment[chemical class]</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>Comment[protocol]</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>Comment[internal standard]</xsl:text><xsl:text>&#9;</xsl:text>
            <xsl:text>Comment[scan type]</xsl:text><xsl:text>&#9;</xsl:text> 
            
            <!-- creates a set of Quantitation Type headers for each of the samples -->
            <!-- TODO: I think this for-each can be replaced by an xsl:template -->
            <xsl:for-each select="//injection[lower-case(@polarity) ='negative']">
                    
               <!-- [SOP][_][PlateBarcode][_][WellPosition][_][AcquisitionMethodIndex][_][RunNumber][_][InjectionNr][_][SampleType ID][_][SampleBarcode][_][sample identifier if setting is set][.wiff] -->             
                <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
                <xsl:choose>
                    <xsl:when test="parent::well/@sample !=''">
                        <xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                    </xsl:otherwise>
                </xsl:choose>               
                <xsl:text>[signal intensity]&#9;</xsl:text>
                
                <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
                <xsl:choose>
                    <xsl:when test="parent::well/@sample !=''">
                        <xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                    </xsl:otherwise>
                </xsl:choose> 
                <xsl:text>[concentration(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
                <xsl:text>)]&#9;</xsl:text>

                <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
                <xsl:choose>
                    <xsl:when test="parent::well/@sample !=''">
                        <xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                    </xsl:otherwise>
                </xsl:choose>  
                <xsl:text>[signal intensity Internal Std]&#9;</xsl:text>

                <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
                <xsl:choose>
                    <xsl:when test="parent::well/@sample !=''">
                        <xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                    </xsl:otherwise>
                </xsl:choose> 
                    <xsl:text>[concentration Internal Std(</xsl:text><xsl:value-of select="//data/@concentrationUnit"/>
                    <xsl:text>)]&#9;</xsl:text>
       
                <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::well/@wellPosition"/><xsl:text>_</xsl:text>
                <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>
                <xsl:choose>
                    <xsl:when test="parent::well/@sample !=''">
                        <xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                    </xsl:otherwise>
                </xsl:choose>  
                    <xsl:text>[status]&#9;</xsl:text>   
                
            </xsl:for-each>    
            <xsl:text>
</xsl:text> 
   
            <!-- now add actual measurements for each metabolite for the relevant runs -->
            <xsl:for-each select="//measure[generate-id() = generate-id(key('measure_by_metabolite', @metabolite)[1])]">
                <xsl:if test="ancestor::injection[lower-case(@polarity) ='negative']" >
                   
                    <xsl:choose>
                        <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@CHEBI !=''">
                    <xsl:text>CHEBI:</xsl:text>
                    <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@CHEBI"/>
                    </xsl:when>
                        <xsl:otherwise>
                        <xsl:text>not available</xsl:text>
                    </xsl:otherwise>
                    </xsl:choose>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:choose>
                        <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@IUPAC !=''">
                            <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@IUPAC"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>not available</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:choose>
                        <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@SMILES!=''">
                            <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@SMILES"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>not available</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                    <!-- <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@HMDB"/> --> 

                    <xsl:text>&#9;</xsl:text>
                    <xsl:choose>
                        <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@INCHI!=''">
                            <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@INCHI"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>not available</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                    
                    <xsl:text>&#9;</xsl:text>
                    
                    <xsl:choose>
                        <xsl:when test="key('metabolitelookupid',@metabolite)/BioID[1]/@molecule!=''">                          
                            <xsl:value-of select="key('metabolitelookupid',@metabolite)/BioID[1]/@molecule"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>not available</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>

                    <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="@metabolite"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@metaboliteClass"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@protocol"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@internalStd"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="key('metabolitelookupid',@metabolite)/@scanType"/>
                <xsl:text>&#9;</xsl:text> 
                <xsl:for-each select="key('measure_by_metabolite', @metabolite)">
                    <xsl:value-of select="@intensity"/>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:value-of select="@concentration"/>
                    <xsl:text>&#9;</xsl:text>
                    <xsl:value-of select="@intensityIstd"/>
                    <xsl:text>&#9;</xsl:text>    
                    <xsl:value-of select="@concentrationIstd"/> 
                    <xsl:text>&#9;</xsl:text>   
                    <xsl:value-of select="@status"/>
                    <xsl:text>&#9;</xsl:text>
                </xsl:for-each>
<xsl:text>
</xsl:text>
                </xsl:if>
            </xsl:for-each>
        </xsl:result-document>
</xsl:template> 

<xsl:template match="well">
    <!-- TODO: I think the xsl:text and xsl:value here can be tidied up -->
    <xsl:text>
    </xsl:text>     
    <xsl:text>well:</xsl:text>
    <xsl:text>&#9;</xsl:text>
    <xsl:value-of select="@wellPosition"/>
    <xsl:text>&#9;</xsl:text>
    <xsl:apply-templates select="injection"/>     
</xsl:template>



<!-- ****************************************************** -->
<!--     template to create ISA s_study table               -->
    <xsl:template name="study" match="sample"  priority="1">
    
    <xsl:variable name="studyfile" select="concat('output/',data,'s_study_biocrates.txt')[normalize-space()]"/>
    <xsl:value-of select="$studyfile[normalize-space()]" /> 
    <xsl:result-document href="{$studyfile}">
        <xsl:copy-of select=".[normalize-space()]"></xsl:copy-of>
    
    <xsl:text>"Source Name"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Characteristics[barcode identifier]"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Characteristics[material role]"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Characteristics[chemical compound]"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Characteristics[Organism]"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Term Source REF"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Term Accession Number"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Characteristics[Organism part]"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Term Source REF"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Term Accession Number"</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:for-each select="/data/sample/sampleInfoExport[generate-id(.)=generate-id(key('sampleinfo-features', @feature)[1])]/@feature">    
            <!-- <xsl:sort/> -->     
            <xsl:text>"Characteristics[</xsl:text>
            <xsl:choose>
                <xsl:when test="contains(.,'(') or contains(.,')')">
                    <xsl:variable name="this" select="translate(.,'(','-')"/>
                    <xsl:value-of select="translate($this,')','')"/>
                </xsl:when>
                <xsl:otherwise>
                <xsl:value-of select="."/>
                    </xsl:otherwise>   
            </xsl:choose>
            <xsl:text>]"&#9;</xsl:text>  
     </xsl:for-each>              
    <xsl:text>"Protocol REF"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Date"</xsl:text><xsl:text>&#9;</xsl:text> 
 <!--   <xsl:text>Parameter Value[plate info]</xsl:text><xsl:text>&#9;</xsl:text> 
    <xsl:text>Parameter Value[well position]</xsl:text><xsl:text>&#9;</xsl:text>  -->
    <xsl:text>"Sample Name"</xsl:text><xsl:text>&#9;</xsl:text>
    <xsl:text>"Material Type"</xsl:text><xsl:text>&#9;</xsl:text>
        
    <xsl:apply-templates select="sample" mode="sample_record"/>
        
    </xsl:result-document>
 </xsl:template>
    
<xsl:template match="sample" mode="sample_record">  
<xsl:text>
</xsl:text>
         <xsl:choose>
             <xsl:when test="@sampleType !='SAMPLE'">
                 <xsl:call-template name="sample_material_name"/>                
                 <xsl:text>&#9;</xsl:text>               
                 <xsl:value-of select="if (@barcode != '') then isa:quotes(@barcode) else concat('&#9;&quot;','none reported','&quot;&#9;')"/>
                 <xsl:text>&#9;</xsl:text>
                 <xsl:call-template name="sampleType"/>                 
                 <xsl:text>&#9;</xsl:text>
                 <xsl:value-of select="isa:quotes(@Material)"/>
                 <xsl:text>&#9;</xsl:text>
                 <xsl:text>"not applicable"</xsl:text>
                 <xsl:text>&#9;&#9;&#9;</xsl:text>
                 <xsl:text>"not applicable"</xsl:text>
                 <xsl:text>&#9;&#9;&#9;</xsl:text>
             </xsl:when>
             <xsl:otherwise>
                 <xsl:call-template name="sample_material_name"/>        
                 <xsl:text>&#9;</xsl:text>
                 <xsl:value-of select="if (@barcode != '') then isa:quotes(@barcode) else concat('&#9;&quot;','none reported','&quot;&#9;')"/>
                 <xsl:text>&#9;</xsl:text>   
                 <xsl:text>"specimen"</xsl:text>
                 <xsl:text>&#9;</xsl:text>
                 <xsl:text>"not applicable"</xsl:text>
              
                 
                 <xsl:variable name="species_var" select="@Species"></xsl:variable>
                 
                 <xsl:call-template name="mapping-replacement">
                          <xsl:with-param name="mapping-param" select="$species_var"/>
                 </xsl:call-template>
               
                 
                 <xsl:variable name="material_var" select="@Material"></xsl:variable>
                 
                 <xsl:call-template name="mapping-replacement">
                     <xsl:with-param name="mapping-param" select="$material_var"/>
                 </xsl:call-template>
                 
                 <xsl:text>&#9;</xsl:text>             
             </xsl:otherwise>
         </xsl:choose>
          
         
        <!--Note: muenchian transform -->
        <xsl:variable name="sampleinfoexport" select="key('feature-by-sample', @identifier)"/>
        <xsl:for-each select="$sampleinfo-features">              
            <xsl:value-of select="concat('&quot;', $sampleinfoexport[@feature = current()]/@value, ' &quot;')"/><xsl:text>&#9;</xsl:text>
        </xsl:for-each>   
                  
         <xsl:text>"sample collection"</xsl:text>
         <xsl:text>&#9;</xsl:text>    
         <xsl:value-of select="if (@collectionDate != '') then isa:quotes(substring-before(@collectionDate,'T')) else concat('&quot;','&quot;')"/>
         <xsl:text>&#9;</xsl:text>
    
        <xsl:call-template name="sample_material_name"/>
    
        <xsl:text>&#9;</xsl:text>  
        <xsl:call-template name="sampleType"/>  
<!--        <xsl:value-of select="isa:quotes(lower-case(@sampleType))"/>-->
</xsl:template>   
    
<xsl:template name="mapping-replacement">
    <xsl:param name="mapping-param"/>
    <xsl:variable name="mapping" select="document('ISA-Team-Biocrates2ISA-CV-mapping.xml')"/>
<!--    <xsl:text>&#9;</xsl:text><xsl:value-of select="$species_param"/>
    <xsl:text>&#9;</xsl:text><xsl:value-of select="$mapping/root/mapping-replacement/element[1]/@biocrateslabel"/>-->
<!--    <xsl:value-of select="if ($mapping/root/mapping-replacement/element[@biocrateslabel=$species_param]) then concat('&#9;&quot;',$mapping/root/mapping-replacement/element/@ontoterm, '&quot;') else concat('&#9;&quot;','other-species','&quot;&#9;')"/>-->
    
    <!-- TODO: I think that this can be done by not using an xsl:for-each -->
    <xsl:for-each select="$mapping/root/mapping-replacement/element">
        <xsl:if test="@biocrateslabel=$mapping-param">
            <xsl:value-of select="concat('&#9;&quot;',@ontoterm, '&quot;','&#9;&quot;',@ontosource, '&quot;&#9;&quot;',@url,'&quot;')"/>
        </xsl:if>           
    </xsl:for-each>    
</xsl:template>

<xsl:template name="sample_material_name" match="sample">
    <xsl:choose>
        <xsl:when test="@SampleIdentifier !=''">
            <xsl:choose>
                <xsl:when test="@SampleIdentifier !=''">
                    <xsl:choose>
                        <xsl:when test="contains(@SampleIdentifier,':') or contains(@SampleIdentifier,'+')">
                            <xsl:variable name="one" select="translate(@SampleIdentifier,':','-')"/>
                            <xsl:value-of select="isa:quotes(translate($one,'+',' and '))"/> 
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="isa:quotes(@SampleIdentifier)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="isa:quotes(@sampleType)"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="isa:quotes(@sampleType)"/> 
        </xsl:otherwise>
    </xsl:choose>    
</xsl:template>
    
<xsl:template name="sampleType" match="sample">
    <xsl:choose>
        <xsl:when test="@sampleType='BLANK'">
            <xsl:text>"negative control"</xsl:text>
        </xsl:when>
        <xsl:when test="contains(@sampleType,'QC_')">
            <xsl:text>"positive control"</xsl:text>
        </xsl:when>
        <xsl:when test="contains(@sampleType,'ZERO_')">
            <xsl:text>"negative control"</xsl:text>
        </xsl:when>
        <xsl:when test="contains(@sampleType,'STANDARD_')">
            <xsl:text>"positive control"</xsl:text>
        </xsl:when>
        <xsl:otherwise>
            <xsl:text>"specimen"</xsl:text>
        </xsl:otherwise>
    </xsl:choose>    
</xsl:template>    
 
<xsl:template name="assay-negativeMode" match="plate"  priority="1">

    <xsl:variable name="assaynegativefile" select="concat('output/',data,'a_biocrates_assay_negative_mode.txt')[normalize-space()]"></xsl:variable>
    <xsl:value-of select="$assaynegativefile[normalize-space()]" /> 
    <xsl:result-document href="{$assaynegativefile}">
    
        <xsl:text>Sample Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Extract Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[kit name]</xsl:text><xsl:text>&#9;</xsl:text> 
        <xsl:text>Parameter Value[plate ID]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[plate position]</xsl:text><xsl:text>&#9;</xsl:text>
      <!--  <xsl:text>Parameter Value[chromatography instrument]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[chromatography column]</xsl:text><xsl:text>&#9;</xsl:text> -->
        <xsl:text>Parameter Value[mass spectrometry instrument]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>         
        <xsl:text>Parameter Value[acquisition parameter file]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[inlet type]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[polarity]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[run number]</xsl:text><xsl:text>&#9;</xsl:text> 
        <xsl:text>Parameter Value[injection number]</xsl:text><xsl:text>&#9;</xsl:text>        
        <xsl:text>Date</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>MS Assay Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Raw Spectral Data File</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[software]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Data Transformation Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Derived Spectral Data File</xsl:text><xsl:text>&#9;</xsl:text>
<xsl:text>
</xsl:text>        
        <xsl:apply-templates select="//well" mode="negative"/>     
</xsl:result-document>
</xsl:template>

 <xsl:template name="wellnegative" match="//well" mode="negative">      
        <xsl:apply-templates select="injection" mode="polarity">
            <xsl:with-param name="polarity">negative</xsl:with-param>
        </xsl:apply-templates>
</xsl:template>


<xsl:template match="plate" name="assay-positiveMode" priority="1">
    <xsl:variable name="assaypositivefile" select="concat('output/',data,'a_biocrates_assay_positive_mode.txt')[normalize-space()]"></xsl:variable>
    <xsl:value-of select="$assaypositivefile[normalize-space()]" /> 
    <xsl:result-document href="{$assaypositivefile}">
        <xsl:copy-of select=".[normalize-space()]"></xsl:copy-of>
        
        <xsl:text>Sample Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Extract Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[kit name]</xsl:text><xsl:text>&#9;</xsl:text> 
        <xsl:text>Parameter Value[plate ID]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[plate position]</xsl:text><xsl:text>&#9;</xsl:text>
      <!--<xsl:text>Parameter Value[chromatography instrument]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[chromatography column]</xsl:text><xsl:text>&#9;</xsl:text> -->
        <xsl:text>Parameter Value[mass spectrometry instrument]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>        
        <xsl:text>Parameter Value[acquisition parameter file]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[inlet type]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[polarity]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Source REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Term Accession Number</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[run number]</xsl:text><xsl:text>&#9;</xsl:text> 
        <xsl:text>Parameter Value[injection number]</xsl:text><xsl:text>&#9;</xsl:text>        
        <xsl:text>Date</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>MS Assay Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Raw Spectral Data File</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Protocol REF</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Parameter Value[software]</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Data Transformation Name</xsl:text><xsl:text>&#9;</xsl:text>
        <xsl:text>Derived Spectral Data File</xsl:text><xsl:text>&#9;</xsl:text>
<xsl:text>
</xsl:text>  
        <xsl:apply-templates select="//well" mode="positive"/> 
    </xsl:result-document>
 </xsl:template>
  
<xsl:template name="wellpositive" match="//well" mode="positive">      
    <xsl:apply-templates select="injection" mode="polarity">
            <xsl:with-param name="polarity">positive</xsl:with-param>
        </xsl:apply-templates>
</xsl:template>    

<xsl:template name="injection" match="injection" mode="polarity">
    <xsl:param name="polarity"/>
    <xsl:variable name="wellposition" select="parent::well/@wellPosition"></xsl:variable>
   
        <xsl:choose>    
            <xsl:when test="contains(lower-case(@polarity), $polarity)">                  
                <xsl:choose>
                    <xsl:when test="key('samplelookupid',parent::well/@sample)/@SampleIdentifier !=''">
                        <xsl:choose>                       
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':') or contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:variable name="one" select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                                <xsl:value-of select="translate($one,'+',' and ')"/> 
                                <!-- <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/> -->
                                <xsl:text>&#9;</xsl:text>
                            </xsl:when>
                            <!-- <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            <xsl:text>&#9;</xsl:text>
                        <"/xsl:when>-->
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                                <xsl:text>&#9;</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>
                        <!-- <xsl:text>none reported</xsl:text> -->
                        <xsl:text>&#9;</xsl:text> 
                    </xsl:otherwise>
                </xsl:choose> 
                <xsl:text>"extraction/derivatization"</xsl:text>
                <xsl:text>&#9;</xsl:text>
                <xsl:choose>
                    <xsl:when test="key('samplelookupid',parent::well/@sample)/@SampleIdentifier !=''">
                        <xsl:choose>                       
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':') or contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:variable name="one" select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                                <xsl:value-of select="isa:quotes(translate($one,'+',' and '))"/> 
                                <!-- <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/> -->
                                <xsl:text>&#9;</xsl:text>
                            </xsl:when>
                            <!-- <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                            <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                            <xsl:text>&#9;</xsl:text>
                        </xsl:when>-->
                            <xsl:otherwise>
                                <xsl:value-of select="isa:quotes(key('samplelookupid',parent::well/@sample)/@SampleIdentifier)"/>
                                <xsl:text>&#9;</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                        <!--<xsl:choose>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                                <xsl:text>&#9;</xsl:text>
                            </xsl:when>
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:value-of select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+',' and ')"/>
                                <xsl:text>&#9;</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                                <xsl:text>&#9;</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>-->
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="isa:quotes(key('samplelookupid',parent::well/@sample)/@sampleType)"/>
                        <xsl:text>&#9;</xsl:text> 
                    </xsl:otherwise>                        
                </xsl:choose>
                
                <xsl:value-of select="concat(isa:quotes(ancestor::plate/@usedOP),'&#9;')"/>
                
                <xsl:choose>   
                    <xsl:when test="starts-with(ancestor::plate/@usedOP,'KIT1-')">
                        <!-- <xsl:value-of select="substring-after(/data/plateInfo/@usedOP,'KIT1-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates p150 Kit"</xsl:text>
                        <xsl:text>&#9;</xsl:text>
                    </xsl:when>
                    <xsl:when test="starts-with(ancestor::plate/@usedOPP,'KIT2-')">
                        <!-- <xsl:value-of select="substring-after(child::plateInfo/@usedOP,'KIT2-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates p180 LCMS Part"</xsl:text>
                        <xsl:text>&#9;</xsl:text>
                    </xsl:when>
                    <xsl:when test="starts-with(ancestor::plate/@usedOP,'KIT3-')">
                        <!--<xsl:value-of select="substring-after(child::plateInfo/@usedOP,'KIT3-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates p180 FIA Part"</xsl:text>
                        <xsl:text>&#9;</xsl:text>
                    </xsl:when>
                    <xsl:when test="starts-with(ancestor::plate/@usedOP,'ST17-')">
                        <!--<xsl:value-of select="substring-after(child::plateInfo/@usedOP,'ST17-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates Stero17 Kit"&#9;</xsl:text>
                    </xsl:when>
                    <xsl:when test="starts-with(ancestor::plate/@usedOP,'MD01-')">
                        <!--  <xsl:value-of select="substring-after(child::plateInfo/@usedOP,'MD01-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates MetaDis Kit LCMS Part"&#9;</xsl:text>
                    </xsl:when> 
                    <xsl:when test="starts-with(ancestor::plate/@usedOP,'MD02-')">
                        <!-- <xsl:value-of select="substring-after(child::plateInfo/@usedOP,'MD02-')">
                </xsl:value-of> -->
                        <xsl:text>"Biocrates MetaDis Kit FIA Part"&#9;</xsl:text>
                    </xsl:when> 
                    <xsl:otherwise>
                        <xsl:text>"not reported"&#9;</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>     
                <xsl:value-of select="concat(isa:quotes(ancestor::plate/@plateBarcode),'&#9;')"/>
                
                <xsl:value-of select="isa:quotes($wellposition)"/>
                <xsl:text>&#9;</xsl:text>
                
                <xsl:call-template name="instrument"></xsl:call-template>
                <xsl:text>&#9;</xsl:text>
                
                <xsl:value-of select="isa:quotes(@acquisitionMethod)"/>
                <xsl:text>&#9;</xsl:text>
                
                <xsl:choose>    
                    <xsl:when test="contains(@acquisitionMethod, 'FIA')">
                        <xsl:text>"flow injection analysis"&#9;</xsl:text>
                        <xsl:text>"PSI-MS"&#9;</xsl:text>
                        <xsl:text>"http://purl.obolibrary.org/obo/MS_1000058"&#9;</xsl:text><!--http://purl.obolibrary.org/obo/ -->                            
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>"liquid chromatography separation"&#9;</xsl:text>
                        <xsl:text>"PSI-MS"&#9;</xsl:text>
                        <xsl:text>"http://purl.obolibrary.org/obo/MS_1002271"&#9;</xsl:text><!--http://purl.obolibrary.org/obo/ -->                            
                    </xsl:otherwise>                   
                </xsl:choose>   
                
                <xsl:value-of select="concat(isa:quotes(concat(lower-case(@polarity), ' scan')),'&#9;')"/>
                <xsl:text>"PSI-MS"&#9;</xsl:text>
                <xsl:text>"http://purl.obolibrary.org/obo/MS_1000129"&#9;</xsl:text><!--http://purl.obolibrary.org/obo/ -->
                
                <xsl:value-of select="isa:quotes(ancestor::plate/@runNumber)"/>
                <xsl:text>&#9;</xsl:text>
                
                <xsl:value-of select="isa:quotes(@injectionNumber)"/>
                <xsl:text>&#9;</xsl:text>
                
                <xsl:value-of select="isa:quotes(substring-before(@injectionTime,'T'))"/>
                <xsl:text>&#9;"</xsl:text>
                
                <xsl:value-of select="concat(ancestor::plate/@usedOP, '_',ancestor::plate/@plateBarcode, '_',$wellposition,'_',ancestor::plate/@runNumber, '_',@injectionNumber,'_',key('samplelookupid',parent::well/@sample)/@sampleType,'_',key('samplelookupid',parent::well/@sample)/@barcode,'_')"/>
                <!--                    <xsl:value-of select="ancestor::plate/@usedOP"/><xsl:text>_</xsl:text>                     
                    <xsl:value-of select="ancestor::plate/@plateBarcode"/><xsl:text>_</xsl:text>
                    <xsl:value-of select="$wellposition"/><xsl:text>_</xsl:text>
                    <xsl:value-of select="ancestor::plate/@runNumber"/><xsl:text>_</xsl:text>
                    <xsl:value-of select="@injectionNumber"/><xsl:text>_</xsl:text>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/><xsl:text>_</xsl:text>
                    <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@barcode"/><xsl:text>_</xsl:text>-->                   
                <xsl:choose>
                    <xsl:when test="key('samplelookupid',parent::well/@sample)/@SampleIdentifier !=''">
                        <xsl:choose>                       
                            <xsl:when test="contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':') or contains(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,'+')">
                                <xsl:variable name="one" select="translate(key('samplelookupid',parent::well/@sample)/@SampleIdentifier,':','-')"/>
                                <xsl:value-of select="translate($one,'+',' and ')"/> 
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@SampleIdentifier"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="key('samplelookupid',parent::well/@sample)/@sampleType"/>                           
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text>"&#9;</xsl:text>
                
                <xsl:value-of select="isa:quotes(@rawDataFileName)"/>
                <xsl:text>&#9;</xsl:text>
                <xsl:text>"biocrates analysis"</xsl:text>
                <xsl:text>&#9;</xsl:text>
                <xsl:value-of select="isa:quotes(/data/@swVersion)"/>
                <xsl:text>&#9;</xsl:text>                  
                <xsl:value-of select="isa:quotes(concat('DT_',ancestor::plate/@usedOP, '_',ancestor::plate/@plateBarcode))"/>
                <xsl:text>&#9;</xsl:text>                  
                <xsl:value-of select="isa:quotes(concat('DT_',ancestor::plate/@usedOP, '_',ancestor::plate/@plateBarcode,'_',$polarity,'_maf.txt'))"/>
                
               
<xsl:text>
</xsl:text>
            </xsl:when>
        </xsl:choose>
</xsl:template>


<!-- //////////////////HELPER TEMPLATE/////////////// -->
<!-- a template to infer Instrument related information from Biocrates Kit number -->
<!-- TODO: incorporate the processing in the core template -->
    <xsl:template match="/data/plate/well/injection" name="instrument">
        <xsl:choose>
            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-2'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> <!-- manufacturer -->
                <xsl:text>4000er/4500er eclipse</xsl:text>
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000870</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-LC')">
                    <xsl:text>liquid chromatography</xsl:text>
                </xsl:if>
            </xsl:when>
            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-5502'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> 			   <!-- manufacturer -->
                <xsl:text>4000er/4500er eclipse</xsl:text> <!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000870</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-LC')">
                    <xsl:text>liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>

            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-5512'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> 			<!-- manufacturer -->
                <xsl:text>5500er eclipse</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000931</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UHPLC')"> 
                    <xsl:text>ultra high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>
            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-8004'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Waters</xsl:text> 			<!-- manufacturer -->
                <xsl:text>TQ-MS HPLC</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001790</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UPLC')"> 
                    <xsl:text>high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>

            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-8014'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Waters</xsl:text> 			<!-- manufacturer -->
                <xsl:text>Xevo TQ MS</xsl:text>			<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001790</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UPLC')"> 
                    <xsl:text>ultra high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	

            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-8114'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Waters</xsl:text> 			<!-- manufacturer -->
                <xsl:text>Xevo TQ-S</xsl:text>			<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001792</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UPLC')"> 
                    <xsl:text>ultra high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	

            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-9004'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Thermo</xsl:text> 			<!-- manufacturer -->
                <xsl:text>TSQ Vantage</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001510</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UPLC')"> 
                    <xsl:text>ultra high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	

            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-9014'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Thermo</xsl:text> 			<!-- manufacturer -->
                <xsl:text>TSQ Vantage	</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001510</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT2-UPLC')"> 
                    <xsl:text>ultra high performance liquid chromatography</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	
            
            <xsl:when test="ancestor::plate/@usedOP='KIT3-0-5404'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> <!-- manufacturer -->
                <xsl:text>4000er/4500er eclipse</xsl:text>
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000870</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')">
                    <xsl:text>flow infusion acquisition</xsl:text>
                </xsl:if>
            </xsl:when>	

            <xsl:when test="ancestor::plate/@usedOP='KIT3-0-5504'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> <!-- manufacturer -->
                <xsl:text>5500er eclipse</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000931</xsl:text>			<!-- PSI-MS identifier -->	
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')">
                    <xsl:text>flow infusion acquisition</xsl:text>
                </xsl:if>
            </xsl:when>	

            <xsl:when test="ancestor::plate/@usedOP='KIT3-0-5604'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>ABSciex</xsl:text> <!-- manufacturer -->
                <xsl:text>6500er eclipse</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1000931</xsl:text>			<!-- PSI-MS identifier -->	
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')">
                    <xsl:text>flow infusion acquisition</xsl:text>
                </xsl:if>
            </xsl:when>	
 
            <xsl:when test="ancestor::plate/@usedOP='KIT3-0-8004'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Waters</xsl:text> 			<!-- manufacturer -->
                <xsl:text>TQ-MS HPLC</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001790</xsl:text>			<!-- PSI-MS identifier -->	
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')"> 
                    <xsl:text>flow infusion acquisition</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	
 
            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-8114'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Waters</xsl:text> 			<!-- manufacturer -->
                <xsl:text>Xevo TQ-S</xsl:text>			<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001792</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')"> 
                    <xsl:text>flow infusion acquisition</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>	
            
            <xsl:when test="ancestor::plate/@usedOP='KIT2-0-9004'">
                <xsl:value-of select="@usedOP"/>
                <xsl:text>Thermo</xsl:text> 			<!-- manufacturer -->
                <xsl:text>TSQ Vantage</xsl:text>		<!-- instrument name -->
                <xsl:text>&#9;</xsl:text>
                <xsl:text>http://purl.obolibrary.org/obo/MS_1001510</xsl:text>			<!-- PSI-MS identifier -->
                <xsl:text>&#9;PSI-MS</xsl:text>
                <xsl:if test="contains(@acquisitionMethod,'KIT3-FIA')"> 
                    <xsl:text>flow infusion acquisition</xsl:text> <!-- instrument type -->
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>"none reported"&#9;</xsl:text>
                <xsl:text>&#9;</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>   


<!-- //////////////////HELPER TEMPLATE/////////////// -->
<!-- implementation of a 'string replace' -->
 <xsl:template name="string-replace-all">
        <xsl:param name="text" />
        <xsl:param name="replace" />
        <xsl:param name="by" />
        <xsl:choose>
            <xsl:when test="contains($text, $replace)">
                <xsl:value-of select="substring-before($text,$replace)" />
                <xsl:value-of select="$by" />
                <xsl:call-template name="string-replace-all">
                    <xsl:with-param name="text"
                        select="substring-after($text,$replace)" />
                    <xsl:with-param name="replace" select="$replace" />
                    <xsl:with-param name="by" select="$by" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>    


<!-- //////////////////HELPER TEMPLATE/////////////// -->
<!-- implementation of a recursive loop invoked when padding tables -->
    <!-- uses the $max variable to set the value of the limit -->
    <xsl:template name="loop">
        <xsl:param name="i"/>
        <xsl:param name="limit"/>
        <xsl:if test="$i &lt; $limit">
                 <xsl:text>not applicable&#9;</xsl:text>                        
            <xsl:call-template name="loop">
                <xsl:with-param name="i" select="$i+1"/>
                <xsl:with-param name="limit" select="$limit"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>