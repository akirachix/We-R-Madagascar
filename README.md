## Nepal Drone Portal


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
```
#### 6. Populate Initial data

```
python manage.py loaddata registry/defaultregistrydata.json
```
#### 7. Run Server

```
python manage.py runserver
```

### 8. Launch browser 
Launch browser to http://localhost:8000/api/v1/ to launch the API Explorer

### Running with Docker compose
If you have docker-compose installed you may clone this repository and run:
```
docker-compose -f docker-compose-prod.yaml up --build -d  #for production
docker-compose -f docker-compose-dev.yaml up --build -d  #for developement
```