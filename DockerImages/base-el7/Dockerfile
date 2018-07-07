FROM centos:7

RUN yum -y upgrade && \
    yum -y install epel-release yum-plugin-priorities

# well rounded basic system to support a wide range of user jobs
RUN yum -y groups mark convert \
    && yum -y grouplist \
    && yum -y groupinstall "Compatibility Libraries" \
                           "Development Tools" \
                           "Scientific Support"

RUN yum -y install \
           redhat-lsb \
           binutils \
           binutils-devel \
           coreutils \
           curl \
           fontconfig \
           gcc \
           gcc-c++ \
           gcc-gfortran \
           git \
           glew-devel \
           glib2-devel \
           glib-devel \
           graphviz \
           gsl-devel \
           java-1.8.0-openjdk \
           java-1.8.0-openjdk-devel \
           libgfortran \
           libGLU \
           libgomp \
           libicu \
           libquadmath \
           libtool \
           libtool-ltdl \
           libtool-ltdl-devel \
           libX11-devel \
           libXaw-devel \
           libXext-devel \
           libXft-devel \
           libxml2 \
           libxml2-devel \
           libXmu-devel \
           libXpm \
           libXpm-devel \
           libXt \
           mesa-libGL-devel \
           numpy \
           octave \
           octave-devel \
           p7zip \
           p7zip-plugins \
           python2-dateutil \
           python2-netcdf4 \
           python2-numpy \
           python2-pip \
           python2-requests \
           python2-simplejson \
           python34-dateutil \
           python34-devel \
           python34-netcdf4 \
           python34-numpy \
           python34-pip \
           python34-requests \
           python34-simplejson \
           python-devel \
           R-devel \
           redhat-lsb-core \
           rsync \
           scipy \
           tcl-devel \
           time \
           tk-devel \
           wget \
           which

# some more python modules
RUN pip2 install pandas &&\
    pip3 install pandas

