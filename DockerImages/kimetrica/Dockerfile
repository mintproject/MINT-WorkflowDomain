FROM mintproject/base-ubuntu16

# Note: python3 is used for this project

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip3 install typing
RUN pip3 install scipy
RUN pip3 install numpy
RUN export CFLAGS=$(gdal-config --cflags) && pip3 install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
RUN pip3 install pandas
RUN pip3 install geopandas
RUN pip3 install rasterio
RUN pip3 install luigi

# add user
RUN useradd --gid 100 --uid 550 --create-home --password mint mint

USER mint
WORKDIR /home/mint

