FROM mintproject/base-ubuntu16

RUN wget -nv -O ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.3.14-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -f -p /opt/conda && \
    export PATH=/opt/conda/bin:$PATH && \
    conda install --yes anaconda && \
    conda install --yes -c conda-forge numpy pandas tensorflow keras shapely descarteslabs scikit-image && \
    conda create --yes -n gdalenv -c conda-forge python=3.6 numpy gdal=2.4.2 urllib3 rasterio h5py=2.8.0 && \
    /opt/conda/bin/pip install s2cloudless
