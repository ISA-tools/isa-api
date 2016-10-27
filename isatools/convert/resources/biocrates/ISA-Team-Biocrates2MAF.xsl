<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0" xmlns:xs="http://www.w3.org/2001/XMLSchema"> 

    
<!--
    
***************************README********************************************** 
Date: 2014-10-15

Content: xsl stylesheet for Biocrates XML documents comlpying with schema xmlns="http://www.biocrates.com/metstat/result/xml_1.0"

Task: 
Creates 'Metabolite Assignment File' (aka MAF files) required for a submission to EMBL-EBI Metabolights repository [1] of Metabolomics Data
from Biocrates XML documents compliant to Biocrates xsd 1.0 [2].

Note: 
This is an XSL 2.0 transformation and requires Saxon-PE- 9.5.1.5 to run.

Biocrates test files:
demo_data.xml
2014-07-15_Conc.xml

Command: xsltproc ISA-Team-Biocrates2MAF.xsl <Biocrates-StudyExportFile.xml>

TODO: 
improve on performance.
transpose output to make it a true MAF file


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
    

    
        <xsl:output method="text"/>

        <xsl:key name="measure-by-injection" match="measure" use="ancestor::injection[1]/@rawDataFileName"/>
        <xsl:key name="injection-measures" match="measure" use="@metabolite"/>
        <xsl:variable name="injection-measures" select="/data/plate/well/injection/measure[generate-id()=generate-id(key('injection-measures', @metabolite)[1])]/@metabolite"/>

    
<xsl:template match="data" priority="1">
                


        <xsl:call-template name="datafiles-per-plate"/> 
</xsl:template>



<xsl:template name="datafiles-per-plate" match="plate">
    
    <xsl:for-each select="/data">
        
        <!--BEGIN a block of commented lines to record some provenance information -->
        <!--This information may be used by EMBL-EBI Metabolights -->   
        <xsl:text>#BIOCRATES software version: </xsl:text>  <xsl:value-of select="@swVersion"/>
        <xsl:text>
</xsl:text>
        <xsl:text>#BIOCRATES document filename: </xsl:text>
        <xsl:value-of select="base-uri()"/>
        <xsl:text>
</xsl:text>
        <xsl:text>#BIOCRATES export date: </xsl:text>  <xsl:value-of select="substring-before(@dateExport,'T')"/>
        <xsl:text>
</xsl:text>
        <xsl:text>#EMBL-EBI: MetabolightsISATab transformation by: ISA-Team-Biocrates2MAF.xsl </xsl:text>
        <!-- END of the comment block -->                    
    </xsl:for-each>
    
    <xsl:for-each select="data">
        <xsl:value-of select="@swVersion"/>
        <xsl:text>
</xsl:text>            
        <xsl:value-of select="@concentrationUnit"/>
        <xsl:text>
</xsl:text>            
    </xsl:for-each>
    
    
            <xsl:for-each select="plate">      
                <xsl:variable name="usedOP" select="@usedOP"/>
                <xsl:variable name='plateBarcode' select="@plateBarcode"/> 
                
                <xsl:variable name="datafile" select="concat('output/',$usedOP,'-',$plateBarcode,'-maf.txt')[normalize-space()]"></xsl:variable>
                <xsl:value-of select="$datafile[normalize-space()]" />
                <xsl:result-document href="{$datafile}">
                    <xsl:copy-of select=".[normalize-space()]"></xsl:copy-of>
                    <!--   <xsl:for-each select="/data/plate/well/injection[generate-id(.)=generate-id(key('injection',@polarity)[1])]/@polarity">
           <xsl:variable name='polarity' select="." />-->
                    <xsl:text>Sample ID&#9;</xsl:text>
                    <xsl:for-each select="/data/plate/well/injection/measure[generate-id()=generate-id(key('injection-measures', @metabolite)[1])]/@metabolite">    
                        <!-- <xsl:sort/> --> 
                        <xsl:if test="contains(.,$usedOP)">
                            <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text>&#9;</xsl:text>
                            <!-- <xsl:text></xsl:text><xsl:value-of select="key('metabolitelookupid',.)/metabolitePlateInfo/@uloq"/><xsl:text> [uloq]&#9;</xsl:text> -->
                            <!--  <xsl:text></xsl:text><xsl:value-of select="key('metabolite_by_platebarcode',concat($plateBarcode,key('metabolitelookupid',.)/@identifier)), /metabolitePlateInfo/@uloq"/><xsl:text> [uloq]&#9;</xsl:text> 
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [intensity]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [concentration]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [status]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [internal standard area]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [internal standard retention time]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [internal standard intensity]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [internal standard concentration]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [relative retention time]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [analyte signal to noise ratio]&#9;</xsl:text>
                   <xsl:text></xsl:text><xsl:value-of select="."/><xsl:text> [accuracy]&#9;</xsl:text>      -->             
                        </xsl:if>    
                    </xsl:for-each>    
<xsl:text>
</xsl:text>         
                    <xsl:for-each select="child::well/injection">  
                        <!--<xsl:value-of select="ancestor::well[1]/@sample"/>-->
                        <xsl:choose>
                            <xsl:when test="contains(lower-case(@polarity), 'positive')">  
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [concentration (</xsl:text><xsl:value-of select="ancestor::data/@concentrationUnit"/><xsl:text>)]&#9;</xsl:text>                         
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose> 
                                        <xsl:when test="$measure[@metabolite = current()]/@intensity !=''"> 
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@concentration"/><xsl:text>&#9;</xsl:text>                                   
                                        </xsl:when> 
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose> 
                                </xsl:for-each>                          
<xsl:text>
</xsl:text>                               
   <!--                             
       
       
                            <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [analyte Peak Area]&#9;</xsl:text>                                                           
                                <xsl:variable name="measure1" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure1[@metabolite = current()]/@intensity  !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure1[@metabolite = current()]/@analytePeakArea"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>                      
<xsl:text>
</xsl:text>                 
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [analyte retention time]&#9;</xsl:text>
                                <xsl:variable name="measure2" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure2[@metabolite = current()]/@intensity !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure2[@metabolite = current()]/@analyteRetentionTime"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each> 
<xsl:text>
</xsl:text>                     
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [intensity]&#9;</xsl:text>                    
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@intensity !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@intensity"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>             
<xsl:text>
</xsl:text> -->
                                
                    
                                                            
<!--                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [status]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@intensity !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@status"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text>                 
                                
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [internal standard area]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@ISTDArea !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@ISTDArea"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text>  
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [internal standard retention time]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@internalStdRetentionTime !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@internalStdRetentionTime"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
 <xsl:text>
</xsl:text> 
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [internal standard intensity]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@intensityIstd !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@intensityIstd"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text>                      
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [internal standard concentration(</xsl:text><xsl:value-of select="/data/@concentration"/><xsl:text>)]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@concentrationIstd !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@concentrationIstd"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text>  
                               
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [relative retention time]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@relRetentionTime !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@relRetentionTime"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text>
                                
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [analyte S/N]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@analyteS2N !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@analyteS2N"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
 <xsl:text>
</xsl:text>                    
                                
                                <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [accuracy]&#9;</xsl:text>               
                                <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
                                <xsl:for-each select="$injection-measures"> 
                                    <xsl:choose>
                                        <xsl:when test="$measure[@metabolite = current()]/@accuracy !=''">
                                            <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@accuracy"/><xsl:text>&#9;</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>&#9;</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>   
<xsl:text>
</xsl:text> -->
                            </xsl:when>
                            
                            <!-- OLD LAYOUT Kept for Documentation 
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@concentration"/>                    
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@status"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@ISTDArea"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@internalStdRetentionTime"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@intensityIstd"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@concentrationIstd"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@relRetentionTime"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@analyteS2N"/>
                       <xsl:text>&#9;</xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@accuracy"/> -->
                            <!--          </xsl:when>
                   </xsl:choose>
              </xsl:for-each> 
<xsl:text>
</xsl:text> -->
                            
                            <!-- TODO: deal with Negative Polarity -->
           <xsl:when test="contains(lower-case(@polarity), 'negative')">    
               <xsl:value-of select="concat(substring-before(@rawDataFileName, '.'),':', @polarity)"/><xsl:text> [concentration (</xsl:text><xsl:value-of select="ancestor::data/@concentrationUnit"/><xsl:text>)]&#9;</xsl:text>                         
               <xsl:variable name="measure" select="key('measure-by-injection', @rawDataFileName)"/>
               <xsl:for-each select="$injection-measures"> 
                   <xsl:choose>
                       <xsl:when test="$measure[@metabolite = current()]/@intensity !=''">
                           <xsl:text></xsl:text><xsl:value-of select="$measure[@metabolite = current()]/@concentration"/><xsl:text>&#9;</xsl:text>
                       </xsl:when>
                       <xsl:otherwise>
                           <xsl:text>&#9;</xsl:text>
                       </xsl:otherwise> 
                   </xsl:choose>
               </xsl:for-each>                          
<xsl:text>
</xsl:text>   
           </xsl:when>                
      <!--           <xsl:variable name="measureN" select="key('measure-by-injection', @rawDataFileName)"/>
                 <xsl:for-each select="$injection-measures"> 
                     <xsl:choose>
                         <xsl:when test="$measureN[@metabolite = current()]/@intensity !=''">
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@metabolite"/>
                             <xsl:text>:</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@analytePeakArea"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@analyteRetentionTime"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@intensity"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@concentration"/>                    
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@status"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@ISTDArea"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@internalStdRetentionTime"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@intensityIstd"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@concentrationIstd"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@relRetentionTime"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@analyteS2N"/>
                             <xsl:text>&#9;</xsl:text><xsl:value-of select="$measureN[@metabolite = current()]/@accuracy"/>
                         </xsl:when>
                     </xsl:choose>
                 </xsl:for-each> 
<xsl:text>
</xsl:text> --> 

            
                            <!--   
        <xsl:for-each select="/data/plate/well/injection/measure[generate-id(.)=generate-id(key('run-metabolites', @metabolite)[1])]/@metabolite">              
               <xsl:text>metabolite:</xsl:text><xsl:value-of select="."/>        
            </xsl:for-each>
                     -->
                            
                        </xsl:choose>
                    </xsl:for-each>                     
                </xsl:result-document>
            </xsl:for-each> 
</xsl:template>
        
        
</xsl:stylesheet>