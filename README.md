# ashar-backend
Backend for the ashar project in which you can create words that need a translation in the Kyrgyz language, there is also authorization, authentication and registration, we also added the functionality of likes so that you can like translations. Project will be continued.

## Setup

Install pipenv

    pip install --user pipenv

Install packages

    pipenv sync

In case there is an error with openssl

    env LDFLAGS="-I/opt/homebrew/opt/openssl/include -L/opt/homebrew/opt/openssl/lib" pipenv sync

Create your copy of .env

    cp .env.example .env

Activate virtualenv

    pipenv shell

Run migrations

    python manage.py migrate

Run server

    python manage.py runserver

License: MIT License
