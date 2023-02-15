from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "hospital.patient"

    # tracking attr used to log the change in the chatter. 
    name = fields.Char(tracking=True)
    is_child = fields.Boolean(tracking=True)
    age = fields.Integer(tracking=True)

    # when age changes call this function.
    @api.onchange('age')
    def _onChange_age(self):
        if self.age >= 10:
            self.is_child = False
        else: 
            self.is_child = True