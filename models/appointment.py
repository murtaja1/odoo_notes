from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'
    _description = "hospital.appointment"
    _order = 'doctor_id,id desc'

    # tracking attr used to log the change in the chatter.  
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    age = fields.Integer(tracking=True, related='patient_id.age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    description = fields.Text()
    ref = fields.Char(name="Reference", default=lambda self: _('New'))
    date = fields.Date('Date')
    time_checkup = fields.Datetime()
    medicine_line_ids = fields.One2many('hospital.appointment.medicine','appointment_id',string="Medicine Lines")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True
    )

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'
    
    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'
    
    @api.onchange('patient_id')
    def onchagne_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
        else:
            self.gender = ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals_list)
    
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_('you can\'t delete this record because it is in done state!'))
        return super(HospitalAppointment, self).unlink()
    
class HospitalAppointmentMedicine(models.Model):
    _name = "hospital.appointment.medicine"
    _description = "hospital.appointment.medicine"

    name = fields.Char(string="Name", required=True)
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment')
