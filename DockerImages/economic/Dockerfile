FROM mintproject/base-el7

COPY linux_x64_64_sfx.exe /tmp/linux_x64_64_sfx.exe
RUN mkdir -p /opt/gams && \
    cd /opt/gams && \
    chmod 755 /tmp/linux_x64_64_sfx.exe && \
    /tmp/linux_x64_64_sfx.exe

