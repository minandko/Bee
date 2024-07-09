# -*- coding: utf-8 -*-
{
    'name': "Weight Scale Check In Check Out",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "BEE Data Myanmar",
    'website': "https://www.beedatamyanmar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web', 'product', 'uom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gate_screen.xml',
        'views/truck_check_in_check_out.xml',
        'views/gate_ip_address.xml',
        'views/master_data.xml',
        'views/truck.xml',
        'wizard/truck_out_finder.xml',
        'data/uom_data.xml',
        'data/ir_sequence.xml',
        'views/menu_items.xml',
        'report/weight_scale_templates.xml',
        'report/weight_scale_reports.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
    'assets': {
        'web.assets_backend': [
            'weight_scale_check_in_out/static/src/**/*',
            'weight_scale_check_in_out/static/src/xml/**/*',
        ],
    },
}
