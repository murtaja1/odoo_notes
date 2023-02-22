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
        rec = self.env['hospital.appointment'].create(vals)
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'view_mode':"form",
            'res_model':"hospital.appointment",
            'res_id': rec.id
        }

    def action_view_appointments(self):
        # method 1
        action = self.env.ref('hospital_management.hospital_appointment_action').read()[0]
        action['domain'] = [('patient_id','=',self.patient_id.id)]
        return action
        
        # method 2
        # action = self.env["ir.actions.act_window"]._for_xml_id('hospital_management.hospital_appointment_action')
        # action['domain'] = [('patient_id','=',self.patient_id.id)]
        # return action

        # method 3
        # return {
        #     'name': _('Appointments'),
        #     'type': 'ir.actions.act_window',
        #     'view_type':'form',
        #     'view_mode':"tree,form",
        #     'res_model':"hospital.appointment",
        #     'domain': [('patient_id','=',self.patient_id.id)]
        # }