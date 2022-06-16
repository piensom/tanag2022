# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Reporte de Comisiones',
    'version': '14.1',
    'category': 'Accounting',
    'summary': 'Reporte de Comisiones',
    'license':'AGPL-3',
    'description': """
    Reporte de Comisiones
""",
    'author' : 'Piensom, Sociedad Anonima',
    'website' : 'http://www.piensom.com',
    'depends': ['account'],
    'data': [
        'wizard/print_payment_summary_view.xml',
        'views/usuarios_comisiones.xml',
        'security/ir.model.access.csv',        
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
