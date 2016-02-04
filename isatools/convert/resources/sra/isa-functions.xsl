<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:isa="http://www.isa-tools.org/"
    exclude-result-prefixes="xs isa"
    version="2.0">
    
    <xsl:function name="isa:quotes" as="xs:string">
        <xsl:param name="input" as="xs:string?"/>
        <xsl:value-of select="concat('&quot;', $input, '&quot;')"/>
    </xsl:function>    
    
    <xsl:function name="isa:quotes-tab" as="xs:string">
        <xsl:param name="input" as="xs:string?"/>
        <xsl:value-of select="concat('&quot;', $input, '&quot;', '&#9;')"/>
    </xsl:function>
    
    <xsl:function name="isa:single-name-value" as="xs:string">
        <xsl:param name="name" as="xs:string"/>
        <xsl:param name="value" as="xs:string?"/>
        <xsl:value-of select="concat('&quot;', $name, '&quot;', '&#9;', '&quot;', $value, '&quot;', '&#10;')"/>
    </xsl:function>
</xsl:stylesheet>