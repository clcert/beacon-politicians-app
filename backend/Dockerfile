FROM python:3.11-alpine

RUN apk update
RUN apk add chromium chromium-chromedriver

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

RUN mkdir data
RUN mkdir logs

COPY . /app

COPY appcrons /var/spool/cron/crontabs/root

RUN touch data/last_deputies.json
RUN python3 manager.py --create_db --init 
RUN python3 manager.py --update_profiles 
RUN python3 manager.py --run

CMD crond -b && python webapp.py
