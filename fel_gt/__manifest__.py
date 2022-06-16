# -*- encoding: utf-8 -*-

{
    'name': 'FEL Guatemala',
    'version': '15.0.1',
    'category': 'Custom',
    'description': """ Campos y funciones base para la facturación electrónica en Guatemala """,
    'author': 'Rodrigo Fernandez',
    'website': 'http://aquih.com/',
    'depends': ['l10n_gt_extra', 'res_address_towns'],
    'data': [
        'views/account_view.xml',
        'views/partner_view.xml',
    ],
    'demo': [],
    'installable': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
