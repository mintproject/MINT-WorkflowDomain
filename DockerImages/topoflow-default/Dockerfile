FROM ubuntu
MAINTAINER add Lucas Carvalho lucas.carvalho@ic.unicamp.br

WORKDIR /app

ADD . /app

RUN apt-get update

RUN apt-get install -y python-pip wget zip
RUN wget https://github.com/peckhams/topoflow/archive/master.zip
RUN unzip master.zip && cd topoflow-master && pip install --editable ./ && pip install -U numpy==1.11.0
