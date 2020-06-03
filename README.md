## Drone Registry 


## Setting up a development environment

This is a Django project that uses Django and Django Rest Framework and the API Specification 

### Setting up a development environment
#### 2.Install pipenv
```
 pip install --user pipenv
```
#### 3.Download source code

```
git clone git@github.com:naxadevelopers/twilio.git
cd twilio
```
#### 4.Create Virtual Environment & Install dependencies

```
pipenv install -r requirements.txt --python=python3
```
#### 5.Activate Virtual Environment

```
pipenv shell
```
#### 6.Run Database Migrations

```
Python manage.py migrate
```
#### 7.Populate Initial data

```
python manage.py loaddata registry/defaultregistrydata.json
```
#### 8.Run Server

```
python manage.py runserver
```


### 9. Launch browser 
Launch browser to http://localhost:8000/api/v1/ to launch the API Explorer
