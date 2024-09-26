# ctr-ledger1-django

Basic ledger system using Django REST Framework with SQLite.

This poject explores coding and tools using:

* Web local service receving and responding rest requests using Django REST Framework (DRF) in the project root
* An Invoice1 app in ./invoice1, using function based views and plain Python 3 service in ./invoice1/invoice_service.pu. This service is a class containing methods that receive variables with the content of the requests and returns dicts with the contents of the responses. So it can be incorporated into other REST services beyond DRF.
* An User app using DRF working with class-based views and Django coding in ./drf/user, accessed via endpoints and also the Django admin.

## Scope

Interface using the REST endpoints:

Login using Django

Invoice1 CRUD:

* GET: get all invoices
* POST: Create invoice
* PUT: Update invoice
* DELETE: Delete invoice
* Reset: Reset db

Invoice data is based in Invoice1 from the CTR - Finance controls project

```Javascript
{
    num: 1, // auto
    value: 1000.00, // float
    issueDate: "2000-01-02", // string representing date in yyyy-mm-dd
    parts_seller_name: "Example Ltd", // string between 3 and 30 chars
    parts_buyer_name: "Cedar stores Ltd.", // string between 3 and 30 chars
    status: "open" // "open", "paid", or "canceled"
}
```

## Install

```shell
git clone plinioprado/ctr-ledger1-django # clone repo
source venv/bin/activate # activate venv
```

## Run

```shell
python manage.py runserver
```

The first request should be to adim endpoint to login with a Django page.
    For this demo, login is "admin" and pass "12345"
The next ones will be to the invoice1 endpoint
There an opiton to access user and group endpoints

## Endpoints

* Admin: http://127.0.0.1:8000/admin/
* Users: http://127.0.0.1:8000/users/
* Groups: http://127.0.0.1:8000/groups/
* Invoice1: http://127.0.0.1:8000/invoice1/

## Stack

* Python 3
* venv
* Django and djangorestframework

## Test

Unit test of the invoice1 module running pytest from the project root:

```shell
pytest invoice1/invoice1_tests.py -vv
```

Integration test inclusing the web service:

1. Import to  Postman the collection stored in invoice1/test/postman/ctr-invoice1-python.postman_collection
2. Run the application
3. Run the collection in Postman

## Dev notes

Django and djangorestframework setup followed https://www.django-rest-framework.org/tutorial/quickstart/

Development tools can be run with:

```shell
pylint invoice1/invoice1_service.py # to check code linting
mypy invoice1/invoice1_service.py # to check type hints
```
