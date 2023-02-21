from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "hospital.appointment"

    # tracking attr used to log the change in the chatter.  
    patient_id = fields.Many2one('hospital.patient', string='Name')
    age = fields.Integer(tracking=True, related='patient_id.age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    description = fields.Text()
    ref = fields.Char(name="Reference", default=lambda self: _('New'))
    date = fields.Date('Date')
    time_checkup = fields.Datetime()
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