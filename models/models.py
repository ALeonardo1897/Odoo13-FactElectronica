from odoo import models, fields, api
from .. import nubefact
import json,requests

import logging
_logger = logging.getLogger(__name__)

class MyFact(models.Model):
     _name = 'account.move'
     _inherit = 'account.move'

     '''New Fields'''
     type_voucher = fields.Selection(
          selection=[
               ('factura','(01) Factura'),
               ('boleta_venta','(02) Boleta de Venta'),
               ('nota_credito', '(03) Nota de Crédito'),
               ('nota_debito','(04) Nota de Débito')
          ], string='Tipo de Comprobante', default='factura')

     response_sunat = fields.Char('Respuesta Sunat',size=150)

     http_response_code_sunat = fields.Integer('HTTP Response Code PSE')

     url_pdf_pse = fields.Char('URL PDF', size=300)

     '''Method Send SUNAT'''
     def button_fact_elec(self):

          # Header
          headers = {'Authorization': 'Bearer ' + nubefact.credentials.TOKEN,
                     'Content-Type':'application/json'}

          # Body
          body = {

               "operacion": "generar_comprobante",
               #Factura -> 1
               "tipo_de_comprobante": nubefact.utils.validate.check_type_voucher(self.type_voucher),
               #Factura empieza con F
               "serie": nubefact.utils.validate.extract_serial_by_type_document(self.type_voucher),
               # Dinamico
               "numero": nubefact.utils.validate.extract_sequence(self.name),
               #Venta Interna -> 1
               "sunat_transaction": 1,
               #Tipo de Identificación del Cliente (DNI->1,RUC->6)
               "cliente_tipo_de_documento": nubefact.utils.validate.check_type_document(self.partner_id.l10n_latam_identification_type_id.id),
               #Número de Identificación del Cliente
               "cliente_numero_de_documento": self.partner_id.vat,
               "cliente_denominacion": self.partner_id.name,
               "cliente_direccion":  self.partner_id.street + " - " + self.partner_id.city,
               "fecha_de_emision": nubefact.utils.validate.format_date(self.invoice_date),
               "moneda": nubefact.utils.validate.check_currency(self.currency_id.id),
               "porcentaje_de_igv": 18.00,
               "total_gravada": self.amount_untaxed,
               "total_igv": self.amount_tax,
               "total": self.amount_total,
               "enviar_automaticamente_a_la_sunat": True,
               "enviar_automaticamente_al_cliente": False,
               "items": self.get_items()
          }

          # Request
          r = requests.post(nubefact.credentials.URL, headers=headers, data=json.dumps(body))
          response = r.json()
          status_code = r.status_code
          _logger.error(json.dumps(body))
          _logger.error(response)

          #Check Boleta Response None
          if(response['sunat_description'] is None):
               response['sunat_description'] = ''

          # Set response_sunat
          if(status_code == 200):
               if(self.type_voucher == 'factura'):
                    self.response_sunat = 'Success : ' + response['sunat_description']
               elif(self.type_voucher == 'boleta_venta'):
                    self.response_sunat = 'Success : ' + response['serie'] + '-' + str(response['numero'])
               self.http_response_code_sunat = status_code
               self.url_pdf_pse = response['enlace_del_pdf']
          else:
               self.http_response_code_sunat = status_code
               self.response_sunat = 'Error : ' + response['errors']


     def get_items(self):
          dataArray = []
          for item in self.invoice_line_ids:
               data = {
                    # Producto -> NIU | Servicio -> ZZ
                    "unidad_de_medida": "NIU",
                    "codigo": item.product_id.default_code,
                    "descripcion": item.product_id.name,
                    "cantidad": item.quantity,
                    "valor_unitario": item.price_unit,
                    "precio_unitario": item.price_unit + item.price_unit*18/100,
                    "descuento": item.price_unit*item.discount/100,
                    "subtotal": item.price_subtotal,
                    # Gravado - Operacion Onerosa
                    "tipo_de_igv": 1,
                    "igv": item.price_subtotal*18/100,
                    "total": item.price_total,
                    "anticipo_regularizacion": False,
                    #Codigo del CATALOGO PRODUCTO SUNAT - NUBEFACT
                    "codigo_producto_sunat": "10000000",
               }
               dataArray.append(data)
          _logger.error(dataArray)
          return dataArray
