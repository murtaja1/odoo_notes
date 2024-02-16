# Errors & Solutions:

### field 'company_id' used in domain of field is restricted to the group(s) base.group_multi_company:
```
https://stackoverflow.com/questions/76209128/error-field-is-restricted-to-the-groups

<field name="company_id" invisible="1" groups="base.group_multi_company"/>
<field name="company_id" invisible="1" groups="!base.group_multi_company"/>
```