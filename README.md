# odoo_notes

# adding a StatusBar:
        1. add a selection field named state in the model with the states like e.g. 
        ` state = fields.Selection(
            selection=[
                ('draft', 'Draft'),
                ('confirm', 'Confirm'),
                ('done', 'Done'),
                ('cancel', 'Cancelled'),
            ],
            string='Status',
            default='draft',
        )`
    2. add a header in the form view e.g. 
