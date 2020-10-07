from odoo import fields, models


class Partner(models.Model):
    # _name = 'openacademy.course'
    # _description = 'Model to store partner'
    _inherit = "res.partner"
    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many(
        "openacademy.session", string="Attended Sessions", readonly=True
    )
    other_field = fields.Boolean(default=True)
    other_field2 = fields.Boolean(default=True)
