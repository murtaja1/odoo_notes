from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # 'mail.activity.mixin' used to schedule an activity.
    _description = "hospital.patient"

    # tracking attr used to log the change in the chatter.  
    name = fields.Char(tracking=True)
    is_child = fields.Boolean(tracking=True)
    age = fields.Integer(tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    # compute attr means that the field will be filled the function.
    capitalize_name = fields.Char(compute='_compute_capitalize_name')
    ref = fields.Char(name="Reference", default=lambda self: _('New'))
    appointment_count = fields.Integer(string='Appointment Count', compute="_compute_appointment_count")

    responsible_id = fields.Many2one('res.partner', string="Responsible")
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
    
    def _compute_appointment_count(self):
        appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count = appointment_count

    # conditions on a field.
    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age <= 0:
                raise ValidationError(_('Age must be filled!'))

    # decorator used to change the field when changing name without saving. 
    @api.depends('name')
    def _compute_capitalize_name(self):
        for rec in self:
            if rec.name: rec.capitalize_name = rec.name.upper()
            else: rec.capitalize_name = ''
    

    # when age changes call this function.
    @api.onchange('age')
    def _onChange_age(self):
        if self.age >= 10:
            self.is_child = False
        else: 
            self.is_child = True

    # overwriting the create method. vals_list contains all the record values.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals_list)