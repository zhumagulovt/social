# REST API Backend for social network app or website

This backend provides:
  - Beautiful admin page created by using django-jazzmin
  - JWT authentication
  - User's following system
  - User's feedback by followings
  - Likes, comments for each post
  - Real time chat of two users
  
# Running the server
If you wish to run the server, the first step is [installing Python](https://www.python.org/downloads/).

Create virtual enviroment and activate

Install dependencies
```
pip install -r requirements.txt
```


Migrate database
```
python3 manage.py migrate
```

Create admin user
```
python3 manage.py createsuperuser
```

Run
```
python3 manage.py runserver
```

All queries to db are optimized.

This project is developed in Python using Django and djangorestframework
