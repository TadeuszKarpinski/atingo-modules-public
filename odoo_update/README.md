![Banner](static/description/images/banner.png?raw=true "Banner")

Odoo Update
------------------------------
With this module developer can update install and uninstall modules from command line. Module should be loaded from default config, or placed directly in odoo addons.

Update:

Update single module
```
python odoo-bin update --module=crm
```

Update multiple modules
```
python odoo-bin update --modules=crm,sale
```

Update modules with their dependencies
```
python odoo-bin update --modules=crm,sale --with-depends
```

By default base in never updated. Add --with-base to update with base
```
python odoo-bin update --modules=crm,sale --with-depends --with-base
```

Update apps list
```
python odoo-bin update --list
```

This module added extra **post_update_hook**, which can be used in any module updated with this command. Example can be found inside.

Install:

Install single module
```
python odoo-bin install --module=crm
```

Install multiple modules
```
python odoo-bin install --modules=crm,sale
```

Uninstall:

Uninstall single module
```
python odoo-bin uninstall --module=crm
```

Uninstall multiple modules
```
python odoo-bin uninstall --modules=crm,sale
```

By default user must confirm uninstallation. Confirmation can be skipped
```
python odoo-bin uninstall --modules=crm,sale --force
```

In case of any questions don't hesitate to email me: tadeusz.karpinski@gmail.com

Screenshots
------------------------------

Screenshot 1

![Screenshot 1](static/description/images/screenshot1.png?raw=true "Screenshot 1")

Screenshot 2

![Screenshot 2](static/description/images/screenshot2.png?raw=true "Screenshot 2")

Screenshot 3

![Screenshot 3](static/description/images/screenshot3.png?raw=true "Screenshot 3")
