FROM mintproject/base-ubuntu18

ENV TAUDEM_VERSION 5.3.7
ENV SUNDIALS_VERSION 3.2.1
ENV PIHM_VERSION 4.0


# ------
# TauDEM
# ------

RUN git clone --branch v${TAUDEM_VERSION} https://github.com/dtarb/TauDEM && \
    cd TauDEM/src && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && make install && \
    cd ../../.. && \
    rm -rf TauDEM

# --------
# PIHMgisR
# --------

COPY Rprofile /root/.Rprofile
RUN Rscript -e 'install.packages("GGally"); install.packages("ncdf4"); install.packages("devtools"); library("devtools"); install_github("mayani/PIHMgisR");'

# ------
# PIHM++
# ------

RUN wget -nv https://computation.llnl.gov/projects/sundials/download/sundials-${SUNDIALS_VERSION}.tar.gz && \
    tar xvf sundials-${SUNDIALS_VERSION}.tar.gz && \
    cd sundials-${SUNDIALS_VERSION} && \
    mkdir build-dir && \
    cd build-dir && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local/sundials -DOPENMP_ENABLE=1 -DMPI_ENABLE=1 .. && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf sundials*

ENV LD_LIBRARY_PATH /usr/local/sundials/lib

RUN wget "https://github.com/shulele/PIHM-${PIHM_VERSION}/archive/master.zip" && \
    unzip master.zip && \
    cd PIHM-${PIHM_VERSION}-master && \
    make pihm pihm_omp calib_omp && \
    mv pihm++ pihm_omp calib_omp /usr/bin && \
    cd .. && \
    rm -rf master.zip PIHM*
