from odoo import models, fields, api, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # 'mail.activity.mixin' used to schedule an activity.
    _description = "hospital.doctor"

    name = fields.Char(tracking=True)
    age = fields.Integer(tracking=True)
    image = fields.Binary(string='image')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
