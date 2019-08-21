# Dockerfile for flask container
# This image does not include the project directory
# you should use -v ./src:dst/ options in docker run
# to mount your directory.

# From the base directory mdc_team_b_back/src 
# Use the follow command to create the image
# docker build  -t development -f development/Dockerfile .
# Use the follow command to start the container 
# docker run -d -v flaskr:/flaskr --name flask-dev -p 5000:5000  development

FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV FLASK_APP flaskr
ENV FLASK_ENV development

EXPOSE 5000:5000

CMD flask run --host=0.0.0.0
