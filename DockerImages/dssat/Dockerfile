FROM centos:7

MAINTAINER Mats Rynge "rynge@isi.edu"

RUN yum -y upgrade
RUN yum -y install epel-release yum-plugin-priorities

COPY dssat.tar.gz /tmp/dssat.tar.gz
RUN cd /opt && tar xzf /tmp/dssat.tar.gz && rm -f /tmp/dssat.tar.gz

