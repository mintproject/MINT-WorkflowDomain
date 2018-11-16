FROM mintproject/base-ubuntu16

RUN wget -nv -O ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -f -p /opt/conda && \
    export PATH=/opt/conda/bin:$PATH && \
    conda install --yes anaconda && \
    conda install --yes -c conda-forge -c digitalglobe gbdxtools && \
    conda install --yes -c conda-forge numpy pandas tensorflow keras && \
    conda create --yes -n gdalenv -c conda-forge python=2.7 numpy gdal=2.2.4 urllib3=1.23 rasterio



