FROM centos:7

MAINTAINER Mats Rynge "rynge@isi.edu"

RUN yum -y upgrade
RUN yum -y install epel-release yum-plugin-priorities

COPY Cycles /usr/bin/Cycles
RUN chown root:root /usr/bin/Cycles && chmod 755 /usr/bin/Cycles

