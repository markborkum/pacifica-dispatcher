# Pacifica Dispatcher
[![Build Status](https://travis-ci.org/pacifica/pacifica-dispatcher.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-dispatcher)
[![Build status](https://ci.appveyor.com/api/projects/status/vjcs904285d1jexn?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-dispatcher)
[![Maintainability](https://api.codeclimate.com/v1/badges/b75312dc89c170cb4510/maintainability)](https://codeclimate.com/github/pacifica/pacifica-dispatcher/maintainability)

[![Frontend Stars](https://img.shields.io/docker/stars/pacifica/dispatcher-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-frontend/general)
[![Backend Stars](https://img.shields.io/docker/stars/pacifica/dispatcher-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-backend/general)
[![Frontend Pulls](https://img.shields.io/docker/pulls/pacifica/dispatcher-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-frontend/general)
[![Backend Pulls](https://img.shields.io/docker/pulls/pacifica/dispatcher-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-backend/general)
[![Frontend Automated build](https://img.shields.io/docker/automated/pacifica/dispatcher-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-frontend/builds)
[![Backend Automated build](https://img.shields.io/docker/automated/pacifica/dispatcher-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/dispatcher-backend/builds)

Pacifica dispatcher runs applications based on incoming cloud events.

## The Parts

There are several parts to this code as it encompasses
integrating several python libraries together.

 * [PeeWee](http://docs.peewee-orm.com/en/latest/)
 * [CherryPy](https://cherrypy.org/)
 * [Celery](http://www.celeryproject.org/)

For each major library we have integration points in
specific modules to handle configuration of each library.

### PeeWee

The configuration of PeeWee is pulled from an INI file parsed
from an environment variable or command line option. The
configuration in the file is a database
[connection url](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url).

 * [Dispatcher PeeWee Model](pacifica/dispatcher/orm.py)
 * [Dispatcher Config Parser](pacifica/dispatcher/config.py)

### CherryPy

The CherryPy configuration has two entrypoints for use. The
WSGI interface and the embedded server through the main
method.

 * [Dispatcher Main Method](pacifica/dispatcher/__main__.py)
 * [Dispatcher WSGI API](pacifica/dispatcher/wsgi.py)
 * [Dispatcher CherryPy Objects](pacifica/dispatcher/rest.py)

### Celery

The Celery tasks are located in their own module and have
an entrypoint from the CherryPy REST objects. The tasks
save state into a PeeWee database that is also accessed
in the CherryPy REST objects.

 * [Dispatcher Tasks](pacifica/dispatcher/tasks.py)

## Start Up Process

The default way to start up this service is with a shared
SQLite database. The database must be located in the
current working directory of both the celery workers and
the CherryPy web server. The messaging system in
[Travis](.travis.yml) and [Appveyor](appveyor.yml) is
redis, however the default is rabbitmq.

There are three commands needed to start up the services.
Perform these steps in three separate terminals.

 1. `docker-compose up rabbit`
 2. `celery -A pacifica.dispatcher.tasks worker -l info`
 3. `python -m pacifica.dispatcher

To test working system run the following in bash:

 1. `UUID=$(curl http://127.0.0.1:8069/dispatch/add/2/2)`
 2. `curl http://127.0.0.1:8069/status/$UUID`
