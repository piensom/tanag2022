from odoo import models, fields, api, _
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf
import datetime
from odoo.exceptions import UserError

class PrintPaymentSummary(models.TransientModel):
    _name = "print.payment.summary"
    
    @api.model
    def _get_from_date(self):
        company = self.env.user.company_id
        current_date = datetime.date.today()
        from_date = company.compute_fiscalyear_dates(current_date)['date_from']
        return from_date
    
    from_date = fields.Date(string='From Date', default=_get_from_date)
    to_date = fields.Date(string='To Date', default=fields.Date.context_today)
    payment_summary_file = fields.Binary('Payment Summary Report')
    file_name = fields.Char('File Name')
    payment_report_printed = fields.Boolean('Payment Report Printed')
    currency_id = fields.Many2one('res.currency','Currency', default=lambda self: self.env.user.company_id.currency_id)
    
    
    def action_print_payment_summary(self,):
        
        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True;')
        worksheet = workbook.add_sheet('Reporte Comisiones')
        quantity_format = xlwt.easyxf(num_format_str='#,##0.00')
        
        worksheet.col(0).width = 7000
        worksheet.col(1).width = 7000
        worksheet.col(2).width = 7000
        worksheet.col(3).width = 7000
        worksheet.col(4).width = 7000
        worksheet.col(5).height = 5000
          
        row = 2
        customer_row = 2
        total_pagos = 0
        paid_amount = 0
        
        usuarios_objs = self.env['usuarios.comisiones'].search([('activo','=',True)])
        
        for wizard in self:
            heading =  'Reporte Comisiones del ' + str(wizard.from_date) + 'al ' + str(wizard.to_date)
            worksheet.write_merge(0, 0, 0, 5, heading, easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color white; font: color black; font:bold True;' "borders: top thin,bottom thin"))
            customer_payment_data = {}
            invoice_objs = self.env['account.payment'].search([('date','>=',wizard.from_date),
                                                               ('date','<=',wizard.to_date),
                                                               ('reconciled_invoices_count','!=',0),
                                                               ('payment_type','=','inbound')])
            
            
            worksheet.write(2, 0, ('Porcentaje Comisiones Pagadas'))
            worksheet.write(2, 1, ('Total de Ventas'))
            worksheet.write(2, 2, ('Total de Ventas (sin IVA)'))
            worksheet.write(2, 3, ('Total de Comisiones Pagadas'))
            
            for payment in invoice_objs:
                paid_amount += payment.amount
                total_pagos += payment.amount
                row += 1
                
            total_pagos_sin_iva = total_pagos/1.12 
            total_comisiones = 0
            for porc in usuarios_objs:
                total_comisiones += porc.porcentaje

            worksheet.write(3, 0, (str(total_comisiones) + '%'))
            worksheet.write(3, 1, total_pagos, quantity_format)
            worksheet.write(3, 2, (total_pagos_sin_iva), quantity_format)
            worksheet.write(3, 3, (total_pagos_sin_iva*(total_comisiones/100)), quantity_format)
            
            
            
            
            worksheet.write(5, 0, 'Nombre', easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color dark_teal; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            worksheet.write(5, 1, 'Total Ventas', easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color dark_teal; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            worksheet.write(5, 2, 'Comision', easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color dark_teal; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            worksheet.write(5, 3, 'Porcentaje Comision', easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color dark_teal; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            
            fila = 6
            
            for linea in usuarios_objs:
                worksheet.write(fila, 0, linea.nombre)
                worksheet.write(fila, 1, total_pagos, quantity_format)
                worksheet.write(fila, 2, (total_pagos_sin_iva*(linea.porcentaje/100)), quantity_format)
                worksheet.write(fila, 3, (str(linea.porcentaje) + '%'))
                fila += 1


            fp = io.BytesIO()
            workbook.save(fp)
            excel_file = base64.encodestring(fp.getvalue())
            wizard.payment_summary_file = excel_file
            wizard.file_name = 'Reporte Comisiones.xls'
            wizard.payment_report_printed = True
            fp.close()
            return {
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'res_model': 'print.payment.summary',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self.env.context,
                    'target': 'new',
                       }

    
# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
