# Installation

Install the pip package:

```bash
pip install django-simplefeedback
```

Install `django-rest-framework` if not already installed

add `simple_feedback` and `rest_framework` to INSTALLED_APPS

include 'simple_feedback.urls' into urlpatterns

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("simple_feedback.urls")),
]
```

Migrate the db to crate simple-feedback models

```bash
python manage.py migrate
```

# Settings

`SIMPLE_FEEDBACK_SEND_TO` - email string or a list of email strings

valid examples:
```
SIMPLE_FEEDBACK_SEND_TO =
SIMPLE_FEEDBACK_SEND_TO = 'sendto@address.org'
SIMPLE_FEEDBACK_SEND_TO = ['sendto1@address.org', 'sendto2@address.org']
```
When SIMPLE_FEEDBACK_SEND_TO is empty or not defined, the email recepients will be all the superusers in the system.


`SIMPLE_FEEDBACK_SEND_MAIL_FUNC_OVERRIDE` - function to send email with
needs to implement two kwargs `message` and `recipients`

valid example:
```python
settings.py:
SIMPLE_FEEDBACK_SEND_MAIL_FUNC_OVERRIDE = send_email_function

def send_email_function(message, recipients):
    send_email()
```

# Develop

Clone the repo

```bash
git clone git@github.com:pulilab/django-simple-feedback.git
```

## Test app

Test standalone app:

$ export DATABASE_URL='your_db'  # you can skip this, defaults to 'localhost' (use postgres.app for simplicity)

$ pip install -r requirements.txt

$ python runtests.py

## Run the app in develop mode

Create a new django project and install the package in develop mode

```bash
django-admin startproject simple_feedback_demo
cd simple_feedback_demo
pip install -e ~LOCAL_PATH_TO_DJANGO_SIMPLEFEEDBACK
```

Add `simple_feedback` and `rest_framework` to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'simple_feedback'
]
```
Configure demo app urls

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("simple_feedback.urls")),
]
```
> SqlLite is not supported

Change the db config to use postgres in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': os.environ.get("DATABASE_URL", 'localhost'),
        'PORT': 5432,
    }
}
```

Migrate db, create super user and run your demo app:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

open the browser at `http://localhost:8000/admin`

