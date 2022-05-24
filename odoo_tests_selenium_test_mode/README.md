![Banner](static/description/images/banner.png?raw=true "Banner")

Odoo Tests Selenium Test Mode
------------------------------
With this module you can enter Test Mode. With Test Mode enabled, all changes on the database won't be commited. Leaving the Test Mode will rollback all changes, so the database won't be affected by your test. This module works well with Selenium IDE. It affects all users! In Test Mode bus.bus and emails are blocked. Be responsible and use it on test instances ONLY!

Use Case:

User can register an action in Selenium IDE, for example creation of a new user. It is impossible to run the registered test, because odoo won't create user with the same login. With Test Mode Selenium can always be ran, because test data will be rollbacked. Restaring odoo server will automatically leave the test mode and rollback database.

Example:

User opens odoo in debug mode and select **Enter Test Mode**

![Screenshot 1](static/description/images/screenshot1.png?raw=true "Screenshot 1")

After clicking this menu item all users will be notified, that Test Mode is enabled. New bar will be shown on the top.

![Screenshot 2](static/description/images/screenshot2.png?raw=true "Screenshot 2")

Now user can change any data in the system. It will be stored until leaving the Test Mode. User can refresh the website, or even close it. In this example the name of the user is changed and browser is refreshed.

![Screenshot 3](static/description/images/screenshot3.png?raw=true "Screenshot 3")

In the next step user exits the Test Mode.

![Screenshot 4](static/description/images/screenshot4.png?raw=true "Screenshot 4")

All database changes are rollbacked. Previous user's name is restored

![Screenshot 5](static/description/images/screenshot5.png?raw=true "Screenshot 5")

In case of any questions don't hesitate to email me: tadeusz.karpinski@gmail.com
