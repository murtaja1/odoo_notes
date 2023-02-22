from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CreateAppointmentWizard(models.TransientModel):
    _name = "hospital.create.appointment.wizard"
    _description = "hospital.create.appointment.wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    name = fields.Char()

    def action_create(self):
        raise ValidationError(_('Create clicked!'))