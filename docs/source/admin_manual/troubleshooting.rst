***************************************
Troubleshooting
***************************************

Error Messages and Failures
===========================

Errors on Startup
-----------------
Most error messages thrown at initial startup or post-upgrade startup are likely to be related to a migration issue. 
In order to ensure that the migrations are up to date, the following command should be run:

``docker-compose exec birdspotter python3 manage.py migrate``

Errors during runtime
---------------------
When a user runs into an error, the application does not display detailed errors to the client, but it will display a more detailed error in the application logs.
In order to view these logs, run the following command:

``docker-compose logs``


Known Bugs and Limitations
===========================
The main known limitation of the application at this point is that the "Queue Analysis" function has not been completed yet, so analysis must be performed manually, and the results re-uploaded. 
As part of this limitation, the application also does not yet support thumbnails for each datapoint.