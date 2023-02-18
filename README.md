# odoo_notes

# adding a StatusBar:

1. add a selection field named state in the model with the states like e.g.

```
state = fields.Selection(
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
```

- widget="statusbar": odoo widget for styling.
- options="{ 'clickable': '1' }": to make the statusbar clickable.
- statusbar_visible='draft,confirm,done': show only the following states.

### Adding buttons in the status bar:

1. we add a function in the model like:

```
def action_confirm(self):
    self.state = 'confirm'
```

2. we add a button in the form view that's related to the model, like:

```
<button id="button_confirm" type="object" name="action_confirm" string="Confirm" class='btn-primary' states="draft"/>
```

- type="object": means there will be a function defined in the model to handle the button when clicked.
- name="action_confirm": the name of the function in the model.
- string="Confirm": the display name.
- states="draft": when should this button be visible. meaning it'll be visible in draft only or you can set to states="draft,cancel,..."

# fields and attributes:

## attributes:

tracking=True: means log any change to this field in the chatter.
used like:

```
age = fields.Integer(tracking=True)
```

## fields:

many2one field: like a selection field with data from another model:
used like:

```
responsible_id = fields.Many2one('res.partner', string="Responsible")
```

- 'res.partner': the name of the model.

# Methods Overriding:

## create method:

- to override the create method use the following code block.

```
@api.model_create_multi
def create(self, vals):
    # peform your action here.
    return super(HospitalPatient, self).create(vals)
```

- vals: the record values that you can update before saving the record.

# Sequential value:

### it's a value that is auto generated with every record.

#### create a seq value with the next steps:

1. create `data/sequence.xml` file with the following code and add in `__manifest__.py` in data after security.

```
<data noupdate="1">
    <record id="hospital_management_squence" model="ir.sequence">
        <field name="name">Patinet Sequence</field>
        <field name="code">hospital.patient</field>
        <field name="prefix">HP</field>
        <field name="padding">5</field>
    </record>
</data>
```

- noupdate="1": means if the user has updated it in the UI don't override it when upgrading the module.
- prefix: means add PH before the sequential value.
- padding: the length of the digits.

2. create a ref field in the model.

```
ref = fields.Char(name="Reference", default=lambda self: _('New'))
```

2. override the create method in the model with the following code.

```
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
    return super(HospitalPatient, self).create(vals_list)
```

3. add the ref field in the form and tree view.

- use the following code in form and add inside the sheet tag.

```
<div class="oe_title">
    <h1>
        <field name="ref" readonly='1'/>
    </h1>
</div>
```

- simply add the field in the tree view like this.

```
<field name="ref"/>
```
