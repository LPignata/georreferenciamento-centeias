FROM ubuntu:18.04

LABEL MAINTAINER="Léo Moraes leo.ms097@gmail.com"

RUN apt-get update

RUN apt-get -y install curl

RUN apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]