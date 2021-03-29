***************************************
Administrative Procedures
***************************************

Installation
================
-----------------
Required Software
-----------------
Docker is required to run the application. For instructions on how to install docker, please visit https://docs.docker.com/get-docker/

.. note:: Some installations such as linux will not include docker-compose and will require additional steps for installation. https://docs.docker.com/compose/install/

-------------
The .env file
-------------
In order for the application to run correctly, the .env file must be filled out correctly. An example file is located at ``docker-compose/.env.example``. This file must be named ``.env``.

- **SECRET_KEY**: The secret key for the application. If one is not supplied, one will be created by the application.
- **DEBUG**: should be set to false for production enviroments.
- **DBUSERNAME/DBPASSWORD**: Username and password for dev purposes (when not run using docker, the application defaults to a sqlite3 database).
- **POSTGRES_USER/POSTGRES_PASSWORD**: user and password that will be used to connect to the production database.
- **PROD_EMAIL**: Whether the application will use a normal mail server to send mail. Setting to false will not send emails and will instead print the email to the application logs.
- **EMAIL_(HOST, PORT, HOST_USER, HOST_PASSWORD, USE_TLS, TIMEOUT)**: Email server configuration options.
- **ALLOWED_HOSTS**: List of allowed host/domain names to be served by the application.
- **USE_X_FOWARDED_HOSTS**: Flag to enable USE_X_FORWARDED_HOST on the server.
- **DOMAIN**: The applications domain address.
- **DJANGO_SUPERUSER_(PASSWORD, USERNAME, EMAIL)**: Credentials for the application's superuser, this user will be responsible for allowing initial users into the system.
- **PROD_FS**: Whether the application will use the production file system.

------------------------
Starting the application
------------------------
1. While in the docker-compose directory, run ``docker-compose up --build``.

.. note:: To run the application in detached mode (the application is not attached to the bash session) run docker-compose up with the detach flag (``-d``)

2. Run ``./initial_setup.sh`` to initialize the stack.
3. Restart the stack by running ``docker-compose restart birdspotter``
4. To stop the application, if you are in the docker-compose directory, you can run ``docker-compose down``.
   
    - If you are running in the attached mode, i.e. logs are being displayed in the terminal window, stopping the stack can be done with CTRL-C


Routine Tasks
================

-------------
User Accounts
-------------
Once there is a set of admins within the system, user administration will come in two forms.

.. TODO Insert image to show navbar with group requests and admin options

First off, requests for elevated group permissions and access to the aplication (going from a public user to registered user) will be handled in the Group Requests page. An admin simply has to press "Approve" or "Deny" depending on the decision and the decision will be stored and the request removed from the list.

.. TODO: insert image of group requests page

The other location for user administration will be within the admin page itself. Like the Group Requests page, there will be an option in the navbar for any admin user that will take them to the Django admin panel. From there, click on Users, and then actions such as creating a user, changing a user's account to inactive, or deleting the user can be performed.

.. TODO: Insert images of Django admin panel, and how to manage users

------------------
Django admin panel
------------------

In addition to performing administration actions on user accounts, the admin panel allows the user to view, edit, and delete any object related to the application.

Backups
================


User Support
================
