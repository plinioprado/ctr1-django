# ctr1-django

Basic ledger system using Django REST Framework with SQLite.

This poject explores coding and tools using:

* Web local service receving and responding rest requests using Django REST Framework (DRF) in the project root
* Applications coded in plain Python, using function based views. These apps are self containing modules that return data as Python dicts that is then inserted into the DRF responses. So can be incorporated into other REST services beyond DRF.
* A ledger system in ./ctr1
* An User app using DRF working with class-based views and Django coding in ./drf/user, accessed via endpoints and also the Django admin.

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
* Single currency (CAD)

## Install

```shell
git clone plinioprado/ctr-ledger1-django # clone repo
source venv/bin/activate # activate venv
```

## Optional authentication

Basic Auth implemented then commented out in setings.py and the views.

Running with Browser when enabled:

The first request should be http://localhost:8000/admin/ to login with a Django page.
    For this demo, login is "admin" and pass "12345"
The next ones will be to the application endpoints
To logout, request again http://localhost:8000/admin/ and click logout

Running with Postman when enabled:

In Authorization, select Aasic Auth, fill Username and Password

## Endpoints

ctr1 main endpoints

* Settings

  * GET    http://localhost:8000/ctr1/admin/setting/{num}   Get setting
  * POST   http://localhost:8000/ctr1/admin/setting        Create setting
  * PUT    http://localhost:8000/ctr1/setting        Update setting
  * DELETE http://localhost:8000/ctr1/admin/setting/{num}   Delete one setting

* Admin

  * GET    http://localhost:8000/ledger/reset   Reset db

* Django

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

Integration test including the web service:

1. Import to Postman the collection stored in invoice1/test/postman/ctr-invoice1-python.postman_collection
2. Run the application
3. Run the collection in Postman

## Standards

References:

* PEP 8 - https://peps.python.org/pep-0008
* pylint - https://pypi.org/project/pylint
* Google Python Style Guide - https://google.github.io/styleguide/pyguide.html

Checked with:

* mypy (static Typing for Python)
* pylint (style checking)

## Dev notes

Django and djangorestframework setup followed https://www.django-rest-framework.org/tutorial/quickstart/

Check type hints:

```shell
mypy ctr1/admin.py
```
