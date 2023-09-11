FROM python:3.11.4-slim-bullseye

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod

RUN apt-get update \
  && apt-get -y install netcat gcc libpq-dev \
  && apt-get clean

RUN pip install -U pip setuptools
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chown -R app:app $APP_HOME

USER app

CMD gunicorn --bind 0.0.0.0:5000 main:app -k uvicorn.workers.UvicornWorker