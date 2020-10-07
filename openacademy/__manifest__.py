{
    "name": "openacademy",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "author": "My Company,Odoo Community Association (OCA)",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml  # noqa
    # for the full list
    "category": "Uncategorized",
    "version": "13.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "board"],
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "views/partner.xml",
        "reports.xml",
        "views/session_board.xml",
    ],
    # only loaded in demonstration mode
    "demo": ["demo/demo.xml"],
    "license": "AGPL-3",
}
