FROM mintproject/mintviz:latest
ENV bash default
RUN cd /mintcast && \
    git pull origin master
CMD ["sh", "-c", "/mintcast/bin/mintcast.sh ${bash}"]