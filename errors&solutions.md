# Errors & Solutions:

### field 'company_id' used in domain of field is restricted to the group(s) base.group_multi_company:
```
https://stackoverflow.com/questions/76209128/error-field-is-restricted-to-the-groups

<field name="company_id" invisible="1" groups="base.group_multi_company"/>
<field name="company_id" invisible="1" groups="!base.group_multi_company"/>
```
### Add new Tab in general settings:
- data-key: to show the icon.
```
<record id="res_config_settings_form" model="ir.ui.view">
    <field name="name">res.config.settings.form</field>
    <field name="model">res.config.settings</field>
    <field name="inherit_id" ref="base.res_config_settings_view_form" />
    <field name="arch" type="xml">
        <xpath expr="//div[hasclass('settings')]" position="inside">
            <div class="app_settings_block" data-string="Vendor-Portal" string="Title" data-key="module_name" groups="group">
            </div>
        </xpath>
    
    </field>
</record>
```