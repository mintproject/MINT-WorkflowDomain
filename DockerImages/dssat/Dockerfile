FROM mintproject/base-el7

MAINTAINER Mats Rynge "rynge@isi.edu"

COPY dssat.tar.gz /tmp/dssat.tar.gz
RUN cd /opt && tar xzf /tmp/dssat.tar.gz && rm -f /tmp/dssat.tar.gz

# update /opt/dssat/DSSATPRO.L47 with the correct paths
RUN perl -p -i -e 's;/home1/00384/rynge;/opt;g' /opt/dssat/DSSATPRO.L47

