from odoo import models, fields, api, _

class CreateAppointmentWizard(models.TransientModel):
    _name = "hospital.search.appointment.wizard"
    _description = "hospital.search.appointment.wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient')

    def action_search_appointment_m1(self):
        action = self.env.ref('hospital_management.hospital_appointment_action').read()[0]
        action['domain'] = [('patient_id','=',self.patient_id.id)]
        return action
    
    def action_search_appointment_m2(self):
        action = self.env["ir.actions.act_window"]._for_xml_id('hospital_management.hospital_appointment_action')
        action['domain'] = [('patient_id','=',self.patient_id.id)]
        return action

    def action_search_appointment_m3(self):
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'view_type':'form',
            'view_mode':"tree,form",
            'res_model':"hospital.appointment",
            'domain': [('patient_id','=',self.patient_id.id)]
        }
