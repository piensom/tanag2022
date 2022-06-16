# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round
from xml.etree import ElementTree as ET
from .qr_generator import generateQrCode
from datetime import datetime
import base64
from lxml import etree
import requests

import html
import uuid
import zeep

import logging

class ResCompany(models.Model):
    _inherit = "res.company"

    usuario = fields.Char('Usuario Tekra')
    clave = fields.Char('Clave Tekra')
    cliente = fields.Char('Cliente Tekra')
    contrato = fields.Char('Contrato Tekra')
    frases_fel = fields.Text('Frases FEL')
    adenda_fel = fields.Text('Adenda FEL')
    pruebas_fel = fields.Boolean('Modo de Pruebas FEL')

class AccountJournal(models.Model):
    _inherit = "account.journal"
    generar_fel = fields.Boolean('Generar FEL',)
    

class AccountMove(models.Model):
    _inherit = "account.move"

    pdf_fel = fields.Binary('PDF FEL', copy=False)
    name_pdf_fel = fields.Char('Nombre archivo PDF FEL', default='fel.pdf', size=32)
    url_tekra = fields.Char('URL Tekra', copy=False)
    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')

    
    def _post(self, soft=True):    
        for factura in self:
            if factura.journal_id.generar_fel and factura.move_type in ['out_invoice', 'out_refund', 'in_invoice']:
                if factura.firma_fel:
                    raise UserError("La factura ya fue validada, por lo que no puede ser validada nuevamnte")


                dte = factura.dte_documento()
                xmls = etree.tostring(dte, xml_declaration=True, encoding="UTF-8").decode("utf-8")
                xmls_base64 = base64.b64encode(xmls.encode("utf-8"))
                logging.warn(dte)
                uuid_factura = str(uuid.uuid5(uuid.NAMESPACE_OID, str(factura.id))).upper()
                if dte:
                    xml_sin_firma = etree.tostring(dte, encoding="UTF-8").decode("utf-8")
                    logging.warn(xml_sin_firma)
                    url = "https://apicertificacion.tekra.com.gt/servicio.php"
                    if factura.company_id.pruebas_fel:
                        url = "http://apicertificacion.desa.tekra.com.gt:8080/certificacion/servicio.php"
                    headers = { "Content-Type": "text/xml" }
                    body = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><CertificacionDocumento xmlns="https://apicertificacion.tekra.com.gt/certificacion/wsdl/"><Autenticacion><pn_usuario>{}</pn_usuario><pn_clave>{}</pn_clave><pn_cliente>{}</pn_cliente><pn_contrato>{}</pn_contrato><pn_id_origen>Sistema Facturacion</pn_id_origen><pn_ip_origen>64.56.44.22</pn_ip_origen><pn_firmar_emisor>SI</pn_firmar_emisor></Autenticacion><Documento><![CDATA[{}]]></Documento></CertificacionDocumento></Body></Envelope>'.format(factura.company_id.usuario,factura.company_id.clave,factura.company_id.cliente,factura.company_id.contrato,xml_sin_firma)
                    #raise UserError(body)
                    response = requests.post(url,data=body,headers=headers)
                    resultadoXML = response.text

                    resultadoXML = resultadoXML.replace("&gt;", ">")
                    resultadoXML = resultadoXML.replace("&lt;", "<")
                    resultadoXML = resultadoXML.replace('<?xml version="1.0" encoding="utf-8"?>', "")
                    resultadoXML = resultadoXML.replace('<?xml version="1.0" encoding="utf-8" ?>', "")
                    resultadoXML = resultadoXML.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
                    if not factura.company_id.pruebas_fel:
                        resultadoXML = resultadoXML.replace('<?xml version="1.0" encoding="utf-8" standalone="no"?>', "")

                    if resultadoXML.find("dte:SAT ClaseDocumento") >= 0:
                        xml_certificado_root = etree.XML(resultadoXML.encode("utf-8"))
                        numero_autorizacion = xml_certificado_root.find(".//{http://www.sat.gob.gt/dte/fel/0.2.0}NumeroAutorizacion")
                        factura.firma_fel = numero_autorizacion.text
                        factura.serie_fel = numero_autorizacion.get("Serie")
                        factura.numero_fel = numero_autorizacion.get("Numero")
                        #factura.url_tekra = 'http://seguimiento.tekra.com.gt/ver_documento.aspx?UUID='+numero_autorizacion.text
                        nit = 'CF'
                        if factura.partner_id.vat:
                            nit = factura.partner_id.vat.replace('-','')
                        factura.url_tekra = 'https://felpub.c.sat.gob.gt/verificador-web/publico/vistas/verificacionDte.jsf?&tipo=autorizacion&numero='+numero_autorizacion.text+'&emisor='+factura.company_id.vat.replace('-','')+'&receptor='+nit+'&monto='+str(factura.amount_total)

                    else:
                        raise UserError(resultadoXML)

        return super(AccountMove,self)._post(soft)
    
    def _generate_qr_code(self):
        self.qr_image = generateQrCode.generate_qr_code(self.url_sat)    

    
    def button_cancel(self):
        result = super(AccountMove, self).button_cancel()
        for factura in self:
            logging.warn(result)
            if factura.journal_id.generar_fel:
                dte = factura.dte_anulacion()
                xmls = etree.tostring(dte, xml_declaration=True, encoding="UTF-8").decode("utf-8")
                xmls_base64 = base64.b64encode(xmls.encode("utf-8"))
                logging.warn(dte)
                #raise UserError(xmls)
                if dte:
                    xml_sin_firma = etree.tostring(dte, encoding="UTF-8").decode("utf-8")

                    url = "https://apicertificacion.tekra.com.gt/servicio.php"
                    if factura.company_id.pruebas_fel:
                        url = "http://apicertificacion.desa.tekra.com.gt:8080/certificacion/servicio.php"

                    headers = { "Content-Type": "application/xml" }
                    body = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><AnulacionDocumento xmlns="https://apicertificacion.tekra.com.gt/certificacion/wsdl/"><Autenticacion><pn_usuario>{}</pn_usuario><pn_clave>{}</pn_clave><pn_cliente>{}</pn_cliente><pn_contrato>{}</pn_contrato><pn_id_origen>Sistema Facturacion</pn_id_origen><pn_ip_origen>64.56.44.22</pn_ip_origen><pn_firmar_emisor>SI</pn_firmar_emisor></Autenticacion><Documento><![CDATA[{}]]></Documento></AnulacionDocumento></Body></Envelope>'.format(factura.company_id.usuario,factura.company_id.clave,factura.company_id.cliente,factura.company_id.contrato,xml_sin_firma)
                    response = requests.post(url,data=body,headers=headers)
                    resultadoXML = response.text
                else:
                    raise UserError(r.text)    
        
        return result                
