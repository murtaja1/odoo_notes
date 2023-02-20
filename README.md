# odoo_notes

# 1. Adding Menus and Actions:
## Menus:

### - a menu that has no parent is the main model menu. like:

```
<menuitem id="hospital_management.root_menu" name="Hospital Management" action="hospital_management.hospital_patient_action" />
```

### - a menu that has a parent is the menu that appear in the header after clicking the main menu. Like:

```
<menuitem id="hospital_management.operations_menu" name="Operations" parent="hospital_management.root_menu" sequence="10"/>
```

### - the following menu is a submenu that appears under the Operations menu. Like:

```
<menuitem id="hospital_management.patients_menu" name="Patients" action="hospital_management.hospital_patient_action" parent="hospital_management.operations_menu" sequence="10"/>
```

## Actions:

### - an action is triggered after clicking the menu that has an action. like:

```
<record id="hospital_management.hospital_patient_action" model="ir.actions.act_window">
    <field name="name">Patients</field>
    <field name="res_model">hospital.patient</field>
    <field name="view_mode">tree,form,kanban</field>
</record>
```


# 2. adding a StatusBar:

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

# 3. fields and attributes:

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

# 4. Methods Overriding:

## create method:

- to override the create method use the following code block.

```
@api.model_create_multi
def create(self, vals):
    # peform your action here.
    return super(HospitalPatient, self).create(vals)
```

- vals: the record values that you can update before saving the record.

# 5. Sequential value:

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

# 6. Group by and filters:

### it's a way of filtering the records or grouping them by a field.

### to add a filter or group by follow the code:

```
<record id="hospital_management.hospital_patient_search" model="ir.ui.view">
    <field name="name">hospital.patient.search</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <search>
            <!-- when filtering, filter for name or ref in the same time without the user choosing which one to filter for! -->
            <!-- | means or -->
            <field name="name" filter_domain="['|', ('name', 'ilike', self), ('ref', 'ilike', self)]"/>
            <field name="age"/>

            <!-- to add a default filter in the Filters dropdown -->
            <filter string="Female" name="filter_female" domain="[('gender', '=', 'female')]"/>
            <filter string="Other" name="filter_other" domain="[('gender', '=', 'other')]"/>
            <separator/> <!-- used as an and operator in the search-->
            <filter string="is child" name="filter_child" domain="[('is_child', '=', True)]"/>

            <!-- to add a default group filter in the group by dropdown -->
            <group expand="0" string="Group By">
                <filter string="Gender" name="group_by_gender" context="{'group_by': 'gender'}"/>
                <filter string="Name" name="group_by_name" context="{'group_by': 'name'}"/>
            </group>
        </search>
    </field>
</record>
```

## Adding a default group by or filter:

### add the following field in the action record:

1. group by one level.

- write `search_default` then the name of the group by that you created ex: `group_by_gender` for group by or `name` for filter.

```
<field name="context">{'search_default_group_by_gender': 1}</field>
```

2. add more default group by:

```
<field name="context">{'search_default_group_by_gender': 1, 'search_default_group_by_name': 1}</field>
```

# 7. Adding Domains: 
### domain is a conditional filter that is add in the action record.

### age is the field name and 18 is the value and &lt;= is the operator.

### - Domain with one field: 
```
<field name="domain">[('age', '&lt;=', '18')]</field>
```
### - Domain with one field and or operator: 
```
<field name="domain">['|',('age', '&lt;=', '18'), ('gender', '=', 'male')]</field>
```
### - Domain with one field and 'and' operator: 
```
<field name="domain">[('age', '&lt;=', '18'), ('gender', '=', 'male')]</field>
```
# 8. Context:
## set default value for field in the context.
### add the following context field in the action record.
### write default_  followed by the field name then colon then the value.
```
<field name="context">{'default_gender': 'male'}</field>
```
### add default value for more than one field.
```
<field name="context">{'default_gender': 'male', 'default_age': 18}</field>
```