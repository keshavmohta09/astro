# astro
Bidder - Online Auction Management System

### Create a virtual environment in python>3.8
`python -m venv env`

### Run the command
`pip install -r requirements.txt`

### Install `wsl` and `redis`


### Create a `.env` file and fill these values:
- SECRET_KEY=anyValue
- DEBUG=True

### Databse credentials
- DATABASE_ENGINE=django.db.backends.postgresql
- DATABASE_NAME=astro
- DATABASE_USER=your value
- DATABASE_PASSWORD=your value
- DATABASE_HOST=your value
- DATABASE_PORT=5432

- CELERY_BROKER_URL=redis://127.0.0.1:6379
- CACHE_BROKER_URL=redis://127.0.0.1:6379/1

# creds for sending email service
- EMAIL_HOST=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=
- EMAIL_PORT=

