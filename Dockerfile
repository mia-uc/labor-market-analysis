FROM python:3.10-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock
RUN pipenv install --dev --system --deploy

COPY ./crontab /etc/cron.d/crontab
COPY . /usr/src/app/

RUN crontab /etc/cron.d/crontab

CMD ["cron", "-f"]