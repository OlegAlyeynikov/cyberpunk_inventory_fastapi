FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY ./ /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

COPY ./start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/start.sh

ENTRYPOINT ["/usr/src/app/start.sh"]
