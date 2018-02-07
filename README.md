# Local stack overflow

my local [stack overflow](https://stackoverflow.com/)

# Install
``` bash
$ python3 -m venv env_name
$ . env_name/bin/activate
$ pip install -r requirements.txt
```

change settings:
``` bash
    EMAIL_HOST_USER = 'email_addres'
    EMAIL_HOST_PASSWORD = 'password'
```
next apply migrations:
``` bash
    $ python manage.py makemigrations
    $ python manage.py migrate
```
and run:
``` bash
    $ python manage.py runserver
    celery:
    $ celery worker -A local_stack_overflow --loglevel=debug --concurrency=4
```
or docker run:
``` bash
    $ docker build
    $ docker up
    $ docker run web python manage.py migrate
    $ docker run web python manage.py createsuperuser
    $ docker up
```
