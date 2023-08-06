
============================
Django IPG HRMS onboarding
============================


Quick start
============


1. Add 'onboarding' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'onboarding'
    ]

2. Include the onboarding to project URLS like this::

    path('onboarding/', include('onboarding.urls')),

3. Run ``python manage.py migrate`` to create onboarding model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user