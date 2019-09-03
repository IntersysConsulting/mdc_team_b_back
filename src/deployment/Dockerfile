# Dockerfile for flask container
# This image need the project directory in order to
# build successfully.

# From the base directory mdc_team_b_back/src 
# Use the follow command to create the image
# docker build  -t deployment -f development/Dockerfile .
# Use the follow command to start the container 
# docker run -d --name flask-dev -p 5000:5000  deployment 

FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
COPY ./entrypoint.py ./
COPY ./config.yaml ./
COPY ./flaskr ./flaskr

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV FLASK_APP flaskr

EXPOSE 5000:5000

CMD python entrypoint.py
