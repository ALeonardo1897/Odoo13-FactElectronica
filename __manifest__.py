# -*- coding: utf-8 -*-
{
    'name': "DConsulting - Facturación Electrónica",

    'summary': """
        Módulo para la facturación electrónica DConsulting | Test""",

    'description': """
        Implementar la facturación electrónica a través de SUNAT | Perú
    """,

    'author': "Alvaro Leonardo | DConsulting",
    'website': "https://www.dconsulting.com.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/invoice.xml'
    ],
}
