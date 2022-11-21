
## Setting up a development environment


#### 2. Download source code

```git clone https://github.com/akirachix/We-R-Madagascar.git```

```cd We-R-Madagascar```

#### 3. Create Virtual Environment & Install dependencies

```python -m venv venv```

#### 4. Activate Virtual Environment

```source venv/bin/activate ```

#### 5. Install the requirements

```pip install -r requirements.txt```

#### 5. Run Database Migrations

```Python manage.py migrate```

#### 7. Run Server

```python manage.py runserver```
