<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:terceros="http://www.sat.gob.mx/terceros">
	<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/>
	<!-- Manejador de nodos tipo PorCuentadeTerceros -->
	<xsl:template match="terceros:PorCuentadeTerceros">
		<!--Iniciamos el tratamiento de los atributos del complemento concepto Por cuenta de Terceros -->
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@version"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@rfc"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@nombre"/>
		</xsl:call-template>
		<!--Iniciamos el tratamiento de los atributos de la información fiscal del complemento de terceros -->
		<xsl:for-each select="./terceros:InformacionFiscalTercero">
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@calle"/>
			</xsl:call-template>
			<xsl:call-template name="Opcional">
				<xsl:with-param name="valor" select="./@noExterior"/>
			</xsl:call-template>
			<xsl:call-template name="Opcional">
				<xsl:with-param name="valor" select="./@noInterior"/>
			</xsl:call-template>
			<xsl:call-template name="Opcional">
				<xsl:with-param name="valor" select="./@colonia"/>
			</xsl:call-template>
			<xsl:call-template name="Opcional">
				<xsl:with-param name="valor" select="./@localidad"/>
			</xsl:call-template>
			<xsl:call-template name="Opcional">
				<xsl:with-param name="valor" select="./@referencia"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@municipio"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@estado"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@pais"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@codigoPostal"/>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Manejo de los atributos de la información aduanera del complemento de terceros -->
		<xsl:for-each select=".//terceros:InformacionAduanera">
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@numero"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@fecha"/>
			</xsl:call-template>
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@aduana"/>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Manejo de los atributos de la cuenta predial del complento de terceros -->
		<xsl:for-each select=".//terceros:CuentaPredial">
			<xsl:call-template name="Requerido">
				<xsl:with-param name="valor" select="./@numero"/>
			</xsl:call-template>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
