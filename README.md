# PayNearby
Design a restful API for customer data

# Steps For Running Application:-

1. Create Virtualenv:- virtualenv -p python3.8 venv
2. Install Requirements:- pip install -r requirements.txt
3. Run Server:- python manage.py runserver

API endpoints: https://documenter.getpostman.com/view/21125999/VUjMq787

# Note: Think database modeling in a way to accommodate ingesting 10M records everyday
--> We can do several steps for handling Millions of data like Caching strategies, chunk approach, Data preprocessing

# For DATABASE :- You can create new DB and save credentials in environment->dev.env file

After follow the steps like:
    - python manage.py makemigrations
    - python manage.py migrate
