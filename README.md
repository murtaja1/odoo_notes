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
    2. add a header tag in the form view e.g.
        widget="statusbar":  odoo widget for styling
        options="{ 'clickable': '1' }":  to make the statusbar clickable.
        statusbar_visible='draft,confirm,done': show only the following states.
        `
        <header>
            <field name="state" widget="statusbar" options="{ 'clickable': '1' }" statusbar_visible='draft,confirm,done'/>
        </header>
        `
