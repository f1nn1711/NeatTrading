FROM python:3.10

RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt


COPY ./scripts/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["python", "./main.py", "help"]
CMD ["cron", "-f"]