<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="xs" xpath-default-namespace="http://www.biocrates.com/metstat/result/xml_1.0"
	version="2.0">
	<xsl:strip-space elements="*"/>
	<xsl:output method="text" encoding="UTF-8"/>
	
	<!-- Separate out each positive and negative of plates into different files -->	
	
	<xsl:template match="/">		
		<xsl:apply-templates select="data/plate" mode="main"/>				
	</xsl:template>
	
	<xsl:template match="data/plate" mode="main">		
		<xsl:variable name="distinct-column-names-with-metabolite" select="distinct-values(well/injection/measure/@*/name(.))"/>
		<xsl:variable name="distinct-column-names" select="$distinct-column-names-with-metabolite[. != 'metabolite']"/>
		<xsl:for-each-group select="." group-by="well/injection/@polarity">
			<xsl:result-document href="{concat('output/DT_', @usedOP, '_', @plateBarcode, '_', lower-case(current-grouping-key()), '_maf.txt')}">
			
				<xsl:for-each select="current-group()">
					<xsl:call-template name="write-out-to-file">												
						<xsl:with-param name="polarity" select="current-grouping-key()" tunnel="yes"/>
						<xsl:with-param name="distinct-column-names" select="$distinct-column-names" tunnel="yes"/>
					</xsl:call-template>
				</xsl:for-each>				
			</xsl:result-document>
		</xsl:for-each-group>									
	</xsl:template>
	
	<xsl:template name="write-out-to-file">		
		<xsl:param name="polarity" required="yes" tunnel="yes"/>			
		<!-- Create the column headers -->				
		<xsl:text>metabolite identifier&#9;database identifier&#9;</xsl:text>
		<xsl:apply-templates select="well/injection[@polarity = $polarity]" mode="header"/>
		<xsl:apply-templates select="preceding-sibling::metabolite">			
			<xsl:with-param name="plate-barcode" select="@plateBarcode" tunnel="yes"/>
		</xsl:apply-templates>	
	</xsl:template>
	
	<!-- Creating the column headers -->
	<xsl:template match="well/injection" mode="header">
		<xsl:param name="distinct-column-names" required="yes" tunnel="yes"/>
		<xsl:variable name="plate-name" select="tokenize(@rawDataFileName, '\.')"/>		
		<xsl:for-each select="$distinct-column-names">			
			<xsl:value-of select="concat($plate-name[1],'[', . ,']')"/><xsl:text>&#9;</xsl:text>			
		</xsl:for-each>			
	</xsl:template>
	
	<!-- Creating the rest of the rows -->
	<xsl:template match="metabolite">
		<xsl:param name="plate-barcode" required="yes" tunnel="yes"/>
		<!-- New line -->
		<xsl:text>&#10;</xsl:text>
		<xsl:value-of select="@identifier"/><xsl:text>&#9;</xsl:text>
		<xsl:text>CHEBI:</xsl:text><xsl:value-of select="child::BioID/@CHEBI[1]"/><xsl:text>&#9;</xsl:text>
		<xsl:apply-templates select="following-sibling::plate[@plateBarcode = $plate-barcode]">
			<xsl:with-param name="metabolite-id" select="@identifier" tunnel="yes"/>				
		</xsl:apply-templates>		
	</xsl:template>		
	
	<xsl:template match="data/plate/well">		
		<xsl:param name="polarity" required="yes" tunnel="yes"/>		
		<xsl:apply-templates select="injection[@polarity = $polarity]"/>															
	</xsl:template>	
	
	<xsl:template match="injection">
		<xsl:param name="metabolite-id" required="yes" tunnel="yes"/>		
		<xsl:param name="distinct-column-names" required="yes" tunnel="yes"/>
		<xsl:variable name="measures" select="measure[@metabolite = $metabolite-id]"/>
		<xsl:for-each select="$distinct-column-names">						
			<xsl:call-template name="fill-in-column">
				<xsl:with-param name="specific-column" select="."/>
				<xsl:with-param name="measures" select="$measures"/>
			</xsl:call-template>																 		
		</xsl:for-each>			
	</xsl:template>
	
	<xsl:template name="fill-in-column">
		<xsl:param name="specific-column" required="yes"/>
		<xsl:param name="measures" required="yes"/>		
		<xsl:value-of select="$measures/@*[name() = $specific-column]"/><xsl:text>&#9;</xsl:text>
	</xsl:template>	
</xsl:stylesheet>	
	
<!--	<xsl:template match="/">
		<xsl:result-document href="output.xml" method="xml">
			<table>
				<xsl:apply-templates select="data/metabolite"/>
			</table>
		</xsl:result-document>		
	</xsl:template>
	
	<xsl:template match="data/metabolite">
		<metabolite>
			<xsl:attribute name="id">
				<xsl:value-of select="@identifier"/>
			</xsl:attribute>
			<xsl:apply-templates select="following-sibling::plate">
				<xsl:with-param name="metabolite-id" select="@identifier" tunnel="yes"/>				
			</xsl:apply-templates>			
		</metabolite>
	</xsl:template>
	
	<xsl:template match="data/plate/well">		
		<xsl:apply-templates select="injection"/>				
	</xsl:template>	
	
	<xsl:template match="injection">
		<xsl:param name="metabolite-id" required="yes" tunnel="yes"/>
		<xsl:variable name="filename" select="tokenize(@rawDataFileName, '\.')"/>
		<injection>		
			<xsl:attribute name="metabolite-id">
				<xsl:value-of select="$metabolite-id"/>
			</xsl:attribute>	
			<xsl:attribute name="id">
				<xsl:value-of select="concat($filename[1], ':', @polarity)"/>
			</xsl:attribute>
			<xsl:attribute name="concentration">
				<xsl:value-of select="measure[$metabolite-id = @metabolite]/@concentration"/>					
			</xsl:attribute>
		</injection>
	</xsl:template>		
</xsl:stylesheet> -->