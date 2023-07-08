FROM python:3.11-alpine

RUN apk update
RUN apk add chromium chromium-chromedriver

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

COPY appcrons /var/spool/cron/crontabs/root

RUN mkdir logs
RUN python3 manager.py --create_db --init --update_profiles --run

CMD crond -b && python webapp.py
