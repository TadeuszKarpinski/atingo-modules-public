![Banner](static/description/images/banner.png?raw=true "Banner")

Odoo Test
------------------------------
With this module developer is able to run tests in easier way. With simple command "test" you are able to run single test, test class or all tests for a module. It support controllers testing!

Examples:

```
python odoo-bin test --test-name=test_odoo_test_example_login - run one test
```

```
python odoo-bin test --test-class=TestOdooTestExample - run all tests from test class
```

```
python odoo-bin test --test-module=odoo_test - run all tests from module
```

```
python odoo-bin test --test-modules=odoo_test,web - run all tests from modules
```

In examples above default configuration file has specified **db_name=v14_atingo**. User can select target db as in example below:

```
python odoo-bin test --database=v14_odoo_vanilla --test-name=test_odoo_test_example_login - run one test on selected database
```

This module must be imported from default path. It won't work with selected custom configuration file. Example:

```
python odoo-bin test --config=/home/tkarpinski/odoo_14/conf/odoo.conf
```

Configuration file with path to custom addons should be coming from default path. If this is not possible, add this module to **odoo/addons** directly. 

Preinit
------------------------------
Before you start working with this module apply suggestions above. This module is using additional python modules, you can install them from **requirements.txt**

Details
------------------------------
odoo_test module checks selected tests. If test inherits HttpCase a new odoo instance with shared cursor will be started. Thanks to it user can test controllers. You can find example in **tests/test_odoo_test_example.py**. In this example a new user is created and logs in.

In case of any questions don't hesitate to email me: tadeusz.karpinski@gmail.com

Screenshots
------------------------------

Screenshot 1

![Screenshot 1](static/description/images/screenshot1.png?raw=true "Screenshot 1")

Screenshot 2

![Screenshot 2](static/description/images/screenshot2.png?raw=true "Screenshot 2")

Screenshot 3

![Screenshot 3](static/description/images/screenshot3.png?raw=true "Screenshot 3")
