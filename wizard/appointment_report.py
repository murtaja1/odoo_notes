from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ReportAppointmentWizard(models.TransientModel):
    _name = "hospital.report.appointment.wizard"
    _description = "hospital.report.appointment.wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date_from = fields.Date()
    date_to = fields.Date()

    def action_print_appointment(self):
        domain = []
        patient_id = self.patient_id
        date_from = self.date_from
        date_to = self.date_to

        if patient_id:
            domain += [('patient_id','=', patient_id.id)]
        if date_from:
            domain += [('date','>=', date_from)]
        if date_to:
            domain += [('date','<=', date_to)]

        appointments = self.env['hospital.appointment'].search_read(domain)
        data = {
            'form_data': self.read()[0],
            'appointments': appointments
        } 
        return self.env.ref('hospital_management.appointment_report_details').report_action(self, data=data)
