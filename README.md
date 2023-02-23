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

## Return Action From Python Code:

### Return form view after creating a record:

```
rec = self.env[<model name>].create(<dict of the values>)
return {
    'name': _(<string>),
    'type': 'ir.actions.act_window',
    'view_mode':"form",
    'res_model':<model name>,
    'res_id': rec.id
}
```

### Return tree view:

`method 1`:

```
action = self.env.ref(<action id>).read()[0]
action['domain'] = [(<field name>,'=',self.<value>)]
return action
```

`method 2`:

```
action = self.env["ir.actions.act_window"]._for_xml_id(<action id>)
action['domain'] = [(<field name>,'=',self.<value>)]
return action
```

`method 3`:

```
return {
    'name': _(<string>),
    'type': 'ir.actions.act_window',
    'view_type':'form',
    'view_mode':"tree,form",
    'res_model':<model name>,
    'domain': [(<field name>,'=',self.<value>)]
}
```

# 2. adding a StatusBar (buttons):

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

## Adding buttons in the status bar:

### there are tow types of buttons

## 1. Object Button:

### calls a function in the model

1. we add a function in the model like:

```
def action_confirm(self):
    self.state = 'confirm'
```

2. we add a button in the form view that's related to the model, like:

```
<button id="button_confirm" type="object" name="action_confirm" string="Confirm" class='btn-primary' states="draft" confirm="Are you sure?"/>
```

- `confirm="Are you sure?"`: asking for confirmation before performing the action.
- `type="object"`: means there will be a function defined in the model to handle the button when clicked.
- `name="action_confirm"`: the name of the function in the model.
- `string="Confirm"`: the display name.
- `states="draft"`: when should this button be visible. meaning it'll be visible in draft only or you can set to states="draft,cancel,..."

## Add a button in tree view:

### same way you add it in form view but, `state` and `id` can't be add in tree view.

## 2. Action Button:

### calls an action record.

```
<button id="button_create_appointment" type="action" name="%(<action_id>)d" string="Create Appointment" class='btn-primary'/>
```

# 3. fields and attributes:

## attributes:
### `sample="1"`: an attribute that's add to the `form or kanban` views to show sample data.

tracking=True: means log any change to this field in the chatter.
used like:

```
age = fields.Integer(tracking=True)
```

## fields:

### `many2one field`: like a selection field with data from another model:

used like:

```
responsible_id = fields.Many2one('res.partner', string="Responsible")
```

### `related='patinet_id.age'`: is an attribute that's added to a related field an that takes its value from a field in the model of `many2one field`. the `age` field is related to another `age` field in another model.

```
age = fields.Integer(tracking=True, related='patinet_id.age')
```

- 'res.partner': the name of the model.

### when using `onchange` and making a field `readonly`, you have to add `force_save="1"` to save the value, like

```
<field name="gender" readonly="1" force_save="1"/>
```

### image field:

```
image = fields.Binary(string='image')
<field name="image" widget="image" class="oe_avatar"/>
```

## Compute Field:

- it's a readonly field that is calculated by a method and not the user.
- the method should start with `_compute_` and the `field name`.

```
appointment_count = fields.Integer(string='Appointment Count', compute="_compute_appointment_count")

def _compute_appointment_count(self):
    appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
    self.appointment_count = appointment_count
```

# 4. Methods:

## create method:

- to override the create method use the following code block.

```
@api.model_create_multi
def create(self, vals):
    # peform your action here.
    return super(HospitalPatient, self).create(vals)
```

- vals: the record values that you can update before saving the record.

## onchange method

```
@api.onchange('patient_id')
def onchagne_patient_id(self):
    # action
```

like:

```
@api.onchange('patient_id')
def onchagne_patient_id(self):
    if self.patient_id:
        if self.patient_id.gender:
            self.gender = self.patient_id.gender
    else:
        self.gender = ''
```

- you can add more depends in `@api.onchange` like `@api.onchange('patient_id','age')`

## default_get method:

### it's a method that gets called when clicking on `create button` (not save button).

```
@api.model
def default_get(self, fields_list):
    res = super(HospitalPatient, self).default_get(fields_list)
    res['age'] = 10
    return res
```

### `res` is python dict.

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

- `code`: it will be used in `self.env['ir.sequence'].next_by_code('hospital.patient')`.
- `noupdate="1"`: means if the user has updated it in the UI don't override it when upgrading the module.
- `prefix`: means add PH before the sequential value.
- `padding`: the length of the digits.

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

### Domain with one field:

```
<field name="domain">[('age', '&lt;=', '18')]</field>
```

### Domain with one field and `or` operator:

```
<field name="domain">['|',('age', '&lt;=', '18'), ('gender', '=', 'male')]</field>
```

### Domain with one field and `and` operator:

```
<field name="domain">[('age', '&lt;=', '18'), ('gender', '=', 'male')]</field>
```

# 8. Context:

## - set default value for field in the context.

### add the following context field in the action record.

### write `default_` followed by the field name then colon then the value.

```
<field name="context">{'default_gender': 'male'}</field>
```

### add default value for more than one field.

```
<field name="context">{'default_gender': 'male', 'default_age': 18}</field>
```

## - hide field based on the context.

### add the following field in the action record.

### `hide_` followed by field name

```
<field name="context">{'hide_gender': 1}</field>
```

### then add following attribute `invisible="context.get('hide_gender')"` in the form view in the field.

### the `context.get('hide_gender')` will be replaced by in value in the context in the action record.

### `hide_gender` is the key in the context.

```
<field name='gender' invisible="context.get('hide_gender')"/>
```

# 9. Access Rights:

## setting which user can access what.

to set access rights:

- create a security folder.
- create `ir.model.access.csv` file and add it in the `__manifest__.py` file in `data`.
- add the following inside `ir.model.access.csv`:

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

like:

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hospital_patient_user,hospital.patient,model_hospital_patient,base.group_user,1,1,1,1
```

- `id`: access_hospital_patient_user
- `model_id:id`: hospital.patient
- `group_id:id`: model_hospital_patient
- `note`: if you want to prevent user from accessing something then set `perm_read,perm_write,perm_create,perm_unlink` to `0,0,0,0` instead of `1,1,1,1` to any of them.

# 10. Views.

## Form View Template

- `header`: where we added the status bar with button.
- `sheet`: where we added the fields.

```
<record id="hospital_management.hospital_appointments_form" model="ir.ui.view">
    <field name="name">Appointments</field>
    <field name="model">hospital.appointment</field>
    <field name="arch" type="xml">
        <form string="">
            <header>
                <button confirm="Are you sure?" id="button_confirm" type="object" name="action_confirm" string="Confirm" class='btn-primary' states="draft"/>

            </header>
            <sheet>
                <div class="oe_title">
                    <h1>
                        <field name="ref" readonly='1'/>
                    </h1>
                </div>
                <group>
                    <field name="name"/>
                    <field name="description"/>
                    <field name="date"/>
                    <field name="time_checkup"/>
                </group>

            </sheet>
        </form>
    </field>
</record>
```

## Tree View Template

```
<record id="hospital_management.hospital_appointment_tree" model="ir.ui.view">
    <field name="name">hospital.appointment</field>
    <field name="model">hospital.appointment</field>
    <field name="arch" type="xml">
        <tree>
            <field name="ref"/>
            <field name="name"/>
        </tree>
    </field>
</record>
```

## Kanban View Template

- add the fields first.
- then add the fields inside the `template`.

```
<record id="hospital_management.hospital_appointment_kanban_view" model="ir.ui.view">
    <field name="name">hospital.appointment.kanban</field>
    <field name="model">hospital.appointment</field>
    <field name="arch" type="xml">
        <kanban>
            <field name="ref"/>
            <field name="name"/>
            <template>
                <t t-name="kanban-box">
                    <div t-attf-class="oe_kanban_global_click">
                        <div class="oe_kanban_details">
                            <ul>
                                <li>
                                    Ref: <field name="ref"/>
                                </li>
                                <li>
                                    Name: <field name="name"/>
                                </li>
                            </ul>
                        </div>
                    </div>
                </t>

            </template>
        </kanban>
    </field>
</record>
```

# 11. Chatter and activity:

## to add a chatter to log any change in the form or send a message or set a schedule:

- inherit `['mail.thread', 'mail.activity.mixin']` in your model.

1. `mail.activity.mixin` used to schedule an activity.
2. `mail.thread` for logs and messages.
3. add `mail` in `__manifest__.py` in `depends`:

- add the following in the form view bellow the `sheet` tag:

```
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

1. `name="message_follower_ids"`: to add followers.
2. `name="activity_ids"`: to schedule an activity.
3. `name="message_ids"`: to send a message.

# 12. Errors:

## singleton error:

### `ValueError: Expected singleton: hospital.patient(1, 2, 4, 5, 8, 14, 15)`

- reason: when adding a field in tree view and not iterating over `self`.

### instead of

```
def _compute_appointment_count(self):
        appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count = appointment_count
```

### do this

```
def _compute_appointment_count(self):
    for rec in self:
        appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',rec.id)])
        rec.appointment_count = appointment_count
```

### Menu not visible reasons:

- file not added in the `__manifest__.py` file.
- `access rights` not set. check this by becoming `superuser`.
- if a menu is not a parent menu and doesn't have an action then it will be invisible.

# 13. Wizard:

## it's a dialog that's created using `models.TransientModel`, to create a wizard:

1. create a folder named `wizard`.
2. inside `wizard`, add your model `model_name.py` and views `view_name.xml`.
3. add the model `access rights` in security.
4. add your `xml` files in the `__manifest__.py data` after the `data section`.

### the `TransientModel` is not stored in the database.

### example:

```
class CreateAppointmentWizard(models.TransientModel):
    _name = "hospital.create.appointment.wizard"
    _description = "hospital.create.appointment.wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    name = fields.Char()

    def action_create(self):
        # action
```

```
<record id="hospital_create_appointment_wizard_form" model="ir.ui.view">
    <field name="name">hospital.create.appointment.wizard.form</field>
    <field name="model">hospital.create.appointment.wizard</field>
    <field name="arch" type="xml">
        <form>
            <group>
                <field name="patient_id"/>
                <field name="name"/>
            </group>
            <footer>
                <button id="button_create" type="object" name="action_create" string="Create" class='btn-primary'/>
                <button string="Cancel" class="btn btn-secondary" special="cancel" data-hotkey="z"/>
            </footer>
        </form>
    </field>
</record>

<record id="hospital_management.hospital_create_appointment_wizard_action" model="ir.actions.act_window">
    <field name="name">Create Appointments</field>
    <field name="res_model">hospital.create.appointment.wizard</field>
    <field name="view_mode">form</field>
    <field name="view_id" ref="hospital_create_appointment_wizard_form"/>
    <field name="target">new</field>
</record>
```

`<field name="target">new</field>` used to get a popup instead of a new window

### note: the `menuItem` should not be added in the wizard, but in the views folder.

# 14. Models:

### `_rec_name = 'field name'`: it's what will be shown in the header title.

# 15. Database Operations:

## create a new record:

```
self.env[<model_name>].create(<dict of the values>)
```
