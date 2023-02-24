from odoo import models, fields, api, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # 'mail.activity.mixin' used to schedule an activity.
    _description = "hospital.doctor"

    name = fields.Char(tracking=True)
    age = fields.Integer(tracking=True, copy=False)
    image = fields.Binary(string='image')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    note = fields.Text(string="Note")
    prescription = fields.Text(string="Prescription")

    def copy(self, default=None):
        default = default or {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
        default['note'] = 'this record is copied!'
        return super(HospitalDoctor, self).copy(default)
