##  RDAP


## Setting up a development environment

This is a Django project that uses Django and Django Rest Framework and the API Specification 

### Setting up a development environment
#### 1. Install pipenv
```
 pip install --user pipenv
```
#### 2. Download source code

```
git clone git@github.com:naxadevelopers/twilio.git
cd twilio
```
#### 3. Create Virtual Environment & Install dependencies

```
pipenv install -r requirements.txt --python=python3
```
#### 4. Activate Virtual Environment

```
pipenv shell
```
#### 5. Run Database Migrations

```
Python manage.py migrate

#### 7. Run Server

```
python manage.py runserver
```
```
