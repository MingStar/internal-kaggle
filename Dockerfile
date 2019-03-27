FROM python:3.6-alpine3.7 AS builder

# update pip
RUN pip install --upgrade pip
# install pipenv
RUN pip install pipenv

RUN mkdir /app
WORKDIR /app

# prerequisite for psycopg2
RUN apk add --no-cache build-base postgresql-dev

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile --system

# clean up to reduce the size of the build image
RUN pip uninstall -y pipenv virtualenv virtualenv-clone

#########################################
FROM python:3.6-alpine3.7 AS runner

WORKDIR /app
ENV FLASK_ENV=production
CMD ["./entrypoint.sh"]

# For installing docker
RUN echo http://dl-cdn.alpinelinux.org/alpine/v3.7/community >> /etc/apk/repositories
RUN apk update

RUN apk add --no-cache docker uwsgi-python3 curl libpq

# executables
COPY --from=builder /usr/local/bin/celery /usr/local/bin/
COPY --from=builder /usr/local/bin/flower /usr/local/bin/
COPY --from=builder /usr/local/bin/flask /usr/local/bin/

# site packages
COPY --from=builder /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/

# source files
COPY docker/* ./
COPY data ./data
COPY migrations ./migrations
COPY run.py ./
COPY app ./app
