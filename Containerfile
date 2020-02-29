# Specific OS distribution to utilize as base image
ARG OS_VERSION=centos:7
ARG ARCHIVE_URL=https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.9.9-01744997.tar.gz

FROM $OS_VERSION

RUN mkdir -p /opt/geth \
    && curl -L https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.9.9-01744997.tar.gz | tar xzf - --strip-components=1 -C /opt/geth \
    && chmod 777 /opt/geth

RUN mkdir /entrypoint.d
COPY entrypoints/setup-config.sh  /entrypoint.d

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY start-geth.sh /usr/bin/start-geth.sh
RUN chmod +x /usr/bin/start-geth.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["start-geth.sh"]
