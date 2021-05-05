# Courses Catalogue
[![Build Status](https://travis-ci.com/mikharkiv/yalantis-test-task.svg?branch=master)](https://travis-ci.com/mikharkiv/yalantis-test-task)

A test task for Yalantis Python Summer School 2021. Made on Django and Django Rest Framework.

Using Flake8, Travis CI and Docker.

## Table of contents
* [Installation](#installation)
  * [Using Docker](#using-docker)
  * [Using Python Virtual Environment](#using-python-virtual-environment)
* [Testing](#testing)
* [How is it built](#how-is-it-built)
* [API guide](#api-guide)
  * [DRF API](#drf-api)
  * [Filtering and searching](#filtering-and-searching)
  * [Pure API](#pure-api)
* [Dependencies](#dependencies)

## Installation
> Note: all commands should be executed in the directory where you have cloned this repository  

#### Using Docker:
0. Download and install [Docker](https://www.docker.com/get-started) if you don't have one  
1. Clone the repository to your computer  
`git clone git@github.com:mikharkiv/yalantis-test-task.git`
2. Set up environment variable _SECRET_KEY_  
On Windows:  
`set SECRET_KEY=<your_secret_key>`  
On macOS and Linux:  
`export SECRET_KEY=<your_secret_key>`  
3. Build an image  
`docker-compose build`  
4. Run a container
`docker-compose up app`
5. Open [URL](http://localhost:8000/) in your browser and enjoy!
> Note: default port of the container is 8000, you can change it in **docker-compose.yml**

#### Using Python virtual environment:
0. Download [Python](https://www.python.org/downloads/) if you don't have one.
1. Clone the repository to your computer  
`git clone git@github.com:mikharkiv/yalantis-test-task.git`
2. Make a new virtual environment  
`python -m venv venv`
3. Activate it  
On macOS and Linux:  
`source venv/bin/activate`  
On Windows:  
`.\venv\Scripts\activate`
4. Install dependencies  
`pip install -r requirements.txt`  
5. Apply migrations  
`python manage.py migrate`  
6. Run the server  
`python manage.py runserver`
7. Open [URL](http://localhost:8000/) in your browser and enjoy!

## Testing
Using **Docker**: `docker-compose up test`  
Using **virtual environment**: `python -m pytest`
  
Tests are also available via Postman:  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1bd1288f6c324c8c5678?action=collection%2Fimport)

## How is it built
I've implemented **two variants** of API:
* First _(DRF API)_ - using Django Rest Framework
* Second _(Pure API)_ - using own views based on Django's built-in views

Both of the variants are returning response in JSON, but DRF API has also an UI, which makes testing more friendly.

Specific code which belongs to the **Pure API** can be found in `views` package:
* `views/json`  
Contains mixins and views providing JSON REST API  
* `views/filters`  
Contains simple and naїve request filters

Default Pure API settings which can be found in `settings.py`:
```python
PURE_REST = {
    'PAGE_SIZE': 10,
    'DATE_FORMAT': "%d.%m.%Y",
}
```
where:
* `PAGE_SIZE` is the count of entries on the page of ListView
* `DATE_FORMAT` is the format of the DateTime field using in JSON serialization

## API guide

Required JSON object format (all parameters are **required**):
```json
{
    "name": "<The name of the object>",
    "start_date": "dd.mm.YYYY",
    "end_date": "dd.mm.YYYY",
    "lectures_num": <number_of_lectures>
}
```

Required header: `Content-Type: application/json`

### DRF API
Base URL is `api/v0/`
#### Get list of courses (search and filters available)
```http request
GET api/v0/courses/?page=<page_num>
```
where `<page_num>` is a number of the page  
Response:
```json
{
  "count": 31,
  "total_pages": 4,
  "results": []
}
```
where `count` is total count of objects matching query, `total_pages` is number of pages, `results` is an array containing objects matching query.  

#### Filtering and searching:  
For filtering by date use this **URL parameter** syntax:
* `<date_name><lookup>=<your_date>`  
where `date_name` is name of the field (`start_date`/`end_date`), lookup is one of the following:  
  * `gt` - greater than;
  * `lt` - lower than;
  * `gte` - greater than or equal;
  * `lte` - lower than or equal;
  * empty - for the exact match  
For example: `start_date__lt=20.01.2020` will select all of objects, whose `start_date` is lower than `20.01.2020`

> **Warning:** date format in DRF API is `dd.mm.YYYY` or `YYYY-mm-dd`

For searching, use `?search=<query>`.

#### Get course details
```http request
GET /api/v0/<course_id>
```

#### Create new course
```http request
POST /api/v0/
```
Requires `body` with serialized object.

#### Change course details
```http request
PUT /api/v0/<course_id>
```
Requires `body` with serialized object.

#### Delete the course
```http request
DELETE /api/v0/<course_id>
```

### Pure API

Here all is the same as with DRF API **except** filters date format and change course details method (POST vs PUT).

> **Warning:** date format in Pure API filters is only `YYYY-mm-dd`

#### Get list of courses (search and filters available)
```http request
GET api/v0/courses/?page=<page_num>
```  

**Filtering and searching:**  
For filtering by date use this **URL parameter** syntax: `<date_name><lookup>=<your_date>`. For searching, use `?search=<query>`.

#### Get course details
```http request
GET /api/v0/<course_id>
```

#### Create new course
```http request
POST /api/v0/
```
Requires `body` with serialized object.

#### Change course details
```http request
PUT /api/v0/<course_id>
```
Requires `body` with serialized object.

#### Delete the course
```http request
DELETE /api/v0/<course_id>
```

## Dependencies
* **django-rest-framework** - for building Rest API;
* **pytest**, **pytest-django** - for running unit-tests;
* **python-decouple** - for managing environment variables;
* **flake8**, **flake8-django** - for checking codestyle.
  
Regards, _mikharkiv_