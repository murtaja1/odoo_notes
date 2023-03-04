from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    # we are only inheriting and not creating new model
    _inherit = 'product.template'

    detailed_type = fields.Selection(selection_add=[('test', 'Test')], ondelete={'test': 'cascade'})
    type = fields.Selection(selection_add=[('test', 'Test')], ondelete={'test': 'cascade'})