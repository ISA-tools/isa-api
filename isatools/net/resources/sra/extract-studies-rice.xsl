<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
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
    
    <xsl:template name="generate-distinct-protocols-description">
        <xsl:param name="protocol" required="yes"/>
        <descriptions>
            <xsl:for-each-group select="$protocol/studies/study" group-by="@protocoldescription">
                <description protocoldescription="{ current-grouping-key() }"/>
            </xsl:for-each-group>
        </descriptions>
    </xsl:template> 
    
    <xsl:template name="process-lib-strategies-sources">
        <xsl:param name="acc-number" required="yes"/>
        <xsl:variable name="experiment-ids" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', $acc-number, '&amp;display=xml'))/ROOT/STUDY/STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(.,'NA-EXPERIMENT')]/following-sibling::ID"/>
        <studies>
            <xsl:for-each select="tokenize($experiment-ids, ',')">
                <xsl:variable name="experiment-document-lib-desc" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', . , '&amp;display=xml'))/ROOT"/>
                <xsl:value-of select="document(concat('http://www.ebi.ac.uk/ena/data/view/', . , '&amp;display=xml'))"/>
                <xsl:apply-templates select="$experiment-document-lib-desc/EXPERIMENT" mode="get-studies">
                    <xsl:with-param name="id" select="."/>
                </xsl:apply-templates>                
            </xsl:for-each>
        </studies>
    </xsl:template>
    
    <xsl:template match="EXPERIMENT" mode="get-studies">
        <xsl:param name="id" required="yes"/>
        <study acc-number="{ $id }" accession="{ @accession }" library-strategy="{ DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY }" library-source="{ DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE }"  protocoldescription="{ DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_CONSTRUCTION_PROTOCOL }"/>
    </xsl:template>
    
    <xsl:template name="generate-distinct-exp-sources-strategies">
        <xsl:param name="exp-sources-strategies" required="yes"/>
        <experiments>
            <xsl:for-each-group select="$exp-sources-strategies/studies/study" group-by="@library-strategy">
                <xsl:sort select="current-grouping-key()"/>
                <xsl:variable name="lib-strategy" select="current-grouping-key()"/>
                <xsl:for-each-group select="current-group()" group-by="@library-source">
                    <xsl:variable name="lib-source" select="current-grouping-key()"/>
                    <xsl:for-each-group select="current-group()" group-by="@acc-number">
                        <xsl:sort select="current-grouping-key()"/>
                        <experiment library-strategy="{ $lib-strategy }" library-source="{ $lib-source }" acc-number="{ @acc-number }">
                            <xsl:variable name="exp" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', @acc-number, '&amp;display=xml'))"/>
                            <xsl:for-each select="current-group()">
                                <exp>
                                    <xsl:attribute name="accession">
                                        <xsl:value-of select="$exp/ROOT/EXPERIMENT[@accession = current()/@accession]/@accession"/>
                                    </xsl:attribute>
                                </exp>                                                    
                            </xsl:for-each>
                        </experiment>
                    </xsl:for-each-group>>
                </xsl:for-each-group>
            </xsl:for-each-group>
            <xsl:value-of select="count(experiment)"/>
        </experiments>
    </xsl:template>
    
    <xsl:template name="process-samples-attributes">
        <xsl:param name="acc-number" required="yes"/>
        <xsl:variable name="sample-ids" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', $acc-number, '&amp;display=xml'))/ROOT/STUDY/STUDY_LINKS/STUDY_LINK/XREF_LINK/DB[contains(.,'NA-SAMPLE')]/following-sibling::ID"/>
        <samples>
            <xsl:for-each select="tokenize($sample-ids, ',')">
                <xsl:variable name="sample-doc" select="document(concat('http://www.ebi.ac.uk/ena/data/view/', ., '&amp;display=xml'))/ROOT"/>
                <xsl:apply-templates select="$sample-doc/SAMPLE" mode="get-sample">
                    <xsl:with-param name="id" select="."/>
                </xsl:apply-templates>                
            </xsl:for-each>
        </samples>
    </xsl:template>
    
    <xsl:template match="SAMPLE" mode="get-sample">
        <xsl:param name="id" required="yes"/>
        <sample acc-number="{ $id }" accession="{ @accession }">
            <xsl:apply-templates select="SAMPLE_ATTRIBUTES" mode="get-sample"/>
        </sample>
    </xsl:template>
    
    <xsl:template match="SAMPLE_ATTRIBUTES" mode="get-sample">
        <xsl:apply-templates select="SAMPLE_ATTRIBUTE" mode="get-sample"/>
    </xsl:template>
    
    <xsl:template match="SAMPLE_ATTRIBUTE" mode="get-sample">
        <xsl:apply-templates select="TAG" mode="get-sample"/>
    </xsl:template>
    
    <xsl:template match="TAG" mode="get-sample">
        <characteristic term="{ . }"/>
    </xsl:template>
    
    <xsl:template name="generate-distinct-characteristic-terms">
        <xsl:param name="characteristics" required="yes"/>
        <terms>
            <xsl:for-each-group select="$characteristics/samples/sample/characteristic" group-by="@term">
                <term>
                    <xsl:value-of select="current-grouping-key()"/>
                </term>
            </xsl:for-each-group>
        </terms>
    </xsl:template>
    
    <xsl:template name="generate-rawdatafile-structure">
        <xsl:param name="parsedlink" required="yes"/>
        <links>
        <xsl:for-each select="tokenize($parsedlink, '\n')">
            <xsl:if test="not(contains(.,'fastq_ftp')) and string-length(.) > 0">
               <link> 
                <xsl:for-each select="tokenize(., '\t')">
                   <xsl:choose>
                       <xsl:when test="contains(.,'.fastq.gz')">
                           <xsl:attribute name="raw-data-file">
                               <xsl:value-of select="."/>
                           </xsl:attribute>
                       </xsl:when>
                       <xsl:otherwise>
                           <xsl:attribute name="file-checksum">
                               <xsl:value-of select="."/>
                           </xsl:attribute>
                       </xsl:otherwise>
                   </xsl:choose>
                </xsl:for-each>
               </link>
            </xsl:if>
        </xsl:for-each>
        </links>         
    </xsl:template>
    
</xsl:stylesheet>
