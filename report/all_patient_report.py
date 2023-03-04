from odoo import models, fields, api, _

class AllPatientReport(models.AbstractModel):
    _name = "report.hospital_management.all_patient_details_report_template"
    _description = "report.hospital_management.all_patient_details_report_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        age = data.get('form_data').get('age')
        gender = data.get('form_data').get('gender')
        if age != 0:
            domain += [('age','=',age)]
        if gender:
            domain += [('gender','=',gender)]
        docs = self.env['hospital.patient'].search_read(domain)
    
        return {
            'docs': docs,
            'search': {'age': age, 'gender':gender}
        }