FROM mintproject/base-ubuntu18

ENV TAUDEM_VERSION 5.3.7


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
