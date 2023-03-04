from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ReportPatientWizard(models.TransientModel):
    _name = "hospital.report.patient.wizard"
    _description = "hospital.report.patient.wizard"

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age = fields.Integer()

    def action_print_patient(self):
        data = {
            'form_data': self.read()[0],
        } 
        return self.env.ref('hospital_management.all_patient_details_report_action').report_action(self, data=data)
