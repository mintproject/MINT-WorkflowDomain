FROM ubuntu:latest
RUN apt update
RUN apt install -y wget
RUN mkdir -p /opt/gams
RUN wget https://d37drm4t2jghv5.cloudfront.net/distributions/25.1.1/linux/linux_x64_64_sfx.exe -O /opt/gams/install-gams.sh
RUN chmod 755 /opt/gams/install-gams.sh
RUN cd /opt/gams && /opt/gams/install-gams.sh
RUN ln -s /opt/gams/gams25.1_linux_x64_64_sfx /opt/gams/default