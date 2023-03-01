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
    appointment_count = fields.Integer(string='Appointment Count', compute="_compute_appointment_count")
    active = fields.Boolean(string="Active", default=True)

    def copy(self, default=None):
        default = default or {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
        default['note'] = 'this record is copied!'
        return super(HospitalDoctor, self).copy(default)
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id','=',rec.id)])
            rec.appointment_count = appointment_count
