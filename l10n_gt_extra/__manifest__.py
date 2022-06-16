# -*- encoding: utf-8 -*-

{
    'name': 'Guatemala - Reportes contabilidad',
    'version': '15.0.1',
    'category': 'Localization',
    'description': """ Reportes por la SAT en Guatemala. """,
    'author': 'Multiple',
    'website': 'http://piensom.com/',
    'depends': ['l10n_gt', 'account_tax_python', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_gt_extra_base.xml',
        'views/account_view.xml',
        'views/res_partner_view.xml',
        'views/product_views.xml',
        'views/report.xml',
        'views/reporte_banco.xml',
        'views/reporte_partida.xml',
        'views/reporte_compras.xml',
        'views/reporte_ventas.xml',
        'views/reporte_inventario.xml',
        'views/reporte_diario.xml',
        'views/reporte_mayor.xml',
        'views/l10n_gt_extra_view.xml',
    ],
    'demo': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
