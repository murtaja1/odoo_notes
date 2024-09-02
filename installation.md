## Installing multiple instances of Odoo on windows:
1. cd into `C:\odoo\odoo_17_c\nssm\win32`.
2. run this command `nssm edit <already existing Odoo service>`.
    - copy the arguments
    - go to `log on` and copy `this account`.
3. run `nssm install <new service name>`
    - set application python to `C:\odoo\odoo_17_c\python\python.exe` or yours.
    - paste your proper arguments
    - go to `log on` and paste your account.
    - add name in `details`



ex arguments: "C:\odoo\odoo17_c\server\odoo-bin" -c "C:\odoo\odoo17_c\server\odoo.conf"
ex this account: NT Authority\LocalService