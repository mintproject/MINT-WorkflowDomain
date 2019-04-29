FROM mintproject/base-ubuntu18

ENV SUNDIALS_VERSION 3.2.1
ENV PIHM_VERSION 4.0

# --------
# PIHMgisR
# --------

COPY Rprofile /root/.Rprofile
RUN Rscript -e 'install.packages("rgeos"); install.packages("ncdf4"); install.packages("rgdal"); install.packages("raster"); install.packages("zoo"); install.packages("abind"); install.packages("xts")'


# ------
# PIHM++
# ------

RUN wget -nv https://computation.llnl.gov/projects/sundials/download/sundials-${SUNDIALS_VERSION}.tar.gz && \
    tar xvf sundials-${SUNDIALS_VERSION}.tar.gz && \
    cd sundials-${SUNDIALS_VERSION} && \
    mkdir build-dir && \
    cd build-dir && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local/sundials .. && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf sundials*

ENV LD_LIBRARY_PATH /usr/local/sundials/lib

RUN git clone https://github.com/shulele/PIHM-4.0.git && \
    cd PIHM-4.0 && \
    make pihm && \
    mv pihm++ /usr/bin && \
    cd .. && \
    rm -rf PIHM*
