# -*- coding: utf-8 -*-
{
    'name': "minisaf",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/lecturer_view.xml',
        'views/student_view.xml',
        'views/course_view.xml',
        'views/courseclass_view.xml',
        'views/courseplan_view.xml',
        'wizard/addstudent_view.xml',
        'wizard/addclass_view.xml',
        'wizard/gettranscript_view.xml',
        'report/report.xml',
        'report/course_list.xml',
        'report/lecturer_list.xml',
        'report/student_list.xml',
        'report/student_transcript.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
