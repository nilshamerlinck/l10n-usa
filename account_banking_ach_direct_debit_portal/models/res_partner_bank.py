from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    bank_address = fields.Char(related="bank_id.street", readonly=False)
