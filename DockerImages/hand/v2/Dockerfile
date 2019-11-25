FROM mintproject/base-ubuntu18

# ------
# TauDEM
# ------

RUN git clone --branch Develop https://github.com/dtarb/TauDEM && \
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
ADD hand-heads.py  hand-weights.py  requirements.txt ./
RUN pip3 install -r requirements.txt
#ENV PATH="/usr/local/taudem/:${PATH}"
RUN echo PATH='/usr/local/taudem/:${PATH}' > /root/.bashrc
