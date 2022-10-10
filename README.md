# REST API Backend for social network app or website

This backend provides:
  - JWT authentication
  - User's following system
  - User's feedback by followings
  - Likes, comments for each post
  - Real time chat of two users
  - Sending confirmation email after registration
  - Sending confirmation email for change password
  - OpenAPI documentation

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



This project is developed in Python using Django and djangorestframework
