FROM ubuntu:16.04

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
        libpng12-dev \
        libssl-dev \
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
        python3-dev \
        python3-netcdf4 \
        python3-pip \
        python3-requests \
        python3-simplejson \
        python-dev \
        python-netcdf4 \
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

RUN wget -nv -O ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -f -p /opt/conda && \
    export PATH=/opt/conda/bin:$PATH && \
    conda install --yes anaconda && \
    conda install --yes -c conda-forge tensorflow keras && \
#     conda install --yes pytorch-cpu torchvision-cpu -c pytorch && \
    conda install --yes -c conda-forge imageio && \
    pip install tifffile && \
    pip install opencv-python && \
    pip install matplotlib && \
    pip install Shapely && \
    pip install requests && \
    pip install numpy && \
    pip install idna && \
    pip install descarteslabs && \
    pip install scikit-image && \
    conda create --yes -n gdaltest gdal
