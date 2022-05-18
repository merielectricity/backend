# backend
Backend server/API code.

## Installation Steps:

1. Create Virtual Environment

   ```python -m venv env```

   Note: for python 3.X and env(virtual environment name) is included in gitignore.

2. Activate Virtual Environment 

   for windows: ```.\env\Scripts\activate```
   
   for linux: ```source env/bin/activate```

3. Installing requirements
   
   ```pip install -r requirements.txt```

## Running Project

1. Create superuser for your local project

   `python manage.py createsuperuser`

   ##### *Note:  Follow on-screen instructions till you recieve `Superuser created successfully` message.*

2. Make model changes ready for migration

   `python manage.py makemigrations`

3. Make migrations

   `python manage.py migrate`

4. Run project locally

   `python manage.py runserver`