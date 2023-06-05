FROM python:3.10-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install commands
RUN apt-get update 
RUN apt-get install -y cron
RUN pip install --upgrade pip
RUN pip install pipenv

# install dependencies
COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock
RUN pipenv install --dev --system --deploy

COPY ./crontab /etc/cron.d/crontab
COPY . /usr/src/app/

RUN crontab /etc/cron.d/crontab

RUN echo "America/New_York" > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

CMD ["cron", "-f"]