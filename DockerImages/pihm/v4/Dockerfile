FROM mintproject/base-ubuntu18

# --------
# PIHMgisR
# --------

RUN Rscript -e 'install.packages("devtools"); library("devtools"); install_github("shulele/PIHMgisR");'

# ------
# PIHM++
# ------

ENV PIHM_VERSION 4.0

RUN wget "https://github.com/shulele/PIHM-${PIHM_VERSION}/archive/master.zip" && \
    unzip master.zip && \
    cd PIHM-${PIHM_VERSION}-master && \
    ./configure && \
    make pihm && \
    mv pihm++ /usr/bin && \
    cd .. && \
    rm -rf master.zip PIHM*

# --------
# AutoPIHM
# --------

# RUN wget "https://github.com/shulele/AutoPIHM/archive/master.zip" && \
#     unzip master.zip && \
#     mv AutoPIHM-master AutoPIHM && \
#     rm -rf master.zip
