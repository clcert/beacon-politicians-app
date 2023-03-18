FROM python:3.10-alpine

RUN apk update
RUN apk add chromium chromium-chromedriver

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

COPY updater-cron /var/spool/cron/crontabs/root

RUN mkdir log
RUN python3 populate_json.py 2

CMD crond -b && python webapp.py
