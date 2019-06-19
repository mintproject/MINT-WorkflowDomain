FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated \
        build-essential \
        cmake \
        curl \
        gdal-bin \
        git \
        gsfonts \
        libfreetype6-dev \
        libgdal-dev \
        libgdal-dev \
        libpng-dev \
        libssl-dev \
        libsundials-dev \
        libomp-dev \
        libopenmpi-dev \
        libxpm-dev \
        libzmq3-dev \
        module-init-tools \
        openjdk-8-jdk \
        openjdk-8-jre-headless \
        pkg-config \
        proj-bin \
        proj-data \
        python \
        python3 \
        python3-dateutil \
        python3-dev \
        python3-netcdf4 \
        python3-numpy \
        python3-pandas \
        python3-pip \
        python3-requests \
        python3-simplejson \
        python3-xarray \
        python-dateutil \
        python-dev \
        python-netcdf4 \
        python-numpy \
        python-pandas \
        python-pip \
        python-requests \
        python-simplejson \
        r-base \
        r-base-dev \
        rsync \
        software-properties-common \
        unzip \
        vim \
        wget \
        zip \
        zlib1g-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
