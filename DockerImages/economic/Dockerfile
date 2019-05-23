FROM mintproject/base-el7

ENV GAMS_MAJOR_VERSION "27"
ENV GAMS_MINOR_VERSION "1"
ENV GAMS_PATCH_VERSION "0"

RUN wget --directory-prefix /tmp/ "https://d37drm4t2jghv5.cloudfront.net/distributions/${GAMS_MAJOR_VERSION}.${GAMS_MINOR_VERSION}.${GAMS_PATCH_VERSION}/linux/linux_x64_64_sfx.exe" && \
    mkdir -p /opt/gams && \
    cd /opt/gams && \
    chmod 755 /tmp/linux_x64_64_sfx.exe && \
    /tmp/linux_x64_64_sfx.exe && \
    ln -s /opt/gams/gams${GAMS_MAJOR_VERSION}.${GAMS_MINOR_VERSION}_linux_x64_64_sfx/gams /usr/local/bin/ && \
    rm /tmp/linux_x64_64_sfx.exe
