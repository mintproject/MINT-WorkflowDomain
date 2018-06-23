FROM mintproject/base-ubuntu16

RUN wget -nv -O ~/miniconda.sh http://repo.continuum.io/miniconda/Miniconda3-4.5.1-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -f -p /opt/conda && \
    export PATH=/opt/conda/bin:$PATH && \
    conda install --yes anaconda && \
    conda install --yes -c conda-forge numpy pandas tensorflow=1.5 keras shapely gdal=2.2.4 opencv rasterio && \
    conda create --yes -n gdalenv -c conda-forge python=2.7 gdal=2.2.4


