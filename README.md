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

## Hide a menu:

### to hide a menu do the following:

```
<delete model="ir.ui.menu" id="<module_name.menu_id>"></delete>
ex:
<delete model="ir.ui.menu" id="hr_appraisal.menu_hr_appraisal_goal"></delete>
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

## `Server Actions`:

it is a button action that is added to the action tab in the form or list view.

### `note`: to check it in UI and if the action was added go to `settings>technical>server actions`

to add a server action follow these steps:

1. create an action record.

```
<record id="<action id>" model="ir.actions.server">
    <field name="name"><button title></field>
    <field name="type">ir.actions.server</field>
    <field name="model_id" ref="model_<model_name>"/>
    <field name="binding_model_id" ref="model_<model_name>"/>
    <field name="state">code</field>
    <field name="code">records.<method_name>()</field>
</record>
```

- `binding_model_id`: to make the button visible in the action tab.
- `state=code`: means I will write python code.
- `records`: if more than one record selected in the `tree view`.

to add a server action that calls an action from `xml file`.

```
<record id="<action id>" model="ir.actions.server">
    <field name="name"><button title></field>
    <field name="type">ir.actions.server</field>
    <field name="model_id" ref="model_<model_name>"/>
    <field name="binding_model_id" ref="model_<model_name>"/>
    <field name="state">code</field>
    <field name="code">
    if record:
            action_values = env.ref('module_name.<action_id>').sudo().read()[0]
            action_values.update({'context': env.context})
            action = action_values
    </field>
</record>
```

## Url Action:

### to open new url in odoo.

1. create a button of type object.
2. then return the following code in the python method:

```
def action_Url(self):
    return {
        'type':'ir.actions.act_url',
        'target':'new',
        'url': <url>
    }
```

- `'target':'new'or'self',`: target can be `new` to open in new tab, or `self` to open in the same tab.

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

## 3. Smart Buttons:

### it's a button that has title and icon and value that can be either `action or object button`.

```
<div class="oe_button_box" name="button_box">
    <button name="<%(action_id)d>or<method_name>" type="<button type>" class="oe_stat_button" icon="fa-calendar">
        <field name="<field_name>"/>
        <span class="o_stat_text"><title></span>
    </button>
</div>
```

# 3. fields and attributes:

## Views Attributes (XML):

### `sample="1"`: an attribute that's add to the `form or kanban` views to show sample data.

### `optional="show" or "hide"`: added to the tree field to either show or hide the field, to make the field dynamic and let the user check or uncheck to show the field.

### `default_order="<field_name>,<field_name>... desc or asc"`: add in the kanban or tree... to order the records.

### `multi_edit="1"`: added to `tree view` to enable editing more than one record at the same time.

### `attrs="{'readonly': [('state', 'in', ('done','cancel','sale'))]}"`: make a field or element conditionally readonly.

### `options="{'no_create_edit':True}"`: added to `Many2one` field and used to disable create and edit option if the record does not exits.

### `options="{'no_create':True}"`: added to `Many2one` field and used to disable create option if the record does not exits.

### `options="{'no_open':True}"`: added to `Many2one` field and used to make the field unclickable (you can't go the field record) option if the record does not exits.

### `options="{'color_field': '<field_name that has the color which is integer>'}"`: to show color of tags.

### `widget="radio" options="{'horizontal': true}"`: added to selection field to make the field radio selection.

### `groups="<group_id>"`: add to elements to restrict them to a particular group only.

### `groups="base.group_no_one"`: to make the field only visible in developer mode.

### `password`: to make a password like field.

### `decoration-success="field_name == 'value'" decoration-info="" decoration-warning=""`: added with `widget="badge"` to a field to give the field states color for the badge.

## Fields Attributes:

### `tracking=True`: means log any change to this field in the chatter.

### `copy=False`: to not copy when clicking the duplicate method to copy the record.

### `expand="1"`: added in the `tree view` to expand the `group by` by default.

### `ondelete={'<selection_name>': 'cascade' or 'set null' or 'set default'}`: add to selection field so when uninstalling the module when specifying `cascade` the record that has this value will be deleted, `set null` will be set to null, `set default` will be set the field default value.

### `selection_add=[('test', 'Test')]`: used to add another option to an existing `selection field`.

### `selection_add=[('test', 'Test'), ('service',)]`: here it means you need to put the test option before the service option (changing the position visibility).

## fields:

### `Many2many field`: create a model and link it in your model like this:

```
tag_ids = fields.Many2many('<model_name>', string="Tags")
```

### `many2one field`: like a selection field with data from another model:

used like:

```
responsible_id = fields.Many2one('res.partner', string="Responsible")
```

### `related='patinet_id.age'`: is an attribute that's added to a related field an that takes its value from a field in the model of `many2one field`. the `age` field is related to another `age` field in another model.

```
age = fields.Integer(tracking=True, related='patient_id.age')
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

## `One2many field:`

### it's a relational field that contains the ids of other model related its model.

1. add a `Many2one` field to the model that you to relate to.

```
appointment_id = fields.Many2one('<model name that has the One2many field>')
```

2. add the `One2many` field in your model, end the name with `_ids`.

```
medicine_line_ids = fields.One2many('<model name>','appointment_id',string="Medicine Lines")
```

### you can add it in the notebook:

```
<page name="medicine_lines" string="Medicine Lines">
    <field name="medicine_line_ids">
        <tree editable="bottom">
            <field name="name"/>
            <field name="qty"/>
        </tree>
        <form>
            <group>
                <group>
                    <field name="name"/>
                </group>
                <group>
                    <field name="qty"/>
                </group>
            </group>
        </form>
    </field>
</page>
```

- `editable="top" or "bottom"`: added to tree view to make the lines editable without opening the form view. `top` means create new record at the top, `bottom` is the opposite.
- `create="0"`: added to tree view to prevent the user from creating new records.
- `delete="0"`: added to tree view to prevent the user from deleting the records.
- `edit="0"`: added to tree view to prevent the user from updating the records.

### `note`: if there is a view related to the model and you don't add a view in the notebook then that view will be uses.

## `active = fields.Boolean(string="Active", default=True)`:

### it's a special in odoo that is used to add the options `archive and unarchive` records.

### to the options in the view form, you need to add the field there and make it invisible

```
<field name='active' invisible="1" />
```

### `note for relation fields`: when you choose many tags in the same field then it's `Many2many`, when it's dropdown then it's `Many2one`, when it's lines then `One2many`.

### `Json Field`: it's a dictionary field like `analytic_distribution` field in `accounting in journal entries in journal items`.

### to update the field or set it, do the following:

```
analytic_account = fields.Many2one('account.analytic.account','Analytic')

def write(self, vals):
    if vals.get('analytic_account'):
        vals['analytic_distribution'] = {vals.get('analytic_account'): 100}
    return super(AccountMoveLine, self).write(vals)

@api.model_create_multi
def create(self, vals):
    for val in vals:
        if val.get('analytic_account'):
            val['analytic_distribution'] = {
                val['analytic_account']: 100
            }

    return super(AccountMoveLine, self).create(vals)
```

### Here I'm creating new field and set the value of json based on the `analytic_account`:

### setting the value like: analytic_distribution =

# 4. Methods:

## `create method:`

- to override the create method use the following code block.

```
@api.model_create_multi
def create(self, vals):
    # peform your action here.
    return super(HospitalPatient, self).create(vals)
```

- vals: the record values that you can update before saving the record.

## `onchange method`

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

## `default_get method:`

### it's a method that gets called when clicking on `create button` (not save button) to create a new record.

```
@api.model
def default_get(self, fields_list):
    res = super(HospitalPatient, self).default_get(fields_list)
    res['age'] = 10
    return res
```

### `res` is python dict.

## `copy method`:

### it's a method that gets called when clicking the `duplicate` button.

```
def copy(self, default=None):
    default = default or {}
    if not default.get(<field name>):
        default[<field name>] = _("%s (Copy)", self.<field name>)
    default[<field name>] = 'this record is copied!'
    return super(<class name>, self).copy(default)
```

## `unlink (delete) method`:

```
def unlink(self):
    if self.state == 'done':
        raise ValidationError(_('you can\'t delete this record because it is in done state!'))
    return super(HospitalAppointment, self).unlink()
```

## `write method`:

### to update a record use the write method:

```
def write(self, vals):
    # action
```

### to update a record:

```
self.<record_name>.write({'<field_name>': <value>})
```

## `method with constrains decorator`:

### used to prevent the user from doing something wrong, and gets called when saving the record.

```
@api.constrains(<field name>, <field name>)
def _check_child_age(self):
    for rec in self:
        # action
```

## `name_get method`:

### used when you need to make the title of the record consist of more than one field or different field other than `name field` in form view or when choosing a record in `many2one field`.

```
def name_get(self):
    res = []
    for rec in self:
        name = '[' + rec.<field name> + ']' + ' ' + rec.<field name>
        res.append((rec.id, name))
    return res
```

## `Overriding existing method and keeping its original functionality':

```
def action_cancel(self):
    # Call the parent method using super to keep the original functionality
    res = super(CustomSaleOrder, self).action_cancel()

    # Add your custom code here

    return res
```

## `Overriding existing method without keeping its original functionality':

```
def action_cancel(self):
    # Add your custom code here
```

- `Note`: you must add the appropriate module in the `depends` in the `__manifest__.py` file for this to work.

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

# 6. Group by and filters and Search:

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

## `SearchPanel`:

### it's a sidebar that's used to filter and search the records based on `many2one, selection` fields.

```
<searchpanel>
    <field name="state" string="Status" enable_counters="1"/>
    <field name="gender" string="Gender" select="multi" icon="fa-users"/>
</searchpanel>
```

- `enable_counters="1"`: used to show the number of the records.
- `select="multi"`: to enable selection of more than one choice.

# 7. Adding Domains:

### domain is a conditional filter that is add in the action record.

### age is the field name and 18 is the value and &lt;= is the operator.

### Domain with one field:

```
<field name="domain">[('age', '<=', '18')]</field>
```

### Domain with one field and `or` operator:

```
<field name="domain">['|',('age', '<=', '18'), ('gender', '=', 'male')]</field>
```

### Domain with one field and `and` operator:

```
<field name="domain">[('age', '<=', '18'), ('gender', '=', 'male')]</field>
```

### if you want to use both operators:

```
<button id="validate_closing_control" name="action_pos_session_closing_control" type="object" string="Close Session & Post Entries" states="closing_control"
                            attrs="{'invisible': [ '|', '&',('state', '!=', 'closing_control'), ('rescue', '=', False),
                                '&',('state', '=', 'closed'), ('rescue', '=', True)]}"
                    class="oe_highlight"/>
```

# 8. Context:

## - set default value for field in the context.

### add the following context field in the `action record`.

### write `default_` followed by the field name then colon then the value.

```
<field name="context">{'default_gender': 'male'}</field>
```

### add default value for more than one field.

```
<field name="context">{'default_gender': 'male', 'default_age': 18}</field>
```

## - hide field based on the context.

### add the following field in the `action record`.

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

## `Active_id`

### it is a special variable in Odoo that is used to represent the ID of the currently selected record or object in a view or form.

- in python code you can access like this:

```
self._context.get('active_id')
```

- in python code you can access like this:

```
<field name="context">{'default_<field_name>': active_id}</field>
```

## context with name_get method:

### using context you can specify whether `rec_name` has a code or not.

1. add an attribute `context="{'<whatever>': True}"`.
2. use this field a condition like:

```
def name_get(self):
    res = []
    for rec in self:
        if not self.env.context.get('<whatever>'):
            name = '[' + rec.ref + ']' + ' ' + rec.name
        else:
            name = rec.name
        res.append((rec.id, name))
    return res
```

# 9. Access Rights and Record Rules (Security):

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

## `Create Groups`.

### if you add this group to your model or element then only those who are inside this group can access that model or element.

1. create file named `security.xml` in the `security` folder and add it in the `__manifest__.py`.
2. in `security.xml` file create a `category` for the `groups`:

```
<record model="ir.module.category" id="module_category_<id>">
    <field name="name"><name></field>
    <field name="sequence">60</field>
</record>
```

3. create your `groups`:

```
<record model="res.groups" id="group_<id>">
    <field name="name"><name></field>
    <field name="category_id" ref="<category_id>"/>
</record>
```

### `note`: you can use this `group_id` in your `ir.model.access.csv` file in `group_id` section to set the group for your model.

### you can inherit a group using `implied_ids`:

- add this field inside the group record.

```
<field name="implied_ids" eval="[(4, ref('<group_id>'))]"/>
```

### `note`: everything the original group has, the new group will have.

## Record Rule:

### it's a rule that's added to a model that only lets a group access some records based on a condition (records inside a model and not the whole model).

```
<record model="ir.rule" id="<id>">
    <field name="name"><name></field>
    <field name="model_id" ref="model_<model_name>"/>
    <field name="domain_force">[('<field_name','=',<value>)]</field>
    <field name="groups" eval="[(4, ref('<group_id>'))]"/>
    <field name="perm_write" eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="0"/>
    <field name="perm_read" eval="1"/>
</record>
```

# 10. Views.

## `Form View Template`

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

## `Notebook and pages`:

- it's added inside the `form view`.

```
<notebook>
    <page name="doctor_prescription" string="Prescription">
        <field name='prescription' />
    </page>
    <page name="doctor_medicine" string="Medicine">
    </page>
    <page name="doctor_other_info" string="Other Info">
        <field name='note' />
    </page>
</notebook>
```

## `Tree View Template`

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

## `Kanban View Template`

- add the fields first.
- then add the fields inside the `template`.
- `records_draggable="0"`: to disable drag and drop that changes state.

```
<record id="hospital_management.hospital_appointment_kanban_view" model="ir.ui.view">
    <field name="name">hospital.appointment.kanban</field>
    <field name="model">hospital.appointment</field>
    <field name="arch" type="xml">
        <kanban records_draggable="0">
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

## `Activity View`:

### add a `activity` inside the `view_mode` in the action, then:

```
<record id="hospital_patient_view_activity" model="ir.ui.view">
    <field name="name">hospital.patient.view.activity</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <activity string="Patients">
            <field name="id"/>
            <field name="name"/>
            <templates>
                <div t-name="activity-box">
                    <img t-att-src="activity_image('hospital.patient', 'image', record.id.raw_value)"
                        t-att-title="record.id.value" t-att-alt="record.id.value"/>
                    <field name="name"/>
                </div>
            </templates>
        </activity>
    </field>
</record>
```

### `note`: define the field before using them in the template, and use the `id` of the record in image with the name of the image field you defined.

## `Search View Template`

```
<record id="hospital_management.hospital_patient_search" model="ir.ui.view">
    <field name="name">hospital.patient.search</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <search>
            <field name="name" filter_domain="['|', ('name', 'ilike', self), ('ref', 'ilike', self)]"/>
            <group expand="0" string="Group By">
                <filter string="Gender" name="group_by_gender" context="{'group_by': 'gender'}"/>
                <filter string="Name" name="group_by_name" context="{'group_by': 'name'}"/>
            </group>
        </search>
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

## Mandatory Field not set..:

### means the form is missing a requried field.

### Menu not visible reasons:

- file not added in the `__manifest__.py` file.
- `access rights` not set. check this by becoming `superuser`.
- if a menu is not a parent menu and doesn't have an action then it will be invisible.

### ValueError: product.template.detailed_type: required selection fields must define an ondelete policy that implements the proper cleanup of the corresponding records upon module uninstallation. Please use one or more of the following policies: 'set default' (if the field has a default defined), 'cascade', or ....

### when receiving such error, you need to use the `ondelete attribute`

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

### `_rec_name = 'field name'`: it's what will be shown in the header title and in the `many2one` field.

### `_order="<field_name>,<field_name>... desc or asc"`: to order the records.

# 15. Database Operations:

## create a new record:

```
self.env[<model_name>].create(<dict of the values>)
```

# 16. Inherit and add to existing Module:

## `add or override an attribute to an already exiting field:`

```
<xpath expr="//field[@name='field_name']" position="attributes">
    <attribute name="attrs">{'readonly': [('state', 'in', ('done','cancel','sale'))]}</attribute>
    # or
    <attribute name="decoration-success">invoice_status == 'refunded'</attribute>
</xpath>
```

### add the module as a `depend` in `__manifest__.py` file.

## `Add menu to existing Module`:

- get the `external id or xml id` by going to `setting>technical>menu items` and search for the menu.
- add the `id` as the `parent` of the menu.

```
<menuitem id="sale_appointments_menu" name="Appointments"
parent="sale.sale_order_menu" action="hospital_management.hospital_appointment_action" sequence="20"/>
```

## `Add new field to existing Module`:

1. add the field to the model.

```
class SaleOrder(models.Model):
    # we are only inheriting and not creating new model
    _inherit = 'sale.order'

    sale_description = fields.Char()
```

2. add it to the form view record.

```
<record id="sale_order_description_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.inherited</field>
    <field name="model">sale.order</field>
    <!-- ref = the form view 'External ID'-->
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- you can use either the field or xpath to add to an inherited form view -->

        <!-- means after the partner_id field -->
        <!-- <field name="partner_id" position="after">
            <field name='sale_description'/>
        </field> -->

        <!-- means there is a field name partner_id -->
        <!-- you can also add after a div tag or anything instead of field -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="sale_description"/>
        </xpath>
    </field>
</record>
```

### if there is two field or elements in the same view or element, then you can access the first or second one... like this:

```
<xpath expr="//div[@class='o_td_label'][2]" position="attributes">
    <attribute name="attrs">{'invisible': [('state', 'in', ['sent'])]}</attribute>
</xpath>
```

### `[2]`: the number of the element, can be any number [1] or [2]...

### add it to the tree view record.

```
<record id="sale_order_description_tree_inherit" model="ir.ui.view">
    <field name="name">sale.order.inherited</field>
    <field name="model">sale.order</field>
    <!-- ref = the tree view 'External ID'-->
    <!-- get the 'External ID' by clicking the arrow of Inherited View to go to the main tree view -->
    <field name="inherit_id" ref="sale.view_quotation_tree"/>
    <field name="arch" type="xml">
        <!-- you can use either the field or xpath to add to an inherited form view -->

        <!-- means there is a field name partner_id -->
        <!-- you can also add after a div tag or anything instead of field -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="sale_description"/>
        </xpath>
    </field>
</record>
```

## `Position Move`:

### used to move fields or elements:

```
 <xpath expr="//field[@name='phone']" position="before">
                <field name="email" position='move'/>
            </xpath>
```

## `Hiding a print button from view`:

### to hide from the UI: go to `settings>technical>reporting>reports` then search the name of the report action. and click `hide from menu`.

### from the code:

```
<record id="<external_id or xml_id>" model="ir.actions.report">
    <field name="binding_model_id" eval="False" />
</record>
```

## to override an existing inherited method:

1. import the file where the method is written.
2. override the method by creating the method with the same name.
   or
3. import the class where the method is defined and call it with your new method, like:

```
from odoo.addons.sale.models.sale_order import SaleOrder as OdooSaleOrder

def _unlink_except_draft_or_cancel(self):
    res = super(SaleOrder,self).unlink()
    # action
    return res

OdooSaleOrder._unlink_except_draft_or_cancel = _unlink_except_draft_or_cancel
```

### `note` where reassigning odoo's original method with our new overridden method.

# 17. PDF Reports:

### to create a report follow these steps:

1. create `report` folder and inside it a `report.xml` file.
2. add your `action` so a `print button` appears.
3. add the file (`report.xml`) in `__manifest__.py` file at the last of `data` section.

```
<record id="<model name>.<id>" model="ir.actions.report">
    <field name="name"><button title></field>
    <field name="model"><model name></field>
    <field name="binding_model_id" ref="model_<model name with _ and not .>"/>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">addon folder name.<template id></field>
    <field name="report_file">addon folder name.<template id></field>
    <field name="binding_type">report</field>
    </record>
```

### `note`: to check if the action was added go to `settings>technical>Reports`

4. create your `report template` in `report` folder and add it in `__manifest__.py` file at the last of `data`.

```
<template id="<template id>">
    <t t-call="web.html_container"/>

    <!-- <t t-call="web.external_layout">
            <div class="page">

            </div>
        </t> -->
    <t t-foreach="docs" t-as="o">
        <t t-call="web.basic_layout">
            <div class="page">
                <div class="oe_structure">
                    <div class="row">
                        <div class="col-xs-8">
                            <table class="table table-condensed" style="border: 3px solid black !important">
                                <tr>
                                    <td width="40%">
                                        <p style="text-align:center;padding-top:10px">
                                            <img t-if="not o.image" t-att-src="'/web/static/src/img/placeholder.png'" height="140" width="120" border="1" />
                                            <!-- <img t-if="o.image" t-att-src="'data:image/png;base64,%s' % to_text(o.image)" height="140" width="120" border="1" /> -->
                                            <img t-if="o.image" t-att-src="image_data_uri(o.image)" height="140" width="120" border="1" />
                                        </p>
                                    </td>
                                    <td width="60%">
                                        <table>
                                            <tr>
                                                <td colspan="3" class="text-center">
                                                    <span t-field="o.name"/>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <span>
                                                        <strong>Age:</strong>
                                                    </span>
                                                </td>
                                                <td>
                                                    <span>:</span>
                                                </td>
                                                <td>
                                                    <span t-field="o.age"/>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <span>
                                                        <strong>Reference:</strong>
                                                    </span>
                                                </td>
                                                <td>
                                                    <span>:</span>
                                                </td>
                                                <td>
                                                    <span t-field="o.ref"/>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <t t-if="o.appointment_ids">
                        <span>Appointment Details</span>
                        <table class="table table-sm o_main_table" name="appointment">
                            <thead>
                                <tr>
                                    <th name="th_reference" class="text-left">
                                        <span>Reference</span>
                                    </th>
                                    <th name="th_age" class="text-left">
                                        <span>Age</span>
                                    </th>
                                    <th name="th_doctor" class="text-left">
                                        <span>Doctor</span>
                                    </th>
                                </tr>
                            </thead>
                            <t t-set="appointment_count" t-value="0"/>
                            <t t-foreach="o.appointment_ids" t-as="line">
                                <t t-set="appointment_count" t-value="appointment_count + 1"/>
                                <tr>
                                    <td>
                                        <span t-field="line.ref"/>
                                    </td>
                                    <td>
                                        <span t-field="line.age"/>
                                    </td>
                                    <td>
                                        <span t-field="line.doctor_id.name"/>
                                    </td>
                                </tr>
                            </t>
                            <tr>
                                <td colspan="2">
                                    <strong>Total Appointments</strong>
                                </td>
                                <td>
                                    <t t-esc="appointment_count"/>
                                </td>
                            </tr>
                        </table>
                    </t>
                </div>
            </div>
        </t>
    </t>
</template>
```

- `t-call="web.basic_layout"`: a layout that you can create from scratch.
- `t-call="web.external_layout"`: a layout that has header and footer built-in.
- `t-foreach="docs" t-as="o"`: looping over the records and using `o` as the variable.
- `t-if="<python code>"`: use to check if certain condition is met like whether a field has a data or not.
- `t-att-src="image_data_uri(o.<field name>)" or <img t-if="o.image" t-att-src="'data:image/png;base64,%s' % to_text(o.<field name>)" height="140" width="120" border="1" />`: add an image.
- `t-field="o.<field name>"`: add the field in your model.
- `t-esc="<python code>or<field name>"`: type python code or field name too.
- `t-set="<var name>" t-value="<value>"`: declare a variable and its value.

### `Note`: you can access Pdf report from UI from `http://<server-address>/report/html/sale.report_saleorder/38`

## `Report form Wizard`:

### follow the same steps above with:

1. create a menu.
2. create the model `TransientModel` and add its access rights and a method to pring the report.

```
def action_print_appointment(self):
    domain = []
    patient_id = self.patient_id
    date_from = self.date_from
    date_to = self.date_to

    if patient_id:
        domain += [('patient_id','=', patient_id.id)]
    if date_from:
        domain += [('date','>=', date_from)]
    if date_to:
        domain += [('date','<=', date_to)]

    appointments = self.env['hospital.appointment'].search_read(domain)
    data = {
        'form_data': self.read()[0],
        'appointments': appointments
    }
    return self.env.ref(<the report action id in the report folder>).report_action(self, data=data)
```

2. create file in the wizard that contains the the form and the action just like in the `Wizard` section.
3. add a button in the `form` that calls the method form the `TransientModel` model.

### `note`: you can access `data` that contains 'form_data' and 'appointments' in the report file.

- `self.read()[0]` is the current record.
- `search_read(domain)` used to get readable data instead of just `search` method that gets record set.

## `Report form Wizard Using Parser`:

### same steps taken to create `Report form Wizard` with:

1. create a model inside `report` folder.
2. instead of handle the logic inside the `TransientModel` model, do it inside the following model.

```
class AllPatientReport(models.AbstractModel):
    _name = "report.hospital_management.all_patient_details_report_template"
    _description = "report.hospital_management.all_patient_details_report_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        age = data.get('form_data').get('age')
        gender = data.get('form_data').get('gender')
        if age != 0:
            domain += [('age','=',age)]
        if gender:
            domain += [('gender','=',gender)]
        docs = self.env['hospital.patient'].search_read(domain)

        return {
            'docs': docs,
            'search': {'age': age, 'gender':gender}
        }
```

- `_name`: the name of this model consists of `report.<module_name>.<report_template_id>`
- `_get_report_values` a method that gets called when printing the reprot.
- all the return data from this `_get_report_values` will be used in report template
- `docids`: the selected record id if it gets called from a record.
- `data`: data that comes from the wizard through the `TransientModel` model.

# 17. Odoo Urls:

- create new database
  `http://localhost:8069/web/database/manager`

# 18. Widgets:

### they are used for style mostly.

## `Banner or Ribbon widget`:

```
<widget name="web_ribbon" bg_color="bg-danger" title="Archived" attrs="{'invisible': [('active','=',True)]}"/>
```

## `widget="many2many_tags"`: added to tags model, used to let you style set color of tags.

# 19. Cron Job (Scheduled Action):

### it's a record that calls a python method as request without the user intervening (automation).

- to check the cron job in the UI go to `settings>technical>Automation>Scheduled Action`
- to create a cron job follow these steps:

1. create an xml file in `data folder`.

```
<record id="<id>" model="ir.cron">
    <field name="name"><name></field>
    <field name="model_id" ref="model_<model_name with underscore>"/>
    <field name="state">code</field>
    <field name="code">model.method_name()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
</record>
```

- `code`: add your method name from your model that's specified in model_id.
- `interval_number`: how many times the cron job will run per the specified interval.
- `interval_type`: can be minutes or hours or days or months.
- `numbercall`: how many times the method is called. `-1` means forever.

# 20. Send an Email and Notifications:

## `send an email`

### in `data` folder create `mail_data.xml` file and add the following:

```
<record id="email_template_for_manager_approval_expense_report" model="mail.template">
    <field name="name">Expense Report: Report Approvel</field>
    <field name="model_id" ref="sh_expense_dynamic_approval.model_hr_expense_sheet" />
    <field name="subject">Expense Report Approvel</field>
    <field name="email_from"></field>
    <field name="partner_to"></field>

    <field name="body_html" type="html">
        <div style="margin: 0px; padding: 0px;">
            <p style="margin: 0px; padding: 0px; font-size: 13px;">
                This is inform you that the expense report is waiting your approval!<br />
                You can use the following link to access the expense report.<br /><br />
                <div style="display: inline-block; margin: 15px; text-align: center">
                    <a t-att-href="'/mail/view?model=hr.expense.sheet&res_id=%s'%object.id" target="_blank"
                        style="padding: 5px 10px; color: #FFFFFF; text-decoration: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius: 3px"
                    >Expense Report Ref: #<t t-out="object.name or ''" /></a>
                </div><br />
                Thanks.
            </p>
        </div>
    </field>
</record>
```

### in your model add the following:

```
template_id = self.env.ref(
        "sh_expense_dynamic_approval.email_template_for_manager_approval_expense_report")
if template_id and self.user_id:
    template_id.sudo().send_mail(self.id, force_send=True, email_values={
        'email_from': self.env.user.email, 'email_to': self.user_id.partner_id.email})
```

## `send a notification`:

### most reliable one:

```
self.message_post(
                body="<text>",
                message_type='notification',
                subtype_id=self.env.ref('mail.mt_comment').id,
                partner_ids=[<partner_ids>],
            )
```

### to send a notification add the following code in your model:

```
notifications = []
if self.user_id:
    notifications.append(
                (self.user_id.partner_id, 'sh_notification_info',
                {'title': _('Notitification'),
                    'message': 'The Expense Report %s is waiting your approval!' % (self.name)
                }))

    self.env['bus.bus']._sendmany(notifications)
```

# 21. Database:

### login to database:

`$ psql -U admin -d <database_name> `

### write the password as `admin`

### to update the password of the Odoo user, type the following command:

`UPDATE res_users set password='admin',login='admin' where id=2;`

# 21. Odoo Configuration:

### to generate a Journal Entry from Inventory transfer:

- go to `Product` then in product `General Information` tab, click on `Product Category`.
- set the `Costing Method` to `Average Cost (AVCO)` and `Inventory Valuation` to `Automated`

# How to

### get users by group id.

```
users = self.env.ref('itsys_real_estate.group_real_estate_manager_discount_approval').users
```

### Create an invoice:

```
def make_invoice(self):
    for rec in self:
        account_move_obj = self.env['account.move']
        journal_pool = self.env['account.journal']
        journal = journal_pool.search([('type', '=', 'sale')], limit=1)
        product_id = self.env['product.template'].search([('detailed_type', '=', 'service')], limit=1)
        if not product_id:
            raise UserError(_('There is no service product!'))
        invoice_line_ids = []
        invoice_line = {
                            'name': ('Delivery Service'),
                            'quantity': 1,
                            'product_id': product_id.product_variant_id.id,
                            'price_unit': rec.delivery_cost
                            }
        invoice_line_ids.append((0, None, invoice_line))

        invoice= account_move_obj.create({'ref': rec.ref, 'journal_id': journal.id,
                                    'currency_id': rec.currency_id.id,
                                    'partner_id': rec.receiver_id.id,
                                    'move_type': 'out_invoice',
                                    'invoice_date_due': rec.actual_delivery_date,
                                    'invoice_line_ids': invoice_line_ids,
                                    })
        invoice.action_post()
        self.invoice_id = invoice.id
```

### Create a (monetary) Currency Field:

```
def _default_currency(self):
    return self.env.user.company_id.currency_id
currency_id = fields.Many2one('res.currency', string='Currency', default=_default_currency)
cost = fields.Monetary(string='Value')
```

### get data from backend

```
	var rpc = require("web.rpc");

rpc.query({
    model: "product.product",
    method: "search_read",
    args: [[["id", "=", id]], ["field_service"]],
})
.then(function (partners) {
    // Process the fetched data
    console.log(partners);
    return partners
});
```

### extend Odoo's database expiration date:

1. open inspector and hover over the whole page.
2. remove the style that makes Odoo unclickable.
3. go to `settings/technical/Parameters/System Parameters`.
4. edit or create a record with the name `database.expiration_date`.
   - add date with this format `YYYY-MM-DD HH:MM:SS` ex. `2222-1-1 10:10:10`.

### To access an element that has no id or name:

1. open the view with browser inspector.
2. go to the element and click copy then copy XPath.

### Create Time field:

1. create a float field.
2. add widget="float_time" in xml.

### Upgrade module from CMD:

- `odoo -c /etc/odoo/odoo.conf -d database_name -u module_name`

### Server Setup:

1. update server and install nginx:

```
sudo apt update
sudo apt install nginx
```

2. Configure Nginx for Odoo:

```
sudo nano /etc/nginx/sites-available/odoo

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

- restart Odoo Service:

```
sudo systemctl status odoo
sudo systemctl restart odoo
```

3. Enable the Configuration:

```
sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled
sudo service nginx reload
```

4. DNS Configuration:
   Update your DNS records to point your custom domain (your-domain.com) to the IP address of your server.

### Get all the users that belong to a group Odoo15:

```
self.env.ref("model.group_id").users.ids
```

### Add label to field:

```
<label for="total_progression"/>
<div class="o_row" style="width: 55px !important">
    <field name="total_progression" readonly="1" force_save="1"/>
    <span>%%</span>
</div>
```

### Send notification to group with users:

```
hr_user_ids = self.env.ref("module.id").users
            for user in hr_user_ids:
                partner_ids.append(user.partner_id.id)
            self.message_post(
                    body="You have an overtime request to approve!",
                    message_type='notification',
                    subtype_id=self.env.ref('mail.mt_comment').id,
                    partner_ids=partner_ids,
                )
```

### add Pdf or image previewer:

- add after the sheet tag.

```
<div class="o_attachment_preview" attrs="{'invisible': []}"/>
```

### if user has group:

```
self.env.user.has_group('sh_return_invoice_bill.group_approve_return_transfer')
```

### current user:

```
self.env.user
```

### change User Registration from portal to internal user:

- Go to Settings >> General Settings.
- In that select Free sign up option for customer account in Users section.
- And click default access right. In that you can select user type as Internal user.
- Make sure all this stuff you have to do in debug mode, otherwise you can see advanced options.
  ref: https://www.odoo.com/pt_BR/forum/ajuda-1/odoo-12-how-to-make-signup-for-internal-user-147374

### Currency Conversion:

```
def _convert_currency(self):
        for rec in self:
            rec.main_price = rec.original_currency_id.with_context(date = rec.create_date).compute(rec.price, self.env.company.target_currency_id)
```

### Change Wizard Footer:

- add the following in the wizard form:

```
 <footer>
    <button id="button_print" type="object" name="action_print_patient" string="Print" class='btn-primary'/>
    <button string="Cancel" class="btn btn-secondary" special="cancel" data-hotkey="z"/>
</footer>
```

### view image from URL:

```
http://localhost:8069/web/image?model=colorify.image.image&id=1&field=colored_image&unique=1690830299000
http://localhost:8069/web/image?model=<model.name>&id=<record_id>&field=<field_name>&unique=1690830299000
```

### Add image in report:

```

<img style="width:150px;height:150px" t-attf-src="/web/image?model=colorify.imageqr&id=1&field=qr_code" alt=""/>
```

- to used as logged in, add the header in the network widget in flutter.

### Create unique field:

```
_sql_constraints = [
						('your_field_name_unique', 'unique(your_field_name)', "Can't be duplicate value for this field!")
						]
```

### Fix PDF reports alignment:

#### this can happen due to database backup or changing the system.

1. go to `Settings/Technical/System Parameters`.
2. search for `report.url` if not there create one.
3. the `key` should be `report.url`, and the `value` should be `the domain or IP of Odoo`.

- check `https://www.youtube.com/watch?v=lC9p_QJUW1Q&list=PLqRRLx0cl0hoiTewSTzSQ3HJ-Vqhh43k0&index=4`

### Use specific view in a related field:

```
<field name="field_name_id" context="{'tree_view_ref': 'approvals.approval_product_line_view_tree', 'kanban_view_ref': 'approvals.approval_product_kanban_mobile_view'}" />
```

### Set a custom field in the configuration:

```
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_product_id = fields.Many2one('product.template', string='Discount Product') 

# used to set the value in the field
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('product_template.discount_product_id', int(self.discount_product_id.id))

# used to show the value in the field
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['discount_product_id'] = int(get_param('product_template.discount_product_id'))
        return res
##########

    <record id="res_config_settings_sale_order_discount_product_view_form" model="ir.ui.view">
        <field name="name">res.config.settings.view.form.inherit</field>
        <field name="model">res.config.settings</field>
        <field name="priority" eval="20"/>
        <field name="inherit_id" ref="sale.res_config_settings_view_form"/>
        <field name="arch" type="xml">
            <xpath expr="//div[@id='show_margins']" position="after">

                <div class="col-12 col-lg-6 o_setting_box" id="discount_product_id_field">
                    <div class="o_setting_left_pane"/>
                    <div class="o_setting_right_pane">
                        <span class="o_form_label">Discount Prodout</span>
                        <div class="text-muted">
                            Product used in the sale order discount line.
                        </div>
                        <div>
                            <field name="discount_product_id"/>
                        </div>
                    </div>
                </div>

            </xpath>
        </field>
    </record>
```

### To install external python package:

- go to python and run:

```
$ .\python.exe -m pip install <package_name>
```

### Add confirmation to button:

```
<button name="name" type="object" string="Confirm" class="btn-primary" confirm="Are you sure you want to confirm?"/>
```

### To override the search when searching in relation fields:

- use name search method.

```
@api.model
def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
    # rest of the code.
    return ids
```

### Make a computed field searchable:

- add the search attribute in the field.

```
field_name = fields.Boolean(compute="_compute_field_name", search="_search_field_name")

@api.depends("user_ids")
def _compute_field_name(self):
    for record in self:
        for user in record.user_ids:
            if user.has_group("id"):
                record.field_name = True
                break
        if not record.field_name:
            record.field_name = False

@api.model
def _search_field_name(self, args, limit=None, order=None, offset=0):
    group_id = self.env.ref("id").id
    record_ids = self.env["res.partner"].search(
        [
            (
                "user_ids.groups_id",
                "in",
                group_id,
            )
        ]
    )
    return [("id", "in", record_ids.ids)]
```

### Override action window:

```
<record id="sale.action_quotations_with_onboarding" model="ir.actions.act_window">
    <field name="domain">[('is_return_order','=', False)]</field>
</record>
```

### Specify Tree and Form views for an action:

- Add the following to the action:

```
<field name="view_ids" eval="[(5, 0, 0),
    (0, 0, {'view_mode': 'tree', 'view_id': ref('view_quotation_cut_off_tree')}),
    (0, 0, {'view_mode': 'form', 'view_id': ref('sale_order_cut_off_form_view')}),
    ]"/>
```

### Add tracking to many2many field:

- add the following method in the model after setting `tracking=True` in your field.

```
field_name = fields.Many2many('comodel_name', tracking=True)

def _mail_track(self, tracked_fields, initial_values):
    changes, tracking_value_ids = super()._mail_track(tracked_fields, initial_values)
    # Many2many tracking
    if len(changes) > len(tracking_value_ids):
        for changed_field in changes:
            if tracked_fields[changed_field]['type'] in ['one2many', 'many2many']:
                field = self.env['ir.model.fields']._get(self._name, changed_field)
                vals = {
                    'field': field.id,
                    'field_desc': field.field_description,
                    'field_type': field.ttype,
                    'tracking_sequence': field.tracking,
                    'old_value_char': ', '.join(initial_values[changed_field].mapped('name')),
                    'new_value_char': ', '.join(self[changed_field].mapped('name')),
                }
                tracking_value_ids.append(Command.create(vals))
    return changes, tracking_value_ids
```

### Close wizard when download report

```
report_action.update({'close_on_report_download': True})
```
### Use existing view in a field:
- context="{'tree_view_ref': 'approvals.approval_product_line_view_tree'}".
- ex:
```
<field name="product_line_ids" context="{'tree_view_ref': 'approvals.approval_product_line_view_tree'}"/>

```