# ctr-ledger1-django

Basic ledger system using Django REST Framework with SQLite.

This poject explores coding and tools using:

* Web local service receving and responding rest requests using Django REST Framework (DRF) in the project root
* Applications coded in plain Python, using function based views. These apps are self containing modules that return data as Python dicts that is then inserted into the DRF responses. So can be incorporated into other REST services beyond DRF.
* Ai ledger system in ./ledger1
* An Invoice1 app in ./invoice1, using function based views and plain Python 3 service in ./invoice1/invoice_service.py. This service is a class containing methods that receive variables with the content of the requests and returns dicts with the contents of the responses. So it can be incorporated into other REST services beyond DRF.
* An User app using DRF working with class-based views and Django coding in ./drf/user, accessed via endpoints and also the Django admin.

## Run

```shell
python manage.py runserver
```

## Scope

Interface using the REST endpoints for:

* Login using Django
* ledger1 module
  * account CRUD
  * transaction CRUD
  * reports (with filter for date and account)
    * chart_account
    * journal
    * general_ledger
    * trial_balance
  * potential integration with documents
    * invoice1
    * bank statement (tdb)
    * eft(tdb)
  * reset db
* invoice1 module
  * invoice1 CRUD (no filter)
  * Reset: Reset db

invoice
bank statement
EFT

Constrains:

* No user login
* Single tennant
* Single language (English)
* Single currency (CAD)

Notes:

* Invoice data is based in Invoice1 from the CTR - Finance controls project

    ```Javascript
    {
        num: 1, // auto
        value: 1000.00, // float
        issueDate: "2000-01-02", // string representing date in yyyy-mm-dd
        cpart_name: "Cedar stores Ltd.", // string between 3 and 30 chars
        status: "open" // "open", "paid", or "canceled"
    }
    ```

## Install

```shell
git clone plinioprado/ctr-ledger1-django # clone repo
source venv/bin/activate # activate venv
```

## Authentication

Basic Auth implemented then commented out in setings.py and the views.

Running with Browser when enabled:

The first request should be http://localhost:8000/admin/ to login with a Django page.
    For this demo, login is "admin" and pass "12345"
The next ones will be to the application endpoints
To logout, request again http://localhost:8000/admin/ and click logout

Running with Postman when enabled:

In Authorization, select Aasic Auth, fill Username and Password

## Endpoints

Accounts

* GET    http://localhost:8000/ledger/accounts/{num}   Get account
* POST   http://localhost:8000/ledger/accounts/        Create account
* PUT    http://localhost:8000/ledger/accounts/        Update account
* DELETE http://localhost:8000/ledger/accounts/{num}   Delete one account

Transactions

* GET    http://localhost:8000/ledger/transactions/        Get all transactions
* GET    http://localhost:8000/ledger/transactions/{num}   Get transaction
* POST   http://localhost:8000/ledger/transactions/        Create transaction
* PUT    http://localhost:8000/ledger/transactions/        Update transaction
* DELETE http://localhost:8000/ledger/transactions/{num}   Delete one transaction

Documents

* GET    http://localhost:8000/ledger/docs/{type}       Get transactions from a type

Reports

* Report: http://localhost:8000/ledger/report/

Admin

* GET    http://localhost:8000/ledger/reset/   Reset accounts and transactions

Django

* Admin: http://localhost/admin/
* Users: http://localhost:8000/users/
* Groups: http://localhost:8000/groups/

## Stack

* Python 3
* venv
* Django and djangorestframework
* django-cors-headers

## Error handling

Will be responded with code:

* 400: client (user) error, raised as ValueError
* 500: server (application) error, raised as any error except ValueError

## Test

Unit test of the invoice1 module running pytest from the project root:

```shell
pytest -vv # or pytest -s to show messages
```

Integration test including the web service:

1. Import to  Postman the collection stored in invoice1/test/postman/ctr-invoice1-python.postman_collection
2. Run the application
3. Run the collection in Postman

## Dev notes

Django and djangorestframework setup followed https://www.django-rest-framework.org/tutorial/quickstart/

Development tools can be run with:

Check code linting:

```shell
pylint invoice1/invoice1_service.py
pylint ledger1/accounts1.py
pylint ledger1/transactions1.py
pylint ledger1/reports_service.py
```

Check type hints:

```shell
mypy invoice1/invoice1_service.py
mypy ledger1/accounts1.py
mypy ledger1/transactions1.py
mypy ledger1/reports_service.py
```
