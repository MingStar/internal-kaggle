# Internal Kaggle

Kaggle like platform for internal use.

## First time setup

1. Install packages & start pipenv shell

```
$ pipenv install
$ pipenv shell
```

2. Start dependent docker services (esp. database)
```
$ cd local-dev
$ docker-compose build
$ docker-compose up -d
$ cd ..
```

2. DB Migrate
```
$ flask db upgrade
$ python migrations/seed.py
```


## Local run

```
flask run
```

## Before deployment

To update the Pipfile.lock with Pipfile
```
$ pipenv lock
```

## How to do DB migration

First, update the model class

then,
```
$ flask db migrate
$ flask db upgrade
```
