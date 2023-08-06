#django-old-new-history
========================

**django-old-new-history** is customize history feature which is used to show the old and new value of model's change field in history action of admin panel.

------------
Requirements
------------

- Python 3.7 or later
- Django 2.0 or later

------------
Features
------------

-  Customize history.
-  Display old and new value of model's change field.
-  Simple admin integration.


------------
Installation
------------

Just use:

::

    pip install django-old-new-history

Setup
=====

Add **django_old_new_history** to **INSTALLED_APPS** in your settings.py, e.g.:

::

    INSTALLED_APPS = [
    ...
    'django_old_new_history',
    ...


Usage
=====

Inherit from **DjangoOldNewHistory** to get the custom history feature.

admin.py e.g.:

::


    from django.contrib import admin
    from .models import ExampleModel
    from django_old_new_history.admin import DjangoOldNewHistory

    @admin.register(ExampleModel)
    class ExampleModelAdmin(DjangoOldNewHistory, admin.ModelAdmin):
        ...

Screenshot
=====
Here is screenshot of django-old-new-history

![alt text](https://raw.githubusercontent.com/mayur-softices/djnago-customize-history/main/docs/_static/Change-history-CrudUser-object-5-Django-site-admin.png)