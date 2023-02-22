from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CreateAppointmentWizard(models.TransientModel):
    _name = "hospital.create.appointment.wizard"
    _description = "hospital.create.appointment.wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Date()

    def action_create(self):
        vals = {
            'patient_id': self.patient_id.id,
            'date': self.date
        }
        self.env['hospital.appointment'].create(vals)