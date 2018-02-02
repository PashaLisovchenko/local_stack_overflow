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
    DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name_db',
        'USER' : 'your_name',
        'PASSWORD' : 'your_password',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
        }
    }

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
