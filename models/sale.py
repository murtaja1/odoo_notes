from odoo import models, fields, api, _
from odoo.addons.sale.models.sale_order import SaleOrder as OdooSaleOrder

class SaleOrder(models.Model):
    # we are only inheriting and not creating new model
    _inherit = 'sale.order'

    sale_description = fields.Char()

    # def _unlink_except_draft_or_cancel(self):
    #     return super(SaleOrder,self).unlink()

def _unlink_except_draft_or_cancel(self):
    return super(SaleOrder,self).unlink()

OdooSaleOrder._unlink_except_draft_or_cancel = _unlink_except_draft_or_cancel