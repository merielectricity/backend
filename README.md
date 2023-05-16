# backend
Backend server/API code.

## Installation Steps:
To install python follow

**Windows** : Install Python: If you haven't already, download and install Python from the official Python website (https://www.python.org/downloads/). Make sure to select the option to add Python to the system PATH during the installation process.

**Linux**  : sudo apt-get install python3

**Move to the backed folder, inside cloned git repo for all steps defined below

1. Create Virtual Environment

   ```python -m venv env```

   Note: for python 3.X and env(virtual environment name) is included in gitignore.

2. Activate Virtual Environment 

   for windows: ```.\env\Scripts\activate```
   
   for linux: ```source env/bin/activate```
 
3. Source local env
    source .env/local
    
3. Installing requirements
   
   ```pip install -r requirements.txt```

## Running Project

Below commands require a database,default is sqlite , use VsCode to avoid setting up database

1. Create superuser for your local project

   `python manage.py createsuperuser`

   ##### *Note:  Follow on-screen instructions till you recieve `Superuser created successfully` message.*

2. Make model changes ready for migration

   `python manage.py makemigrations`

3. Make migrations

   `python manage.py migrate`

4. Run project locally

   `python manage.py runserver`
