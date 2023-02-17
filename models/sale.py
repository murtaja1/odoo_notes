from odoo import models, fields, api, _

class SaleOrder(models.Model):
    # we are only inheriting and not creating new model
    _inherit = 'sale.order'

    sale_description = fields.Char()