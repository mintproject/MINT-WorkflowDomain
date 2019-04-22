# https://github.com/appropriate/docker-postgis/tree/f6d28e4a1871b1f72e1c893ff103f10b6d7cb6e1/10-2.4

FROM postgres:10.6
LABEL maintainer="Rajiv Mayani <mayani@isi.edu>"

ENV POSTGIS_MAJOR 2.5
#ENV POSTGIS_VERSION 2.4.3+dfsg-2.pgdg90+1

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
           postgis \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
