FROM mintproject/base-ubuntu18

# newer R
#RUN export DEBIAN_FRONTEND=noninteractive && \
#    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
#    add-apt-repository 'deb [arch=amd64,i386] http://cran.rstudio.com/bin/linux/ubuntu xenial/' && \
#    apt-get -y update && \
#    apt-get -y install r-base

# R packages for data transforms and helpers
COPY Rprofile /root/.Rprofile
RUN Rscript -e 'install.packages("rgeos"); install.packages("ncdf4"); install.packages("rgdal");'

RUN wget -nv https://computation.llnl.gov/projects/sundials/download/sundials-2.2.0.tar.gz && \
    tar xvf sundials-2.2.0.tar.gz && \
    cd sundials && \
    ./configure --prefix=/opt/sundials && \
    make && \
    make install

RUN wget -nv http://www.pihm.psu.edu/PIHM_v2.2.tar && \
    tar xvf PIHM_v2.2.tar && \
    cd PIHM_v2.2 && \
    (make clean || true) && \
    (grep -rl Makefile . | xargs sed -i 's;/Users/xxy113/software;/opt;g') && \
    make pihm && \
    mv pihm /usr/bin

