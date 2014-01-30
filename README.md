timtec-php-env
==============

This repository contains a Vagrantfile for building a development VM,
a Dockerfile to setup the docker container with a fully functional PHP
environment and a Django web application that is responsible for an
API to manage the containers / environments.

Dockerfile
==========

The container includes an Ubuntu with php-fpm and nginx listening to requests
on port 80

The Document Root (/var/www) is mapped when the container is created

Django App
==========

The django app manages:

- Dynamic nginx config, mapping subdomains to the respective container (using redis)
- The document root for each container

