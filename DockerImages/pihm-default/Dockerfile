FROM ubuntu:16.04

MAINTAINER add Lucas Carvalho lucas.carvalho@ic.unicamp.br

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated \
        build-essential \
        cmake \
        curl \
        git \
        pkg-config \
        python \
        python-dev \
        software-properties-common \
        unzip \
        zip \
        zlib1g-dev \
        openjdk-8-jdk \
        openjdk-8-jre-headless \
        vim \
        wget \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y wget zip make gcc
RUN wget https://computation.llnl.gov/projects/sundials/download/sundials-2.2.0.tar.gz && tar xvf sundials-2.2.0.tar.gz && cd sundials && ./configure && make && make install
RUN wget http://www.pihm.psu.edu/PIHM_v2.2.tar && tar xvf PIHM_v2.2.tar && cd PIHM_v2.2 && make clean
RUN cd PIHM_v2.2 && grep -rl Makefile . | xargs sed -i 's/\/Users\/xxy113\/software/\/app/g'
RUN cd PIHM_v2.2 && make pihm && mv pihm /usr/bin
