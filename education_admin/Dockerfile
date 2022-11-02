FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /education_app
COPY requirements.txt /education_app/

RUN pip install -r requirements.txt

COPY . /education_app

RUN apt update && apt install gettext -y
