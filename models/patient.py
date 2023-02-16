from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "hospital.patient"

    # tracking attr used to log the change in the chatter. 
    name = fields.Char(tracking=True)
    is_child = fields.Boolean(tracking=True)
    age = fields.Integer(tracking=True)
    # compute attr means that the field will be filled the function.
    capitalize_name = fields.Char(compute='_compute_capitalize_name')
    ref = fields.Char(name="Reference", default=lambda self: _('New'))

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