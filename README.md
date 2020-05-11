## Drone Registry 


## Setting up a development environment

This is a Django project that uses Django and Django Rest Framework and the API Specification 

### 1. Install pipenv
`pip install --user pipenv`

### 2. Download source code
```
git clone git@github.com:naxadevelopers/twilio.git
cd twilio
```
### 3. Create Virtual Environment & Install dependencies
```
pipenv install -r requirements.txt --python=python3
```

### 4. Activate Virtual Environment
```
pipenv shell
```

### 5. Create Initial Database
Use `python manage.py migrate` to create the initial database tables locally. It will use the default SQLLite. 

### 6. Populate initial data
Use `python manage.py loaddata registry/defaultregistrydata.json` to populate initial data. 

### 7. Run Server
```
python manage.py runserver
```

### 8. Launch browser 
Launch browser to http://localhost:8000/api/v1/ to launch the API Explorer
