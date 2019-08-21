# Dockerfile for flask container

FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
COPY ./flaskr ./flaskr

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV FLASK_APP flaskr
ENV FLASK_ENV development

EXPOSE 5000:5000

CMD flask run --host=0.0.0.0
