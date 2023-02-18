# odoo_notes

# adding a StatusBar:

1. add a selection field named state in the model with the states like e.g.
   ```state = fields.Selection(
       selection=[
           ('draft', 'Draft'),
           ('confirm', 'Confirm'),
           ('done', 'Done'),
           ('cancel', 'Cancelled'),
       ],
       string='Status',
       default='draft',
   )
   ```
2. add a header tag in the form view e.g.
``` 
   <header>
       <field name="state" widget="statusbar" options="{ 'clickable': '1' }" statusbar_visible='draft,confirm,done'/>
   </header>

- widget="statusbar": odoo widget for styling.
- options="{ 'clickable': '1' }": to make the statusbar clickable.
- statusbar_visible='draft,confirm,done': show only the following states.
   ```

### Adding buttons in the status bar:

1. we add a function in the model like:

```
    def action_confirm(self):
        self.state = 'confirm'
```

2. we add a button in the form view that's related to the model, like:

```
<button id="button_confirm" type="object" name="action_confirm" string="Confirm" class='btn-primary' states="draft"/>

- type="object": means there will be a function defined in the model to handle the button when clicked.
- name="action_confirm": the name of the function in the model.
- string="Confirm": the display name.
- states="draft": when should this button be visible. meaning it'll be visible in draft only or you can set to states="draft,cancel,..."
```

# fields and attributes:
## attributes:
```
tracking=True: means log any change to this field in the chatter.
used like:
age = fields.Integer(tracking=True)
```
## fields:
```
many2one field: like a selection field with data from another model:
used like:
responsible_id = fields.Many2one('res.partner', string="Responsible")
- 'res.partner': the name of the model.
```
