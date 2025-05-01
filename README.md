# ctr1-django

Basic ledger system using Django REST Framework with SQLite.

This poject explores coding and tools using:

* Web local service receving and responding rest requests using Django REST Framework (DRF) in the project root
* Applications coded in plain Python, using function based views. These apps are self containing modules that return data as Python dicts that is then inserted into the DRF responses. So can be incorporated into other REST services beyond DRF.

## Run

```shell
python manage.py runserver
```

## Scope

Interface using the REST endpoints for:

* admin module
  * login
  * setting crud
  * user crud
  * reset db

Constrains:

* Single tennant
* Single language (English)

## Install

```shell
git clone plinioprado/ctr-ledger1-django # clone repo
source venv/bin/activate # activate venv
```

## Optional authentication

Django basic Auth can be used instead of api_keys managed by the ctr1 component. It was implemented then commented out in setings.py and the views.

Running with Browser when enabled:

The first request should be http://localhost:8000/admin/ to login with a Django page.
    For this demo, login is "admin" and pass "12345"
The next ones will be to the application endpoints
To logout, request again http://localhost:8000/admin/ and click logout

Running with Postman when enabled:

In Authorization, select Basic Auth, fill Username and Password

## Endpoints

ctr1 main endpoints

* Settings

  * GET    http://localhost:8000/ctr1/admin/settings/{code}   Get setting
  * POST   http://localhost:8000/ctr1/admin/settings        Create setting
  * PUT    http://localhost:8000/ctr1/admin/settings        Update setting
  * DELETE http://localhost:8000/ctr1/admin/settings/{code}   Delete one setting

* Users

  * GET    http://localhost:8000/ctr1/admin/users/{code}   Get setting
  * POST   http://localhost:8000/ctr1/admin/users        Create setting
  * PUT    http://localhost:8000/ctr1/admin/users        Update setting
  * DELETE http://localhost:8000/ctr1/admin/users/{code}   Delete one setting

* Admin

  * GET    http://localhost:8000/ctr1/reset   Reset db

* Django admin (users are not the same as those used by Ctr1)

  * Admin: http://localhost/admin/
  * Users: http://localhost:8000/users/
  * Groups: http://localhost:8000/groups/

## Stack

* Python 3
* venv
* Django and django rest framework
* django-cors-headers

## Error handling

Will be responded with code:

* 400: client (user) error, raised as ValueError
* 500: server (application) error, raised as any error except ValueError

## Tests

Unit test of the invoice1 module running pytest from the project root:

```shell
pytest -vv # or pytest -s to show messages
```

## Standards

References:

* PEP 8 - https://peps.python.org/pep-0008
* pylint - https://pypi.org/project/pylint
* REST: https://restfulapi.net
* Google Python Style Guide - https://google.github.io/styleguide/pyguide.html

Checked with:

* mypy (static Typing for Python)
* pylint (style checking)

## Dev notes

Django and djangorestframework setup followed https://www.django-rest-framework.org/tutorial/quickstart

When update library run: $ pip freeze > requirements.txt

Check type hints:

```shell
mypy ctr1
```
