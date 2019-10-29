FROM mintproject/base-ubuntu18

ENV TAUDEM_VERSION Develop


# ------
# TauDEM
# ------

RUN git clone --branch ${TAUDEM_VERSION} https://github.com/dtarb/TauDEM && \
    cd TauDEM/src && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && make install && \
    cd ../../.. && \
    rm -rf TauDEM


RUN Rscript -e 'install.packages("rgdal"); install.packages("raster"); install.packages("shapefiles"); install.packages("optparse");'

ADD find_inlets.cpp .
RUN g++ -I /usr/include/gdal find_inlets.cpp -lgdal -o /usr/local/bin/find_inlets
ENV PATH="/usr/local/taudem/:${PATH}"
