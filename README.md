timtec-php-env
==============

This repository contains a Vagrantfile for building a development VM,
a Dockerfile to setup the docker container with a fully functional PHP
environment and a importd/python web application that is responsible for
an API to manage the containers / environments.

Dockerfile
==========

The container includes an Ubuntu with php-fpm and nginx listening to requests
on port 80

The Document Root (/var/www) is mapped when a container is started

Development
===========

vagrant up

Web App
=======

The web app API:

- GET / returns info about running containers
- GET /user_id/ returns info about user_id container
- GET /user_id/start/ creates (if needed) and starts a container
- GET /user_id/stop/ stops a container
- GET /user_id/restart/ restarts a container
- GET /user_id/rm/ removes/delete the container
- POST /user_id/documents/ pushes a new document root to the container
- GET /user_id/url/ returns the url to access the container
