FROM python:3.11-alpine

RUN apk update
RUN apk add chromium chromium-chromedriver
RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir data
RUN mkdir logs

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 manager.py --create_db --init

COPY appcrons /var/spool/cron/crontabs/root

CMD crond -b && gunicorn --bind 0.0.0.0:80 wsgi:app
