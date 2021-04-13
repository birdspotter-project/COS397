***************************************
System Overview
***************************************

Background
================
The system is composed of five major components: the Django Python web application, Postres, NGINX, Traefik, and a mass storage system, as can be seen in :numref:`systemoverview` .

.. _systemoverview:
.. figure:: static/SystemOverview.png
   :alt: "System diagram"
   :align: center

   : A system diagram depicting the relationships between the various parts of the system.


The Django application is the core of the system, while the Postgres database contains all of the application data except for the raw files.
The Django application offloads file uploads and downloads to the NGINX server, while the Traefik proxy handles traffic routing and HTTPS termination. 
The Traefik proxy can also handle automatic certificate renewal via LetsEncrypt if necessary.
Finally, the mass storage handles the storage of all the raw files (Original Shapefiles, GeoTiffs, thumbnails).

Hardware and Software requirements
=====================================
The web server itself has no particularly strict hardware requirements - one CPU core and 2GB of ram, 
>64gb of hard drive space should be plenty for most small deployments, assuming separate file storage of some sort is used for the mass file storage component. 
The provided installation procedures rely on the use of Docker and Docker Compose, so the application can be run on any OS that Docker can run on, 
though some Linux distros (e.g. Ubuntu, Debian, CentOS, RedHat) will be easier than others as they have more community support.

One important note about the mass file storage is that the installation procedures assume that the network file storage is mounted to the host machine.
Doing this via SystemD is advisable, as it will help ensure the remote volume is re-mounted properly in the event of a network disruption or server reboot.